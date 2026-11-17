"""Plan or publish the ordered backlog using existing gh authentication.

Publishing is explicit. Remote markers are reconciled before any POST so a
restart cannot silently duplicate a partly published backlog. Existing issues
are never edited, reopened, assigned or closed by this tool.
"""

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "docs/engineering/backlog/issues.json"
RECEIPT = ROOT / "docs/engineering/backlog/publication.json"
IDENTIFIER = re.compile(r"SAI-B\d{3}\Z")
MARKER = re.compile(r"<!-- solver-ai-backlog:(SAI-B\d{3}) -->")


class PublicationError(RuntimeError):
    """A safe, actionable publication failure without credential diagnostics."""


def validate_catalog(catalog: dict, *, minimum: int = 101) -> list[dict]:
    if catalog.get("repository") != "arunabanarjee32-bit/solver-ai":
        raise PublicationError("The catalogue must target the selected solver-ai repository.")
    issues = catalog.get("issues", [])
    if len(issues) < minimum:
        raise PublicationError(f"The catalogue needs at least {minimum} actionable issues.")
    seen: set[str] = set()
    titles: set[str] = set()
    for order, issue in enumerate(issues, 1):
        identifier = issue.get("id", "")
        if not IDENTIFIER.fullmatch(identifier) or identifier in seen:
            raise PublicationError("Backlog identifiers must be unique SAI-Bnnn values.")
        if issue.get("order") != order:
            raise PublicationError("Backlog ordering must be contiguous and explicit.")
        title = issue.get("title", "")
        if not title.strip() or len(title) > 180 or title.casefold() in titles:
            raise PublicationError("Issue titles must be unique and at most 180 characters.")
        if issue.get("priority") not in {"P0", "P1", "P2", "P3"}:
            raise PublicationError(f"{identifier} has no supported priority.")
        for field in ["problem", "area", "phase", "risk", "owner_role"]:
            if not isinstance(issue.get(field), str) or not issue[field].strip():
                raise PublicationError(f"{identifier} is missing {field}.")
        for field in ["scope", "acceptance", "validation", "out_of_scope", "target_paths"]:
            if not isinstance(issue.get(field), list) or not issue[field]:
                raise PublicationError(f"{identifier} is missing concrete {field}.")
        for dependency in issue.get("depends_on", []):
            if dependency not in seen:
                raise PublicationError(f"{identifier} depends on an unknown or later issue.")
        for path in issue["target_paths"]:
            if not (ROOT / path).resolve().is_relative_to(ROOT):
                raise PublicationError(f"{identifier} has a target outside the repository.")
        status = issue.get("implementation_status", "planned")
        if status not in {"planned", "completed_locally"}:
            raise PublicationError(f"{identifier} has an unsupported implementation status.")
        if status == "completed_locally" and not issue.get("completion_evidence", "").strip():
            raise PublicationError(f"{identifier} needs completion evidence before publication is skipped.")
        seen.add(identifier)
        titles.add(title.casefold())
    return issues


def issue_title(issue: dict) -> str:
    return f"[{issue['id']}] {issue['title']}"


def render_body(issue: dict, published: dict, completed: dict | None = None) -> str:
    completed = completed or {}
    dependencies = [
        f"- [{identifier}]({published[identifier]['url']})"
        if identifier in published else
        f"- [{identifier} (completed locally)]"
        f"(https://github.com/arunabanarjee32-bit/solver-ai/blob/main/"
        f"docs/engineering/backlog/issues/{identifier}.md)"
        if identifier in completed else f"- {identifier} (confirm prerequisite state in the catalogue)"
        for identifier in issue.get("depends_on", [])
    ] or ["- No backlog prerequisites; observe the maintainer's release and spending gates."]
    lines = [
        f"<!-- solver-ai-backlog:{issue['id']} -->",
        f"Order: {issue['order']} / Priority: {issue['priority']} / Phase: {issue['phase']}",
        f"Area: {issue['area']} / Suggested role: {issue['owner_role']}", "",
        "Implementation status: " + issue.get("implementation_status", "planned"), "",
        "## Problem", "", issue["problem"], "", "## Prerequisites", "", *dependencies,
    ]
    if issue.get("implementation_status") == "completed_locally":
        lines[5:5] = ["Completed locally: " + issue["completion_evidence"], ""]
    for heading, field in [
        ("Current code ownership", "target_paths"), ("Scope", "scope"),
        ("Acceptance criteria", "acceptance"), ("Validation", "validation"),
        ("Out of scope", "out_of_scope"),
    ]:
        lines += ["", "## " + heading, ""]
        lines += [f"- {value}" for value in issue[field]]
    lines += [
        "", "## Risk and review", "", issue["risk"], "",
        ("This task is recorded as completed locally. Do not reimplement it as missing work; "
         "open a separately scoped follow-up when a defect or new requirement exists."
         if issue.get("implementation_status") == "completed_locally" else
         "Implement this issue on a dedicated branch and submit a PR linked here. "
        "Include the exact tests run and remaining limitations. Do not self-merge. "
        "A maintainer/assistant review must inspect the diff, dependencies, security "
        "and actual check results before a maintainer-authorized merge. "
        "Do not enable paid services, training or new production infrastructure "
        "without the owner's explicit approval."), "",
    ]
    return "\n".join(lines)


