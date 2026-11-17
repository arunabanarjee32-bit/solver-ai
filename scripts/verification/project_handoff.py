"""Render the root project handoff from reviewed files, features and task cards."""

import argparse
import json
from collections import Counter
from pathlib import Path, PurePosixPath
from urllib.parse import quote

from repository_inventory import build

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "PROJECT_HANDOFF.md"
DIRECTORIES = ROOT / "docs/engineering/handoff-directories.json"

INTRODUCTION = """# Solver AI: project guide and complete implementation handoff

This is the homepage handoff for **Solver AI**, the DSA, competitive-programming
and ICPC practice project in `arunabanarjee32-bit/solver-ai`. Give another coding
tool this file together with [AGENTS.md](AGENTS.md). It explains what works,
where every tracked file belongs, and the detailed work still to complete.

This document is generated from the reviewed file inventory, feature inventory
and canonical task catalogue. Update their sources and regenerate it when the
implementation changes; the maintenance commands are at the end.

## Navigation

- [Main goal and current user journey](#main-goal-and-current-user-journey)
- [DSA solver and fine-tuning delivery](#dsa-solver-and-fine-tuning-delivery)
- [Current evidence and remaining limits](#current-evidence-and-remaining-limits)
- [How another tool should continue](#how-another-tool-should-continue)
- [Every feature: implemented, partial and proposed](#feature-register)
- [Every folder and its responsibility](#complete-folder-map)
- [Every tracked file and its purpose](#complete-file-map)
- [Ordered task index](#ordered-task-index)
- [Complete task specifications](#complete-task-specifications)
- [PR review and merge process](#pr-review-and-merge-process)
- [Keeping this handoff current](#keeping-this-handoff-current)

## Main goal and current user journey

Build an independently controlled learning platform where people can practice
authorized algorithm problems, write code, receive isolated judge verdicts,
understand mistakes, and eventually get measured AI tutoring. Later milestones
add virtual contests, ICPC team practice, bounded candidate solution generation
and licensed-data model research. Product quality, original or authorized content,
privacy and reproducible evidence are the foundations.

The current local journey is: browse/search/filter the three original seed
problems → open a statement and samples → edit Python or C++17 in Monaco → keep
private browser drafts → create/sign into a local account → run or submit through
the separate gVisor judge → inspect the owned submission history and finite
verdict. Public author-written hints and an authenticated author-written hint
request interface are available. These hints are authored content; live AI
generation has not been implemented.

The architecture keeps three boundaries: Next.js/TypeScript owns the browser and
account service; FastAPI/Python owns the catalog, authenticated APIs and durable
submission queue; the trusted Python judge worker controls separate gVisor
sandboxes for learner Python/C++17 programs. Expected answers and host credentials
stay outside the learner sandbox. SQLite supports local state. PostgreSQL and
larger-scale service operations are future work.

Keeping TypeScript for browser/Next.js code and Python for API/judge control is
intentional. Learner languages are a separate product capability. A rewrite into
one language is unnecessary for this handoff and is not an assigned task; shared
HTTP contracts and feature ownership connect the existing services.

## DSA solver and fine-tuning delivery

The main ambition is broad competence on previously unseen DSA problems. A ready
system must attempt supported formats within a budget, generate/explain code,
test it through the isolated judge and report observed results or a clear failure.
No completed task list, model checkpoint or finite evaluation guarantees solving
every possible problem. Track coverage by topic, difficulty, language and format.

Read the [complete readiness checklist](docs/product/DSA_SOLVER_READINESS.md) and
[fine-tuning model research catalogue](docs/research/FINETUNING_MODEL_RESEARCH.md).
**No checkpoint or model family is selected.** The catalogue compares a broad
set of open-weight families and API-baseline alternatives for future research;
it does not claim to enumerate every model or declare a universal best model.

The solver delivery work includes supported-problem contracts; reviewed
evaluators; permitted disjoint training/evaluation data; empirical model
comparison; reproducible SFT/LoRA/QLoRA tooling; approved external smoke and real
training runs; artifact/base/tokenizer lineage; matched-budget held-out and
regression evaluation; qualified inference, pilot and rollback; and controlled
failure-driven improvement. Optional preference/RL work follows reliable rewards
and separate approval. No weights, GPU job, provider or training is activated here.

**B080 is only the training admission gate.** Appended training-delivery tasks
cover actual future implementation and execution beyond it. They remain planned.
Use each card's prerequisites; unrelated contest/business tasks do not become
mandatory ML dependencies merely because they appear earlier in the index.

## Current evidence and remaining limits

The full `npm run test:all` gate passed with exit status **0** at source revision
`33ed42f0b42b43e228c547cfc106c5c874bc61d1`: **337 cases** (137 API, 7 auth,
118 judge including 15 real gVisor cases, 50 repository-tooling cases, and
25 enabled browser cases), plus lint, TypeScript, optimized build and the
private-state packaging guard. The current handoff change is documentation and
documentation generation; that earlier run is named-revision evidence, not a
claim that new application behavior was tested here. See the
[status ledger](docs/status/PROJECT_STATUS.md) and
[validation report](AnalyseFuture/validation/TEST_AND_VALIDATION_REPORT.txt).

Local production-mode builds/Compose smoke checks are recorded. A public
production release, production security certification, current hosted full
gVisor CI, real AI provider, verified general solver, contests, model training,
payments and institution operations are **not implemented**. Finite judge cases
do not prove correctness on every possible input. Perfect AI solving and guaranteed
future model breakthroughs cannot be promised. One-year/two-year/later research
horizons in the [future vision](AnalyseFuture/planning/PROJECT_VISION_AND_FUTURE_ROADMAP.txt)
are conditional plans rather than deadlines or completed features.

Both uploaded ZIPs, all 122 extracted members and 23 historical branch snapshots
are preserved in `AnalyseFuture/`. They are inactive evidence/research, not adopted
product modules. Five archived dataset files contain LFS pointers without their
underlying datasets. Preserve their bytes and provenance. The repository audit
does not establish who caused the reported disruption or certify that a GitHub
account compromise has been resolved.

Git fetch/push works. GitHub API access is currently blocked by the environment's
`api.github.com` network policy. The local task cards are prepared, but **zero
remote issues have been confirmed created**. An additive network-settings draft
requires review/save and environment publication; permissions must then be
verified. Consult the [publication receipt](docs/engineering/backlog/publication.json)
before claiming any issue exists. No background assistant monitor or automatic
merge service is running.

## How another tool should continue

1. Read this file, [AGENTS.md](AGENTS.md), the
   [current status](docs/status/PROJECT_STATUS.md),
   [development guide](docs/onboarding/DEVELOPMENT.md) and the relevant feature code.
   Search for existing implementation before adding another version.
2. Claim **one** ready task below. Use the **Order** column, not the numeric ID
   suffix. Verify its prerequisites; independent ready tasks can proceed in
   parallel when their ownership and contracts do not conflict.
3. The next governance tasks include **SAI-B127** (actual reviewer identities and
   branch rules), **SAI-B002** (owner licensing/contribution decision) and
   **SAI-B003** (pilot/privacy/data lifecycle charter). These require their named
   owner decisions. Ready engineering work such as **SAI-B004** can proceed within
   its scope while those decisions are pending. Do not invent approvals.
4. Keep changes in the named functional collection. Preserve account ownership,
   queue leases, hidden grading data and the sandbox boundary. Never run learner
   programs in the host/API/web process or substitute ordinary containers when
   gVisor is unavailable. Preserve old/uncertain work with provenance in
   `AnalyseFuture/`; keep secrets/private runtime data outside Git.
5. Create a focused branch and PR for other-tool implementation. Include the
   stable local task ID/card if no GitHub issue exists, exact head revision,
   observed before/after behavior, changed paths, prerequisites, checks actually
   run, remaining risks and rollback. Fill the PR evidence record honestly.
6. Run the checks relevant to the task and the required gates. Record failures,
   skips and unrun checks. Do not weaken security or fabricate test results.
7. Update status, feature/file records and this handoff for behavior actually
   implemented. Request maintainer/assistant review; do not self-merge.

Do not purchase compute, activate a paid provider, send private submissions to
external services, train on datasets, settle licensing or release to production
without the stated owner approval. Task assignment does not grant those choices.
The owner has separately authorized this maintenance session's direct-to-`main`
checkpoint commits; other-tool contributions use the reviewed PR workflow.
"""

