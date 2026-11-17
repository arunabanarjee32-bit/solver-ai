"""Verify every preserved ZIP member, its manifest record and optional Git blob."""

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_record(record: dict, git_index: bool) -> None:
    path = ROOT / record["path"]
    if not path.resolve().is_relative_to((ROOT / "AnalyseFuture").resolve()):
        raise ValueError(f"Path outside preservation folder: {record['path']}")
    data = path.read_bytes()
    if len(data) != record["bytes"] or digest(data) != record["sha256"]:
        raise ValueError(f"Preserved bytes differ: {record['path']}")
    if git_index:
        staged = subprocess.check_output(
            ["git", "show", f":{record['path']}"], cwd=ROOT
        )
        if staged != data:
            raise ValueError(f"Git index differs: {record['path']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--git-index", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "AnalyseFuture/manifest.json").read_text())
    count = 0
    for archive in manifest["archives"]:
        verify_record(archive, args.git_index)
        with zipfile.ZipFile(ROOT / archive["path"]) as source:
            names = [item.filename for item in source.infolist() if not item.is_dir()]
            records = {item["archive_member"]: item for item in archive["files"]}
            if len(names) != len(records) or set(names) != set(records):
                raise ValueError(f"Incomplete archive inventory: {archive['path']}")
            for name in names:
                record = records[name]
                verify_record(record, args.git_index)
                if digest(source.read(name)) != record["sha256"]:
                    raise ValueError(f"Archive member differs: {name}")
                count += 1
    history_path = ROOT / "AnalyseFuture/repository-inventory/historical-branches.json"
    history = json.loads(history_path.read_text()) if history_path.exists() else {"files": []}
    for record in history["files"]:
        verify_record(record, args.git_index)
    print(
        f"Preservation verified: {len(manifest['archives'])} ZIPs, {count} members, "
        f"{len(history['files'])} branch snapshots."
    )


if __name__ == "__main__":
    main()
