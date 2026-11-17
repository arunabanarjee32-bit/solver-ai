"""Generate or check the tracked-file ledger without executing project source."""

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT_REPORT = "AnalyseFuture/repository-inventory/COMPLETE_FILE_INVENTORY.txt"
JSON_REPORT = "AnalyseFuture/repository-inventory/current-files.json"
OUTPUTS = {TEXT_REPORT, JSON_REPORT}


def ownership(path: str) -> str:
    for prefix, owner in (
        ("AnalyseFuture/extracted/", "inactive upstream research"),
        ("AnalyseFuture/historical-implementations/", "inactive historical branch evidence"),
        ("AnalyseFuture/archives/", "original uploaded ZIP evidence"),
        ("AnalyseFuture/", "recovery records and inventory"),
        ("apps/web/features/", "web feature: " + path.split("/")[3]
         if path.startswith("apps/web/features/") else "web"),
        ("apps/web/", "web framework, shared shell and tooling"),
        ("services/api/", "authenticated API and durable queue"),
        ("services/judge/", "isolated judge control and sandbox"),
        ("tests/tooling/", "repository and GitHub tooling safety cases"),
        ("tests/", "cross-service browser validation"),
        ("docs/engineering/backlog/", "implementation task catalogue and publication records"),
        ("docs/engineering/", "engineering workflow and contribution guidance"),
        ("docs/", "specifications, decisions and development guidance"),
        ("scripts/github/", "GitHub backlog planning and explicit publication tooling"),
        ("scripts/", "development and verification tools"),
        (".github/", "hosted validation and contributor guidance"),
    ):
        if path.startswith(prefix):
            return owner
    return "root project guidance, dependencies and deployment configuration"


def imports(path: str, data: bytes) -> list[str]:
    try:
        text = data.decode("utf-8")
        if path.endswith(".py"):
            tree = ast.parse(text, filename=path)
            return sorted({
                "." * node.level + (node.module or "")
                for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
            } | {
                alias.name for node in ast.walk(tree) if isinstance(node, ast.Import)
                for alias in node.names
            })
        if path.endswith((".ts", ".tsx", ".mjs")):
            return sorted(set(re.findall(
                r"(?:from\s+|import\s*(?:\(\s*)?)['\"]([^'\"]+)['\"]", text
            )))
    except (UnicodeDecodeError, SyntaxError):
        return ["Non-text content or parser limitation; see review record."]
    return []


def build() -> tuple[dict, str]:
    folder = ROOT / "AnalyseFuture/repository-inventory"
    annotations = {}
    for source in sorted((folder / "reviews").glob("*.json")):
        review = json.loads(source.read_text())
        for row in review.get("files", []):
            annotations[row["path"]] = {**row, "review_record": str(source.relative_to(ROOT))}
    move_file = folder / "moves.json"
    moves = json.loads(move_file.read_text())["baseline_module_moves"] if move_file.exists() else {}
    functional_file = folder / "functional-moves.json"
    if functional_file.exists():
        moves.update(json.loads(functional_file.read_text())["moves"])
    for original, annotation in list(annotations.items()):
        destination = original
        seen = set()
        while destination in moves:
            if destination in seen:
                raise ValueError("Circular file mapping")
            seen.add(destination)
            destination = moves[destination]
        if destination != original:
            annotations[destination] = {**annotation, "original_path": original}
    paths = set(subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT
    ).decode().rstrip("\0").split("\0")) | OUTPUTS
    rows = []
    for path in sorted(paths):
        annotation = annotations.get(path, {})
        data = b"" if path in OUTPUTS else subprocess.check_output(
            ["git", "show", f":{path}"], cwd=ROOT
        )
        owner = ownership(path)
        default = (
            "Preserved branch snapshot; provenance in historical-branches.json."
            if "historical-implementations/" in path else
            "Recovery evidence report or structured review record."
            if path.startswith("AnalyseFuture/") else
            "Repository support file; responsibility identified by owner and filename."
        )
        rows.append({
            "path": path,
            "owner": owner,
            "purpose": annotation.get("purpose", default),
            "feature": annotation.get("feature", owner),
            "active": not path.startswith((
                "AnalyseFuture/extracted/", "AnalyseFuture/archives/",
                "AnalyseFuture/historical-implementations/",
            )),
            "dependencies": imports(path, data) or annotation.get("dependencies", []),
            "assessment": annotation.get("status", "Current support/report artifact; see owner."),
            "risks": annotation.get("risks", []),
            "review_record": annotation.get("review_record", "Coordinator support-file review"),
            "original_path": annotation.get("original_path", path),
            "bytes": None if path in OUTPUTS else len(data),
            "sha256": None if path in OUTPUTS else hashlib.sha256(data).hexdigest(),
        })
    document = {
        "baseline_commit": json.loads((folder / "baseline.json").read_text())["baseline_commit"],
        "scope": "All current Git-index paths; generated inventory outputs included.",
        "self_hash_policy": "Size/hash omitted for both inventory outputs to avoid recursion.",
        "tracked_files": len(rows),
        "files": rows,
    }
    lines = [
        "COMPLETE FILE INVENTORY", "Baseline: " + document["baseline_commit"],
        f"Current indexed paths: {len(rows)}", document["scope"],
        document["self_hash_policy"],
        "Review records describe baseline static findings; final validation and fixes are in",
        "TEST_AND_VALIDATION_REPORT.txt and SECURITY_AUDIT.txt. Archived code was not run.",
        "Ignored dependency/build caches and private runtime state remain outside Git and intact.",
        "Binary assets received metadata/format review, not semantic visual/malware certification.",
        "Current runtime results and publication limits are recorded in validation/; this ledger is static.", "",
    ]
    for row in rows:
        lines.extend([
            row["path"], "  Owner: " + row["owner"], "  Purpose: " + row["purpose"],
            "  Active: " + str(row["active"]) + "; feature: " + str(row["feature"]),
            "  Dependencies: " + ", ".join(map(str, row["dependencies"])),
            "  Assessment: " + str(row["assessment"]),
            "  Risks/gaps: " + "; ".join(map(str, row["risks"])),
            "  Review: " + row["review_record"],
            "  SHA256: " + str(row["sha256"]) + "; bytes: " + str(row["bytes"]), "",
        ])
    return document, "\n".join(line.rstrip() for line in lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--write", action="store_true")
    choice.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document, text = build()
    contents = {TEXT_REPORT: text, JSON_REPORT: json.dumps(document, indent=2) + "\n"}
    for path, expected in contents.items():
        if args.write:
            (ROOT / path).write_text(expected)
        elif (ROOT / path).read_text() != expected:
            raise SystemExit("Inventory is stale; stage intended files and regenerate with --write.")
    print(f"Tracked inventory {'written' if args.write else 'verified'}: {document['tracked_files']} paths.")


if __name__ == "__main__":
    main()