ENDING = """## PR review and merge process

Other tools implement one scoped task and submit a PR. Bring its URL or number
into an active assistant session. Review covers the exact head diff, task and
dependency fit, contracts/imports, ownership/auth, sandbox boundaries, dependency
and data changes, observed checks, docs and rollback. Requested corrections get
reviewed again at the new head before an owner-authorized merge. Preserve Git
history and never force-push `main`.

The implemented evidence metadata gate checks a structured PR record using
trusted base code with read-only permissions. It does not prove tests ran, approve
code or authorize a merge. Hosted execution of this gate and effective GitHub
branch protection remain unverified. SAI-B127 records the separate enforcement
work; do not treat policy prose as enforced permissions or invent an assistant
GitHub identity.

The assistant can review PRs during active sessions. It cannot continue monitoring
or merging after a session ends. Continuous monitoring would require separately
implemented, approved automation. No unattended monitor or auto-merger is enabled.
See the [full contribution workflow](docs/engineering/AI_CONTRIBUTION_WORKFLOW.md)
and [PR evidence contract](docs/engineering/PR_EVIDENCE.md).

## Keeping this handoff current

Sources: `docs/engineering/backlog/issues.json` owns task detail and completion;
`AnalyseFuture/repository-inventory/features.json` owns feature evidence/gaps;
review annotations under `AnalyseFuture/repository-inventory/reviews/` describe
file purposes; `docs/engineering/handoff-directories.json` describes folder
responsibilities. `PROJECT_STRUCTURE.md` is the shorter layout guide. Earlier
review annotations can describe baseline findings; the dated status/validation
ledgers establish later fixes and executed results.

Stage intended source/documentation first: the static inventory reads Git-index
blobs. Add annotations for new files and descriptions for new folders. Regenerate
task cards, then the root handoff, then the hash inventory after staging the
generated handoff. No application or archive code is executed by these generators.

```sh
python3 scripts/github/build_backlog.py --write
git add <the-specific-intended-files>
python3 -W ignore::SyntaxWarning scripts/verification/project_handoff.py --write
git add PROJECT_HANDOFF.md
python3 -W ignore::SyntaxWarning scripts/verification/repository_inventory.py --write
git add AnalyseFuture/repository-inventory/current-files.json AnalyseFuture/repository-inventory/COMPLETE_FILE_INVENTORY.txt
python3 scripts/github/build_backlog.py --check
python3 -W ignore::SyntaxWarning scripts/verification/project_handoff.py --check
python3 -W ignore::SyntaxWarning scripts/verification/repository_inventory.py --check
python3 scripts/verification/verify_preserved_archives.py --git-index
```

The full runtime gate for implementation changes is `npm run test:all` with the
required supported gVisor environment and browser dependencies. Use the
development guide for setup; never report a skipped integration run as a real
sandbox pass. Documentation-only maintenance uses its relevant static consistency
checks and clearly retains the revision of prior runtime evidence.

When issue API access is available, `python3 scripts/github/publish_issues.py
--publish` reconciles and publishes missing tasks using authorized existing
authentication. It records confirmed results and stops on ambiguous writes.
Regenerate task cards and this handoff after the receipt changes. Never paste
credentials into documentation, chat, issues or commits.
"""


