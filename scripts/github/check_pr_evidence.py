"""Validate inert PR evidence metadata; never execute commands or contact GitHub."""

import argparse
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "docs/engineering/backlog/issues.json"
MAX_BODY_BYTES = 65536
MAX_EVENT_BYTES = 4 * 1024 * 1024
BLOCK = re.compile(
    r"^```solver-ai-evidence[ \t]*\n(.*?)^```[ \t]*(?:\n|$)", re.MULTILINE | re.DOTALL
)
OPENER = re.compile(r"^```solver-ai-evidence[ \t]*$", re.MULTILINE)
FIELDS = {
    "schema_version", "backlog_id", "execution_order", "head_revision",
    "prerequisites", "before", "after", "changed_paths", "checks",
    "security_data_impact", "rollback", "limitations", "review_requested",
}
OUTCOMES = {"passed", "failed", "skipped", "not-run", "expected-failure"}
PREREQUISITE_STATES = {"completed", "blocked", "not-completed", "not-run", "waived"}
PLACEHOLDERS = {"todo", "tbd", "n/a", "none", "...", "fill me", "replace me", "not applicable"}


def unique_object(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON field")
        result[key] = value
    return result


def reject_constant(_value: str):
    raise ValueError("Non-JSON numeric value")


def meaningful(value, *, minimum: int = 8, maximum: int = 4000) -> bool:
    return (
        isinstance(value, str) and minimum <= len(value.strip()) <= maximum
        and value.strip().casefold() not in PLACEHOLDERS
        and not re.fullmatch(r"<[^>]*>", value.strip())
    )


def valid_path(value) -> bool:
    if not isinstance(value, str) or not 1 <= len(value) <= 300:
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute() and path.as_posix() == value and not value.endswith("/")
        and not any(part in {".", ".."} for part in value.split("/"))
        and "\\" not in value and ":" not in value and not value.startswith("~")
        and not any(ord(character) < 32 or ord(character) == 127 for character in value)
    )


def validate(body, head_revision, catalog: dict) -> list[str]:
    """Return fixed errors only; PR-supplied values are never included in logs."""
    if not isinstance(body, str) or len(body.encode(errors="replace")) > MAX_BODY_BYTES:
        return ["body: supply a bounded PR body containing one evidence block."]
    normalized = body.replace("\r\n", "\n")
    blocks = BLOCK.findall(normalized)
    if len(blocks) != 1 or len(OPENER.findall(normalized)) != 1:
        return ["body: include exactly one solver-ai-evidence fenced JSON block."]
    try:
        evidence = json.loads(
            blocks[0], object_pairs_hook=unique_object, parse_constant=reject_constant
        )
    except (ValueError, RecursionError):
        return ["schema: evidence must be valid JSON without duplicate fields."]
    if not isinstance(evidence, dict) or set(evidence) != FIELDS:
        return ["schema: supply exactly the documented evidence fields."]
    errors = []
    if type(evidence["schema_version"]) is not int or evidence["schema_version"] != 1:
        errors.append("schema_version: use integer version 1.")
    tasks = {row["id"]: row for row in catalog["issues"]}
    identifier = evidence["backlog_id"]
    task = tasks.get(identifier) if isinstance(identifier, str) else None
    if task is None:
        errors.append("backlog_id: use one known stable catalogue identifier.")
    elif (
        type(evidence["execution_order"]) is not int
        or evidence["execution_order"] != task["order"]
    ):
        errors.append("execution_order: use the catalogue order, not the identifier suffix.")
    if (
        not isinstance(head_revision, str)
        or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", head_revision)
        or evidence["head_revision"] != head_revision
    ):
        errors.append("head_revision: evidence must describe the current PR head SHA.")
    for field in ["before", "after", "security_data_impact", "rollback", "limitations"]:
        if not meaningful(evidence[field]):
            errors.append(f"{field}: provide concrete text rather than a placeholder.")
    paths = evidence["changed_paths"]
    if (
        not isinstance(paths, list) or not 1 <= len(paths) <= 256
        or not all(valid_path(path) for path in paths)
        or len(set(paths)) != len(paths)
    ):
        errors.append("changed_paths: list unique repository-relative file paths without traversal.")
    prerequisites = evidence["prerequisites"]
    dependency_ids = []
    if not isinstance(prerequisites, list) or len(prerequisites) > 128:
        errors.append("prerequisites: list every catalogue dependency and its evidence.")
    else:
        for row in prerequisites:
            if (
                not isinstance(row, dict) or set(row) != {"id", "status", "evidence"}
                or not isinstance(row["id"], str)
                or not isinstance(row["status"], str)
                or row["status"] not in PREREQUISITE_STATES
                or not meaningful(row["evidence"])
            ):
                errors.append("prerequisites: each record needs id, explicit status and concrete evidence.")
                continue
            dependency_ids.append(row["id"])
        expected = set(task.get("depends_on", [])) if task else set()
        if set(dependency_ids) != expected or len(dependency_ids) != len(set(dependency_ids)):
            errors.append("prerequisites: account for each required dependency exactly once.")
    checks = evidence["checks"]
    if not isinstance(checks, list) or not 1 <= len(checks) <= 64:
        errors.append("checks: supply observed check records, including honest not-run reasons.")
    else:
        for row in checks:
            if (
                not isinstance(row, dict) or set(row) != {"command", "outcome", "evidence"}
                or not meaningful(row["command"], minimum=3, maximum=1000)
                or not isinstance(row["outcome"], str)
                or row["outcome"] not in OUTCOMES
                or not meaningful(row["evidence"])
            ):
                errors.append("checks: each record needs a command, supported outcome and result/reason.")
    if evidence["review_requested"] is not True:
        errors.append("review_requested: request maintainer review; this gate cannot approve or merge.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    args = parser.parse_args()
    try:
        if args.event.stat().st_size > MAX_EVENT_BYTES:
            raise ValueError("Event too large")
        event = json.loads(args.event.read_text())
        if not isinstance(event, dict):
            raise TypeError("Invalid event shape")
        pr = event["pull_request"]
        if not isinstance(pr, dict) or not isinstance(pr.get("head"), dict):
            raise TypeError("Invalid PR shape")
        catalog = json.loads(args.catalog.read_text())
        errors = validate(pr.get("body"), pr["head"]["sha"], catalog)
    except (OSError, ValueError, TypeError, KeyError, RecursionError):
        errors = ["input: PR event or trusted catalogue could not be read safely."]
    if errors:
        print("PR evidence metadata is incomplete:")
        for error in errors:
            print("- " + error)
        return 1
    print("PR evidence metadata is complete. This does not verify tests or approve the PR.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