class GitHub:
    def __init__(self):
        self._last_post: float | None = None

    def request(self, endpoint: str, payload: dict | None = None, *, pages: bool = False):
        command = ["gh", "api", "--hostname", "github.com"]
        if pages:
            command += ["--paginate", "--slurp"]
        if payload is not None:
            command += ["--method", "POST", "--input", "-"]
            # Pace content creation. A failed/uncertain POST still stops the run;
            # pacing is never an automatic mutation retry.
            if self._last_post is not None:
                remaining = 1.1 - (time.monotonic() - self._last_post)
                if remaining > 0:
                    time.sleep(remaining)
            self._last_post = time.monotonic()
        command.append(endpoint)
        try:
            result = subprocess.run(
                command, input=json.dumps(payload) if payload is not None else None,
                capture_output=True, text=True, timeout=60, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise PublicationError(
                "GitHub operation was unavailable or timed out. Reconcile remote markers "
                "before retrying; never repeat an uncertain POST blindly."
            ) from error
        if result.returncode:
            raise PublicationError(
                "GitHub API access failed. Check api.github.com network access and the "
                "existing gh account's repository issue permission. No secret values "
                "belong in this report or chat. An interrupted POST is not retried."
            )
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as error:
            raise PublicationError("GitHub returned an unreadable response; reconcile before retry.") from error


def issue_record(row: dict, repository: str) -> dict:
    number = row.get("number")
    url = f"https://github.com/{repository}/issues/{number}"
    if type(number) is not int or row.get("html_url") != url:
        raise PublicationError("Unexpected remote issue identity; refusing publication.")
    return {
        "number": number, "url": url, "title": row.get("title", ""),
        "state": row.get("state", "unknown"),
    }


def remote_index(rows: list[dict], repository: str) -> dict:
    indexed = {}
    for row in rows:
        if "pull_request" in row:
            continue
        marker = MARKER.search(row.get("body") or "")
        title_match = re.match(r"\[(SAI-B\d{3})\] ", row.get("title", ""))
        identifier = marker.group(1) if marker else title_match.group(1) if title_match else None
        if identifier is None:
            continue
        if identifier in indexed:
            raise PublicationError(f"Duplicate remote identifier {identifier}; resolve before publishing.")
        indexed[identifier] = issue_record(row, repository)
    return indexed


def save_receipt(path: Path, receipt: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as temporary:
        temporary.write(json.dumps(receipt, indent=2) + "\n")
        name = Path(temporary.name)
    name.replace(path)


def publish(catalog: dict, github: GitHub, receipt_path: Path, digest: str) -> dict:
    all_issues = validate_catalog(catalog)
    issues = [issue for issue in all_issues if issue.get("implementation_status") != "completed_locally"]
    repository = catalog["repository"]
    receipt = {
        "repository": repository, "catalog_sha256": digest, "status": "in_progress", "issues": {},
        "skipped_completed": {
            issue["id"]: issue["completion_evidence"] for issue in all_issues
            if issue.get("implementation_status") == "completed_locally"
        },
    }
    try:
        metadata = github.request(f"repos/{repository}")
        if metadata.get("full_name") != repository or not metadata.get("has_issues"):
            raise PublicationError("Target repository identity or enabled issue tracker could not be verified.")
        pages = github.request(f"repos/{repository}/issues?state=all&per_page=100", pages=True)
        rows = [row for page in pages for row in page]
        indexed = remote_index(rows, repository)
        for issue in issues:
            identifier = issue["id"]
            if identifier not in indexed:
                # Reuse a unique pre-existing bare title without changing its body.
                # Multiple exact matches require a human reconciliation, not another POST.
                matches = [
                    row for row in rows if "pull_request" not in row
                    and row.get("title", "").casefold() == issue["title"].casefold()
                    and not MARKER.search(row.get("body") or "")
                ]
                if len(matches) > 1:
                    raise PublicationError(f"Ambiguous existing title for {identifier}; reconcile first.")
                if matches:
                    indexed[identifier] = issue_record(matches[0], repository)
            accepted_titles = {issue_title(issue).casefold(), issue["title"].casefold()}
            if identifier in indexed and indexed[identifier]["title"].casefold() not in accepted_titles:
                raise PublicationError(f"Remote {identifier} belongs to another title; refusing overwrite.")
        for issue in issues:
            identifier = issue["id"]
            if identifier not in indexed:
                created = github.request(f"repos/{repository}/issues", {
                    "title": issue_title(issue),
                    "body": render_body(issue, indexed, receipt["skipped_completed"]),
                })
                indexed.update(remote_index([created], repository))
                if identifier not in indexed:
                    raise PublicationError("Created issue marker was not confirmed; reconcile before retry.")
            receipt["issues"][identifier] = indexed[identifier]
            save_receipt(receipt_path, receipt)
            print(f"Confirmed {identifier}: {indexed[identifier]['url']}", flush=True)
        receipt["status"] = "published"
    except PublicationError as error:
        receipt["status"] = "blocked_or_interrupted"
        receipt["reason"] = str(error)
        save_receipt(receipt_path, receipt)
        raise
    save_receipt(receipt_path, receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--receipt", type=Path, default=RECEIPT)
    parser.add_argument("--publish", action="store_true", help="Create missing issues; default is offline validation.")
    args = parser.parse_args()
    raw = args.catalog.read_bytes()
    catalog = json.loads(raw)
    issues = validate_catalog(catalog)
    if args.publish:
        publish(catalog, GitHub(), args.receipt, hashlib.sha256(raw).hexdigest())
    else:
        completed = sum(issue.get("implementation_status") == "completed_locally" for issue in issues)
        print(
            f"Offline plan valid: {len(issues)} ordered tasks "
            f"({len(issues) - completed} pending, {completed} completed locally); no GitHub requests made."
        )


if __name__ == "__main__":
    try:
        main()
    except PublicationError as error:
        raise SystemExit(str(error)) from None
