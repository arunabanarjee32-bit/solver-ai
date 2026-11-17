"""Publication safety checks use a fake GitHub client, never the network."""

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "solver_issue_publisher", ROOT / "scripts/github/publish_issues.py"
)
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)
REPOSITORY = "arunabanarjee32-bit/solver-ai"


@pytest.fixture
def catalog():
    return {
        "repository": REPOSITORY,
        "issues": [
            {
                "id": f"SAI-B{order:03d}", "order": order, "title": f"Fixture task {order}",
                "area": "fixtures", "priority": "P1", "phase": "fixture phase",
                "depends_on": [] if order == 1 else ["SAI-B001"],
                "target_paths": ["README.md"], "problem": "Fixture problem",
                "scope": ["Fixture bounded change"], "acceptance": ["Fixture outcome"],
                "validation": ["Fixture check"], "out_of_scope": ["Production publication"],
                "risk": "No real request", "owner_role": "Fixture reviewer",
            }
            for order in range(1, 102)
        ],
    }


def remote_issue(issue, number):
    return {
        "number": number, "html_url": f"https://github.com/{REPOSITORY}/issues/{number}",
        "title": publisher.issue_title(issue), "body": publisher.render_body(issue, {}),
        "state": "open",
    }


class FakeGitHub:
    def __init__(self, issues, *, fail_post=False, repository=REPOSITORY):
        self.rows = [remote_issue(issue, number) for number, issue in enumerate(issues, 1)]
        self.posts = []
        self.fail_post = fail_post
        self.repository = repository

    def request(self, endpoint, payload=None, *, pages=False):
        if payload is not None:
            self.posts.append(payload)
            if self.fail_post:
                raise publisher.PublicationError("Ambiguous interrupted POST")
            number = 500 + len(self.posts)
            row = {
                **payload, "number": number, "state": "open",
                "html_url": f"https://github.com/{REPOSITORY}/issues/{number}",
            }
            self.rows.append(row)
            return row
        if pages:
            return [self.rows]
        return {"full_name": self.repository, "has_issues": True}


@pytest.mark.parametrize("invalid", ["later_dependency", "duplicate_identifier", "outside_path"])
def test_invalid_plan_is_rejected_before_any_remote_mutation(catalog, invalid, tmp_path):
    if invalid == "later_dependency":
        catalog["issues"][0]["depends_on"] = ["SAI-B101"]
    elif invalid == "duplicate_identifier":
        catalog["issues"][1]["id"] = "SAI-B001"
    else:
        catalog["issues"][0]["target_paths"] = ["../../outside-checkout"]
    client = FakeGitHub([])
    with pytest.raises(publisher.PublicationError):
        publisher.publish(catalog, client, tmp_path / "receipt.json", "fixture-digest")
    assert client.posts == []


def test_offline_default_never_contacts_github(catalog, tmp_path, monkeypatch, capsys):
    source = tmp_path / "issues.json"
    receipt = tmp_path / "receipt.json"
    source.write_text(json.dumps(catalog))
    monkeypatch.setattr(sys, "argv", ["publisher", "--catalog", str(source), "--receipt", str(receipt)])

    def forbidden(*args, **kwargs):
        raise AssertionError("Offline mode must never contact GitHub")

    monkeypatch.setattr(publisher.GitHub, "request", forbidden)
    publisher.main()
    assert "no GitHub requests" in capsys.readouterr().out
    assert not receipt.exists()


def test_remote_markers_recover_an_interrupted_receipt_without_duplicates(catalog, tmp_path):
    client = FakeGitHub(catalog["issues"][:-1])
    receipt_path = tmp_path / "receipt.json"
    receipt = publisher.publish(catalog, client, receipt_path, "fixture-digest")
    assert len(client.posts) == 1
    assert "https://github.com/" + REPOSITORY + "/issues/1" in client.posts[0]["body"]
    assert receipt["issues"]["SAI-B101"]["number"] == 501
    receipt_path.unlink()  # Simulate losing only this test's local receipt.
    repeated = publisher.publish(catalog, client, receipt_path, "fixture-digest")
    assert len(client.posts) == 1
    assert repeated["status"] == "published"
    assert len(repeated["issues"]) == 101


