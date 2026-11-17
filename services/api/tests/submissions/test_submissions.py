"""Authenticated queue/ownership and fail-closed worker protocol checks; no code executes here."""

import os
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi.testclient import TestClient

from solver_api.features.identity import verification as auth
from solver_api.features.submissions.store import SubmissionRequest, get_store
from solver_api.main import app

WORKER_AUTH = {"Authorization": "Bearer test-worker-secret-long-enough"}


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setenv("SOLVER_DB_PATH", str(tmp_path / "state" / "attempts.sqlite3"))
    monkeypatch.setenv("JUDGE_WORKER_TOKEN", "test-worker-secret-long-enough")
    monkeypatch.setenv("AUTH_ISSUER", "http://127.0.0.1:3000")
    monkeypatch.setenv("AUTH_JWKS_URL", "http://127.0.0.1:3000/api/auth/jwks")
    auth.clear_auth_cache()
    private_key = Ed25519PrivateKey.generate()
    public_bytes = private_key.public_key().public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw,
    )

    async def fetch(_url):
        return {
            "keys": [
                {
                    "kid": "queue-key",
                    "kty": "OKP",
                    "crv": "Ed25519",
                    "alg": "EdDSA",
                    "x": jwt.utils.base64url_encode(public_bytes).decode(),
                }
            ]
        }

    monkeypatch.setattr(auth, "_fetch_jwks", fetch)

    def account_headers(user="user-a", key=None):
        now = int(time.time())
        token = jwt.encode(
            {
                "sub": user,
                "iat": now,
                "exp": now + 300,
                "iss": "http://127.0.0.1:3000",
                "aud": "solver-api",
                "token_use": "solver_api",
            },
            private_key,
            algorithm="EdDSA",
            headers={"kid": "queue-key"},
        )
        return {"Authorization": "Bearer " + token, "Idempotency-Key": key or str(uuid4())}

    with TestClient(app) as test_client:
        test_client.account_headers = account_headers
        yield test_client
    auth.clear_auth_cache()


def ready(client, worker="worker-a", languages=None):
    response = client.post(
        "/internal/judge/heartbeat",
        headers=WORKER_AUTH,
        json={
            "worker_id": worker,
            "runtime": "gvisor",
            "languages": languages or ["python", "cpp"],
        },
    )
    assert response.status_code == 200, response.text


def payload(**changes):
    return {
        "problem_slug": "signal-sum",
        "language": "python",
        "source_code": "print(sum(map(int, input().split())))",
        "mode": "submit",
        **changes,
    }


def submit(client, user="user-a", key=None, **changes):
    return client.post(
        "/api/v1/submissions", json=payload(**changes), headers=client.account_headers(user, key)
    )


def lease(client, worker="worker-a"):
    response = client.post("/internal/judge/lease", headers=WORKER_AUTH, json={"worker_id": worker})
    assert response.status_code == 200, response.text
    return response.json()["job"]


def finish(client, job, verdict="AC", worker="worker-a", **changes):
    return client.post(
        f"/internal/judge/jobs/{job['id']}/complete",
        headers=WORKER_AUTH,
        json={
            "worker_id": worker,
            "lease_token": job["lease_token"],
            "verdict": verdict,
            "summary": "private expected/output must not leak",
            **changes,
        },
    )


def test_capabilities_are_fail_closed_until_current_worker(client, monkeypatch):
    response = submit(client)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "JUDGE_UNAVAILABLE"
    assert client.get("/api/v1/capabilities").json()["judge_available"] is False
    ready(client)
    assert client.get("/api/v1/capabilities").json() == {
        "judge_available": True,
        "languages": ["cpp", "python"],
        "reason": None,
    }
    monkeypatch.delenv("JUDGE_WORKER_TOKEN")
    assert client.get("/api/v1/capabilities").json()["judge_available"] is False
    assert submit(client).status_code == 503


def test_expired_heartbeat_and_unsupported_language_reject_new_work(client):
    ready(client, languages=["python"])
    assert submit(client, language="cpp").status_code == 503
    with get_store().connect() as db:
        db.execute("UPDATE judge_workers SET heartbeat_at=?", (time.time() - 61,))
    assert submit(client).status_code == 503
    response = client.post(
        "/internal/judge/lease", headers=WORKER_AUTH, json={"worker_id": "worker-a"}
    )
    assert response.status_code == 409


