# Pull-request evidence contract

SAI-B001 adds a metadata-only check for contributor PRs. It establishes that
required evidence fields are present and refer to the current PR head. It cannot
establish that a test command was executed, prove correctness, approve code or
authorize a merge. Human/assistant review and the separate application checks
remain required.

The [PR template](../../.github/PULL_REQUEST_TEMPLATE.md) contains one fenced
`solver-ai-evidence` JSON block. Fill its fields; unchanged template placeholders
fail. Use the stable task ID and the **Order** column in the
[canonical backlog](backlog/README.md), not the identifier's numeric suffix.

## Required version-1 fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer `1`; booleans and unknown versions fail. |
| `backlog_id` | One known `SAI-Bnnn` identifier from the trusted base catalogue. |
| `execution_order` | That task's integer catalogue order. |
| `head_revision` | Exact current `pull_request.head.sha`, refreshed after new commits. |
| `prerequisites` | Every required dependency exactly once: `id`, `status`, `evidence`. |
| `before`, `after` | Concrete observed problem and resulting behavior. |
| `changed_paths` | Unique POSIX repository-relative file paths; proposed files allowed. |
| `checks` | At least one record containing `command`, `outcome`, `evidence`. |
| `security_data_impact` | Auth, ownership, data, dependencies and execution impact. |
| `rollback`, `limitations` | Recovery path and remaining uncertainty. |
| `review_requested` | Boolean `true`; contributor requests review and does not self-merge. |

Check outcomes are `passed`, `failed`, `skipped`, `not-run` or `expected-failure`.
Failed/skipped/unrun results are allowed with concrete evidence or a reason;
metadata must never force a false passing claim. Merge readiness is assessed by
the reviewer and the actual required checks, not by this field alone.

Prerequisite states are `completed`, `blocked`, `not-completed`, `not-run` or
`waived`. Evidence must explain the state; a claimed waiver is not proof of owner
approval. All dependencies must be accounted for even when the work is blocked.

Concrete text fields require 8–4,000 non-placeholder characters; command strings
allow 3–1,000. The body is capped at 64 KiB, with up to 64 check records, 128
prerequisites and 256 declared paths. Duplicate JSON keys/blocks, unknown fields,
absolute/traversing paths and stale head revisions fail. Paths and commands remain
inert data: the checker never imports PR code or executes any submitted command.

## CI and local use

`.github/workflows/pr-evidence.yml` runs on PR open, body edit, reopen, head
synchronization and ready-for-review events. It checks out the event's **base
commit**, disables persisted checkout credentials, and runs a stdlib-only parser
with `contents: read`. It reads body/head from the runner event JSON; PR body text
is never interpolated into shell commands or echoed into logs. It uses no secrets,
GitHub API writes, approval or merge operation.

```sh
python3 scripts/github/check_pr_evidence.py --event /path/to/pr-event.json
uv run --project services/api --frozen pytest tests/tooling/github/test_pr_evidence.py
```

The checker and catalogue must already exist on the trusted base. They are
installed through the owner's current direct-main maintenance authorization;
bootstrap must not silently fall back to executing PR-head code. A successful
local event fixture is not evidence of a hosted Actions run.

GitHub workflow changes still need substantive review. Server-side rules and
designated reviewer identities are separate SAI-B127 work; this metadata check
is not a tamper-proof branch-protection system. Apply it to all contributors
without trying to classify authorship as human or AI.
