"""Evidence validation remains offline and treats contributor content as data."""

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "solver_pr_evidence", ROOT / "scripts/github/check_pr_evidence.py"
)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)
HEAD = "a" * 40
CATALOG = {"issues": [
    {"id": "SAI-B001", "order": 1, "depends_on": []},
    {"id": "SAI-B127", "order": 2, "depends_on": ["SAI-B001"]},
]}


@pytest.fixture
def evidence():
    return {
        "schema_version": 1, "backlog_id": "SAI-B127", "execution_order": 2,
        "head_revision": HEAD,
        "prerequisites": [{
            "id": "SAI-B001", "status": "completed", "evidence": "Reviewed commit evidence is linked.",
        }],
        "before": "Review rules are not enforced yet.",
        "after": "Owner-approved review rules are recorded.",
        "changed_paths": ["docs/engineering/new-proposed-file.md"],
        "checks": [{"command": "python3 checker.py", "outcome": "passed", "evidence": "All scoped fixtures passed."}],
        "security_data_impact": "No credentials, accounts or private data changed.",
        "rollback": "Revert the rules change after owner review.",
        "limitations": "Real hosted permissions still require owner verification.",
        "review_requested": True,
    }


def body(value):
    return "PR explanation.\n\n```solver-ai-evidence\n" + json.dumps(value) + "\n```\n"


def test_complete_evidence_uses_catalog_order_not_identifier_suffix(evidence):
    assert checker.validate(body(evidence), HEAD, CATALOG) == []


@pytest.mark.parametrize("outcome", ["failed", "skipped", "not-run", "expected-failure"])
def test_honest_nonpassing_outcomes_are_allowed_with_explanation(evidence, outcome):
    evidence["checks"][0] = {
        "command": "npm run test:all", "outcome": outcome,
        "evidence": "Owner paused execution for this scoped documentation change.",
    }
    assert checker.validate(body(evidence), HEAD, CATALOG) == []


@pytest.mark.parametrize("field,value", [
    ("backlog_id", "SAI-B999"), ("backlog_id", []),
    ("execution_order", 127), ("execution_order", True),
    ("head_revision", "b" * 40), ("schema_version", True),
    ("review_requested", False), ("before", "TODO"),
    ("changed_paths", []), ("checks", []), ("prerequisites", []),
])
def test_invalid_or_stale_fields_fail(evidence, field, value):
    evidence[field] = value
    assert checker.validate(body(evidence), HEAD, CATALOG)


@pytest.mark.parametrize("path", ["../outside", "/etc/passwd", "C:\\private", "docs/../secret", "x\nfile", "docs//file"])
def test_traversal_absolute_or_control_paths_fail(evidence, path):
    evidence["changed_paths"] = [path]
    assert any(error.startswith("changed_paths:") for error in checker.validate(body(evidence), HEAD, CATALOG))


@pytest.mark.parametrize("value", [None, "", "```solver-ai-evidence\nnot JSON\n```\n", "x" * 65537])
def test_missing_malformed_or_oversized_body_fails(value):
    assert checker.validate(value, HEAD, CATALOG)


def test_duplicate_blocks_and_duplicate_json_keys_fail(evidence):
    assert checker.validate(body(evidence) + body(evidence), HEAD, CATALOG)
    duplicated = body(evidence).replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1')
    assert checker.validate(duplicated, HEAD, CATALOG)


def test_second_unclosed_evidence_block_is_not_silently_ignored(evidence):
    assert checker.validate(body(evidence) + "\n```solver-ai-evidence\n", HEAD, CATALOG)


def test_placeholder_results_and_malformed_nested_types_fail(evidence):
    for field, bad_value in [("outcome", []), ("evidence", ""), ("command", "TODO")]:
        changed = copy.deepcopy(evidence)
        changed["checks"][0][field] = bad_value
        assert checker.validate(body(changed), HEAD, CATALOG)
    evidence["prerequisites"][0]["status"] = []
    assert checker.validate(body(evidence), HEAD, CATALOG)


def test_duplicate_or_extra_prerequisites_fail(evidence):
    evidence["prerequisites"] *= 2
    assert checker.validate(body(evidence), HEAD, CATALOG)


def test_event_head_is_authoritative_after_synchronize(evidence):
    assert any(error.startswith("head_revision:") for error in checker.validate(body(evidence), "b" * 40, CATALOG))


def test_body_commands_are_not_executed_or_echoed(evidence, tmp_path, monkeypatch, capsys):
    sentinel = "PRIVATE_SENTINEL_MUST_NOT_BE_LOGGED"
    target = tmp_path / "must-not-exist"
    evidence["checks"][0]["command"] = f"$(touch {target}); ::error::{sentinel}"
    event_path, catalog_path = tmp_path / "event.json", tmp_path / "catalog.json"
    event_path.write_text(json.dumps({"pull_request": {"body": body(evidence), "head": {"sha": HEAD}}}))
    catalog_path.write_text(json.dumps(CATALOG))
    monkeypatch.setattr(sys, "argv", ["checker", "--event", str(event_path), "--catalog", str(catalog_path)])
    assert checker.main() == 0
    assert not target.exists()
    output = capsys.readouterr().out
    assert sentinel not in output and "::error::" not in output
    assert "does not verify tests or approve" in output


def test_unreadable_or_oversized_event_fails_with_fixed_diagnostic(tmp_path, monkeypatch, capsys):
    event = tmp_path / "event.json"
    event.write_bytes(b" " * (checker.MAX_EVENT_BYTES + 1))
    monkeypatch.setattr(sys, "argv", ["checker", "--event", str(event)])
    assert checker.main() == 1
    assert str(tmp_path) not in capsys.readouterr().out


def test_unknown_fields_and_non_json_numbers_are_rejected(evidence):
    evidence["execute"] = "This unsupported field must remain inert."
    assert checker.validate(body(evidence), HEAD, CATALOG)
    del evidence["execute"]
    invalid_json = body(evidence).replace('"schema_version": 1', '"schema_version": NaN')
    assert checker.validate(invalid_json, HEAD, CATALOG)


@pytest.mark.parametrize("pr", [None, [], "not a mapping"])
def test_malformed_nested_events_fail_without_traceback_or_payload_echo(pr, tmp_path, monkeypatch, capsys):
    event_path = tmp_path / "event.json"
    event_path.write_text(json.dumps({"pull_request": pr}))
    monkeypatch.setattr(sys, "argv", ["checker", "--event", str(event_path)])
    assert checker.main() == 1
    assert "input: PR event or trusted catalogue" in capsys.readouterr().out