def test_duplicate_remote_marker_stops_before_creating_more_issues(catalog, tmp_path):
    client = FakeGitHub(catalog["issues"][:1])
    client.rows.append(remote_issue(catalog["issues"][0], 900))
    with pytest.raises(publisher.PublicationError, match="Duplicate remote"):
        publisher.publish(catalog, client, tmp_path / "receipt.json", "fixture-digest")
    assert client.posts == []


def test_existing_issue_title_conflict_is_not_overwritten(catalog, tmp_path):
    client = FakeGitHub(catalog["issues"][:1])
    client.rows[0]["title"] = "[SAI-B001] A maintainer changed this scope"
    with pytest.raises(publisher.PublicationError, match="another title"):
        publisher.publish(catalog, client, tmp_path / "receipt.json", "fixture-digest")
    assert client.posts == []


def test_preexisting_bare_title_is_reused_without_duplicate_or_body_edit(catalog, tmp_path):
    client = FakeGitHub(catalog["issues"])
    client.rows[0]["title"] = catalog["issues"][0]["title"]
    client.rows[0]["body"] = "Existing maintainer content; leave this unchanged."
    receipt = publisher.publish(catalog, client, tmp_path / "receipt.json", "fixture-digest")
    assert client.posts == []
    assert receipt["issues"]["SAI-B001"]["number"] == 1
    assert client.rows[0]["body"] == "Existing maintainer content; leave this unchanged."


def test_uncertain_post_is_not_retried_and_confirmed_progress_is_saved(catalog, tmp_path):
    client = FakeGitHub(catalog["issues"][:-1], fail_post=True)
    receipt_path = tmp_path / "receipt.json"
    with pytest.raises(publisher.PublicationError, match="interrupted POST"):
        publisher.publish(catalog, client, receipt_path, "fixture-digest")
    receipt = json.loads(receipt_path.read_text())
    assert len(client.posts) == 1
    assert receipt["status"] == "blocked_or_interrupted"
    assert len(receipt["issues"]) == 100


def test_wrong_repository_response_prevents_publication(catalog, tmp_path):
    client = FakeGitHub([], repository="someone/another-project")
    with pytest.raises(publisher.PublicationError, match="identity"):
        publisher.publish(catalog, client, tmp_path / "receipt.json", "fixture-digest")
    assert client.posts == []


def test_locally_completed_tasks_are_not_opened_as_new_issues(catalog, tmp_path):
    catalog["issues"][-1]["implementation_status"] = "completed_locally"
    catalog["issues"][-1]["completion_evidence"] = "Implementation and scoped regressions are committed."
    client = FakeGitHub(catalog["issues"][:-1])
    receipt = publisher.publish(catalog, client, tmp_path / "receipt.json", "fixture-digest")
    assert client.posts == []
    assert len(receipt["issues"]) == 100
    assert "SAI-B101" in receipt["skipped_completed"]


def test_completed_prerequisite_links_to_its_card_instead_of_reopening_it(catalog, tmp_path):
    catalog["issues"][0]["implementation_status"] = "completed_locally"
    catalog["issues"][0]["completion_evidence"] = "Reviewed implementation and regressions are committed."
    client = FakeGitHub(catalog["issues"][1:-1])
    receipt = publisher.publish(catalog, client, tmp_path / "receipt.json", "fixture-digest")
    assert len(client.posts) == 1
    assert "SAI-B001 (completed locally)" in client.posts[0]["body"]
    assert "/backlog/issues/SAI-B001.md" in client.posts[0]["body"]
    assert "SAI-B001" not in receipt["issues"]


def test_real_client_paces_posts_without_retrying_mutations(monkeypatch):
    calls = []
    sleeps = []
    clock = iter([0.0, 0.1, 1.1])

    def response(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=0, stdout="{}")

    monkeypatch.setattr(publisher.subprocess, "run", response)
    monkeypatch.setattr(publisher.time, "monotonic", lambda: next(clock))
    monkeypatch.setattr(publisher.time, "sleep", sleeps.append)
    client = publisher.GitHub()
    client.request("repos/fixture/project/issues", {"title": "one"})
    client.request("repos/fixture/project/issues", {"title": "two"})
    assert len(calls) == 2
    assert sleeps == [pytest.approx(1.0)]