def link(path: str, label: str | None = None) -> str:
    if not (ROOT / path).exists():
        return code(label or path) + " (proposed or historical reference)"
    return f"[{label or path}]({quote(path, safe='/.-_')})"


def cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def code(value: str) -> str:
    return f"`{cell(value).replace('`', '&#96;')}`"


def task_link(identifier: str) -> str:
    return f"[{identifier}](#{identifier.lower()})"


def bullets(lines: list[str]) -> list[str]:
    return [f"- {line}" for line in lines] or ["- None specified."]


def render() -> str:
    inventory, _ = build()
    files = inventory["files"]
    feature_catalog = json.loads(
        (ROOT / "AnalyseFuture/repository-inventory/features.json").read_text()
    )
    catalog = json.loads((ROOT / "docs/engineering/backlog/issues.json").read_text())
    tasks = sorted(catalog["issues"], key=lambda task: task["order"])
    receipt = json.loads((ROOT / "docs/engineering/backlog/publication.json").read_text())
    descriptions = json.loads(DIRECTORIES.read_text())["directories"]
    directories = {str(parent) for row in files for parent in PurePosixPath(row["path"]).parents}
    if set(descriptions) != directories:
        raise SystemExit(
            "Directory descriptions differ from tracked tree: "
            f"missing={sorted(directories - descriptions.keys())}; "
            f"stale={sorted(descriptions.keys() - directories)}"
        )
    counts = Counter(
        str(parent) for row in files for parent in PurePosixPath(row["path"]).parents
    )
    completed = sum(task.get("implementation_status") == "completed_locally" for task in tasks)
    lines = [INTRODUCTION.rstrip(), "", "## Feature register", ""]
    lines.extend([
        (f"Reviewed feature records: **{len(feature_catalog['features'])}**. "
         "The status below describes the feature, not whether every production "
         "hardening task is complete. An active workflow can still have recorded gaps."),
        "",
        "| Status | Meaning |", "| --- | --- |",
        "| Implemented locally | Active source workflow with recorded local evidence; production gaps can remain. |",
        "| Partial | Some supporting work exists; the complete workflow is blocked or unfinished. |",
        "| Planned | Feasible proposal; not an implemented product feature. |",
        "| Research only | Inactive upstream experiment or future investigation; not product integration. |", "",
    ])
    states = {
        "active": "Implemented locally", "partial": "Partial",
        "feasible_proposal": "Planned", "research_only": "Research only",
    }
    for feature in feature_catalog["features"]:
        lines.extend([
            f"### {feature['id']}: {feature['name']}", "",
            f"**Status:** {states[feature['status']]}. **Owner:** {feature['service']}.", "",
            feature["behavior"], "",
            "**Files / evidence:** " + "; ".join(link(path) for path in feature["files"]) + ".", "",
            "**Dependencies:** " + "; ".join(feature["dependencies"]) + ".", "",
            "**Recorded checks / references:** " + (
                "; ".join(code(t) for t in feature["tests"])
                or "None executed for this proposed capability"
            ) + ".", "",
            "**Remaining gaps / conditions:**", "", *bullets(feature["gaps"]), "",
        ])
    lines.extend([
        "## Complete folder map", "",
        (f"**{len(directories)} folders including the root**, derived from all "
         f"**{len(files)} tracked files**. Counts include nested descendants. "
         "Folders are functional owners; preserved upstream internal structure remains evidence."), "",
        "| Folder | Responsibility | Tracked files below it |", "| --- | --- | --- |",
    ])
    for directory in sorted(directories):
        lines.append(
            f"| {link(directory, directory + '/' if directory != '.' else './')} "
            f"| {cell(descriptions[directory])} | {counts[directory]} |"
        )
    lines.extend([
        "", ("Ignored local folders such as `.local/`, `.venv/`, `node_modules/`, "
        "`.next/`, generated `public/monaco/`, browser reports and caches are runtime, "
        "dependency or generated data. They are intentionally outside the tracked "
        "source catalogue. Private state must remain ignored; it is not copied into preservation."), "",
        "## Complete file map", "",
        (f"Every one of the **{len(files)} tracked paths** appears once below, grouped "
         "by its immediate owning folder. Each entry explains its reviewed role. "
         "The linked full inventory records direct imports/dependencies and provenance. "
         "Product task ownership is defined "
         "by the target paths in the complete task specifications."), "",
        ("The [full inventory](AnalyseFuture/repository-inventory/COMPLETE_FILE_INVENTORY.txt) "
        "also records baseline assessments, risks, review provenance, sizes and hashes. "
        "Preserved material is marked inactive below, even when its upstream code "
        "describes an implemented research experiment. Documentation and configuration "
        "support a feature; their existence alone does not implement the planned behavior."), "",
    ])
    for directory in sorted({str(PurePosixPath(row["path"]).parent) for row in files}):
        rows = [row for row in files if str(PurePosixPath(row["path"]).parent) == directory]
        lines.extend([
            "<details>", f"<summary>{directory}/ — {len(rows)} files</summary>", "",
            descriptions[directory], "",
            "| File | Purpose / feature |",
            "| --- | --- |",
        ])
        for row in rows:
            purpose = row["purpose"]
            state = "**Inactive preserved material.** " if not row["active"] else ""
            lines.append(
                f"| {link(row['path'], PurePosixPath(row['path']).name)} | {state}{cell(purpose)} "
                "|"
            )
        lines.extend(["", "</details>", ""])
    lines.extend([
        "## Ordered task index", "",
        (f"**{len(tasks)} detailed tasks: {len(tasks) - completed} pending, "
         f"{completed} completed locally.** Preserve stable IDs and use the execution "
         "order below. Completion requires observed acceptance/validation evidence; "
         "a task card or generated file is not completion."), "",
        (f"Actual GitHub publication receipt: **{receipt['status']}**; "
         f"**{len(receipt.get('issues', {}))}** confirmed remote issue links. "
         "Until access is restored, assign and reference these local cards."), "",
        "| Order | Task | State | Priority | Area / phase | Prerequisites |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for task in tasks:
        state = "Completed locally" if task.get("implementation_status") == "completed_locally" else "Pending"
        prerequisites = ", ".join(task_link(t) for t in task["depends_on"]) or "None"
        lines.append(
            f"| {task['order']} | {task_link(task['id'])}: {cell(task['title'])} "
            f"| {state} | {task['priority']} | {cell(task['area'])} / "
            f"{cell(task['phase'])} | {prerequisites} |"
        )
    lines.extend([
        "", "## Complete task specifications", "",
        ("All scope, acceptance, validation, exclusions and review risks from the "
        "canonical catalogue are included here. Expand a task to assign it. Target "
        "paths can name future files; they are ownership instructions rather than "
        "claims those files already exist. Owner roles suggest expertise, not actual "
        "assignees or granted permissions."), "",
    ])
    for task in tasks:
        identifier = task["id"]
        state = task.get("implementation_status", "pending")
        lines.extend([
            f'<a id="{identifier.lower()}"></a>', "<details>",
            f"<summary>{task['order']}. {identifier}: {task['title']} [{state}]</summary>", "",
            f"**Suggested role:** {task['owner_role']}.", "",
            "**Prerequisites:** " + (", ".join(task_link(t) for t in task["depends_on"]) or "None") + ".", "",
            "**Problem / missing behavior**", "", task["problem"], "",
            "**Target paths / responsibility**", "", *bullets([code(p) for p in task["target_paths"]]), "",
        ])
        for key, title in (
            ("scope", "Implementation scope"), ("acceptance", "Acceptance criteria"),
            ("validation", "Validation required"), ("out_of_scope", "Out of scope"),
        ):
            lines.extend([f"**{title}**", "", *bullets(task[key]), ""])
        lines.extend(["**Risk and review**", "", task["risk"], ""])
        if task.get("completion_evidence"):
            lines.extend([
                f"**Completion record ({task['completed_date']}):** " + task["completion_evidence"], "",
            ])
        lines.extend(["</details>", ""])
    lines.append(ENDING.rstrip())
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.write:
        OUTPUT.write_text(expected)
    elif not OUTPUT.exists() or OUTPUT.read_text() != expected:
        raise SystemExit("PROJECT_HANDOFF.md is stale; stage intended inputs and regenerate with --write.")
    print(f"Project handoff {'written' if args.write else 'verified'}; no network or runtime tests.")


if __name__ == "__main__":
    main()