@pytest.mark.parametrize("path", ["/api/v1/submissions", "/api/v1/submissions/not-a-job"])
def test_history_and_source_require_verified_identity(client, path):
    response = client.get(path, headers={"X-User-ID": "user-a"})
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_creation_persistence_history_and_ownership(client):
    ready(client)
    response = submit(client)
    assert response.status_code == 202
    job = response.json()
    assert job["status"] == "QUEUED"
    assert job["verdict"] is None
    assert job["source_code"] == payload()["source_code"]
    assert job["problem_title"] == "Signal Sum"
    assert not {"user_id", "lease_hash", "lease_token", "worker_id"} & job.keys()
    assert job["created_at"].endswith("Z")
    headers = client.account_headers()
    history = client.get("/api/v1/submissions", headers=headers).json()
    assert history["total"] == 1
    assert "source_code" not in history["items"][0]
    assert history["items"][0]["id"] == job["id"]
    assert client.get(f"/api/v1/submissions/{job['id']}", headers=headers).json() == job
    other = client.account_headers("user-b")
    assert client.get("/api/v1/submissions", headers=other).json()["total"] == 0
    assert client.get(f"/api/v1/submissions/{job['id']}", headers=other).status_code == 404
    # Reopen the same on-disk database through a separate SQLite connection.
    with sqlite3.connect(os.environ["SOLVER_DB_PATH"]) as db:
        assert (
            db.execute("SELECT source_code FROM submissions").fetchone()[0]
            == payload()["source_code"]
        )
    assert os.stat(os.environ["SOLVER_DB_PATH"]).st_mode & 0o777 == 0o600


def test_idempotency_retries_do_not_duplicate_or_require_online_worker(client):
    ready(client)
    key = str(uuid4())
    first = submit(client, key=key)
    assert first.status_code == 202
    retry = submit(client, key=key)
    assert retry.json() == first.json()
    with get_store().connect() as db:
        db.execute("DELETE FROM judge_workers")
    assert submit(client, key=key).json() == first.json()
    conflict = submit(client, key=key, source_code="print(0)")
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "IDEMPOTENCY_CONFLICT"
    assert client.get("/api/v1/submissions", headers=client.account_headers()).json()["total"] == 1


def test_idempotency_scope_and_one_active_per_user(client):
    ready(client)
    key = str(uuid4())
    first = submit(client, key=key)
    second = submit(client, user="user-b", key=key)
    assert first.status_code == second.status_code == 202
    assert first.json()["id"] != second.json()["id"]
    blocked = submit(client)
    assert blocked.status_code == 429
    assert blocked.json()["error"]["code"] == "SUBMISSION_IN_PROGRESS"
    assert blocked.headers["retry-after"] == "5"


@pytest.mark.parametrize("key", [None, "", "not-a-uuid", "x" * 1000])
def test_idempotency_key_is_required_and_bounded(client, key):
    ready(client)
    headers = client.account_headers()
    if key is None:
        headers.pop("Idempotency-Key")
    else:
        headers["Idempotency-Key"] = key
    response = client.post("/api/v1/submissions", json=payload(), headers=headers)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_IDEMPOTENCY_KEY"


@pytest.mark.parametrize(
    "changes",
    [
        {"source_code": ""},
        {"source_code": "x" * 32769},
        {"source_code": "€" * 10923},
        {"language": "bash"},
        {"mode": "contest"},
        {"problem_slug": "../secret"},
        {"unexpected": True},
    ],
)
def test_source_and_payload_validation(client, changes):
    ready(client)
    response = submit(client, **changes)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_REQUEST"


def test_missing_problem_is_not_queued(client):
    ready(client)
    response = submit(client, problem_slug="does-not-exist")
    assert response.status_code == 404
    assert client.get("/api/v1/submissions", headers=client.account_headers()).json()["total"] == 0


def test_request_body_limit_is_enforced_for_declared_and_streamed_bodies(client):
    headers = client.account_headers()
    declared = client.post("/api/v1/submissions", content="x" * 131073, headers=headers)
    assert declared.status_code == 413
    assert declared.json()["error"]["code"] == "REQUEST_TOO_LARGE"
    streamed = client.post(
        "/api/v1/submissions",
        content=iter([b"x" * 70000, b"y" * 70000]),
        headers={**headers, "Content-Type": "application/json"},
    )
    assert streamed.status_code == 413
    assert streamed.json()["request_id"] == streamed.headers["x-request-id"]


@pytest.mark.parametrize(
    "path,body",
    [
        (
            "/internal/judge/heartbeat",
            {"worker_id": "w", "runtime": "gvisor", "languages": ["python"]},
        ),
        ("/internal/judge/lease", {"worker_id": "w"}),
        (
            "/internal/judge/jobs/missing/complete",
            {"worker_id": "w", "lease_token": "x" * 43, "verdict": "AC"},
        ),
    ],
)
def test_worker_control_requires_dedicated_secret(client, path, body, monkeypatch):
    for headers in [{}, client.account_headers(), {"Authorization": "Bearer wrong"}]:
        response = client.post(path, json=body, headers=headers)
        assert response.status_code == 403
    monkeypatch.delenv("JUDGE_WORKER_TOKEN")
    assert client.post(path, json=body, headers=WORKER_AUTH).status_code == 403


def test_unreviewed_runtime_cannot_advertise_readiness(client):
    response = client.post(
        "/internal/judge/heartbeat",
        headers=WORKER_AUTH,
        json={"worker_id": "w", "runtime": "runc", "languages": ["python"]},
    )
    assert response.status_code == 422
    assert client.get("/api/v1/capabilities").json()["judge_available"] is False


def test_malformed_worker_headers_fail_closed_without_internal_error(client):
    body = {"worker_id": "worker-a"}
    for headers in [
        [(b"authorization", b"Bearer \xc3\xa9")],
        [(b"authorization", b"Bearer test-worker-secret-long-enough")] * 2,
    ]:
        response = client.post("/internal/judge/lease", json=body, headers=headers)
        assert response.status_code == 403
        assert response.json()["error"]["code"] == "WORKER_FORBIDDEN"


def test_only_one_worker_gets_each_lease_and_completion_is_one_shot(client):
    ready(client)
    ready(client, worker="worker-b")
    first = submit(client).json()
    job = lease(client)
    assert job["id"] == first["id"]
    assert job["source_code"] == payload()["source_code"]
    assert lease(client, worker="worker-b") is None
    status = client.get(f"/api/v1/submissions/{job['id']}", headers=client.account_headers()).json()
    assert status["status"] == "RUNNING"
    assert "lease_token" not in status
    assert finish(client, job, worker="worker-b").status_code == 409
    assert finish(client, job, lease_token="x" * 43).status_code == 409
    assert finish(client, job).status_code == 200
    assert finish(client, job).status_code == 409
    detail = client.get(f"/api/v1/submissions/{job['id']}", headers=client.account_headers()).json()
    assert detail["status"] == "FINISHED"
    assert detail["verdict"] == "AC"
    assert detail["summary"] == "All grading checks passed."
    assert detail["completed_at"] is not None
    assert "private expected/output" not in str(detail)


@pytest.mark.parametrize("verdict", ["AC", "WA", "CE", "RE", "TLE", "MLE", "OLE", "SYSTEM_ERROR"])
def test_worker_verdicts_are_stored_with_safe_summaries(client, verdict):
    ready(client)
    submit(client, mode="run")
    job = lease(client)
    assert finish(client, job, verdict=verdict).status_code == 200
    result = client.get(f"/api/v1/submissions/{job['id']}", headers=client.account_headers()).json()
    assert result["verdict"] == verdict
    assert result["summary"]
    assert "private expected/output" not in result["summary"]
    if verdict == "AC":
        assert result["summary"] == "All public samples passed."


def test_expired_lease_and_abandoned_queue_terminate_without_reexecution(client):
    ready(client)
    submit(client)
    job = lease(client)
    with get_store().connect() as db:
        db.execute("UPDATE submissions SET lease_expires_at=?", (time.time() - 1,))
    response = client.get(f"/api/v1/submissions/{job['id']}", headers=client.account_headers())
    assert response.json()["verdict"] == "SYSTEM_ERROR"
    assert finish(client, job).status_code == 409
    assert lease(client) is None
    queued = submit(client).json()
    with get_store().connect() as db:
        db.execute(
            "UPDATE submissions SET created_at=? WHERE id=?", (time.time() - 601, queued["id"])
        )
    result = client.get(
        f"/api/v1/submissions/{queued['id']}", headers=client.account_headers()
    ).json()
    assert result["status"] == "FINISHED"
    assert result["verdict"] == "SYSTEM_ERROR"
    assert lease(client) is None


def test_rate_limit_persists_across_completed_jobs(client):
    ready(client)
    for _ in range(10):
        assert submit(client).status_code == 202
        assert finish(client, lease(client)).status_code == 200
    response = submit(client)
    assert response.status_code == 429
    assert response.json()["error"]["code"] == "RATE_LIMITED"
    assert response.headers["retry-after"] == "60"
    assert submit(client, user="user-b").status_code == 202


def test_global_queue_bound_and_pagination(client):
    ready(client)
    store = get_store()
    for index in range(100):
        request = SubmissionRequest(**payload())
        store.create(f"queue-user-{index}", str(uuid4()), request, "Signal Sum")
    response = submit(client)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "QUEUE_FULL"
    page = client.get(
        "/api/v1/submissions?limit=1&offset=1", headers=client.account_headers("queue-user-0")
    ).json()
    assert page["total"] == 1
    assert page["items"] == []
    assert (
        client.get("/api/v1/submissions?limit=101", headers=client.account_headers()).status_code
        == 422
    )


def test_concurrent_idempotent_creates_are_atomic(client):
    ready(client)
    key = str(uuid4())
    store = get_store()
    request = SubmissionRequest(**payload())
    with ThreadPoolExecutor(max_workers=4) as executor:
        jobs = list(
            executor.map(
                lambda _: store.create("parallel-user", key, request, "Signal Sum"), range(8)
            )
        )
    assert len({job.id for job in jobs}) == 1
    assert store.list("parallel-user", 20, 0).total == 1


def test_concurrent_workers_do_not_duplicate_a_job(client):
    ready(client)
    for index in range(5):
        submit(client, user=f"user-{index}")
    store = get_store()
    with ThreadPoolExecutor(max_workers=4) as executor:
        jobs = list(executor.map(lambda _: store.lease("worker-a")["job"], range(8)))
    leased = [job["id"] for job in jobs if job]
    assert len(leased) == len(set(leased)) == 5
