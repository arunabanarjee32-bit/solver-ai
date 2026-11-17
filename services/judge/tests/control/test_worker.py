import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch
from uuid import uuid4

import pytest
from solver_judge.control.worker import (
    SUMMARIES,
    APIClient,
    APIError,
    Worker,
    validate_base_url,
    validate_job,
)


@pytest.fixture
def job():
    return {
        "id": uuid4().hex,
        "source_code": "print(7)",
        "language": "python",
        "problem_slug": "signal-sum",
        "mode": "submit",
        "lease_token": "lease-secret-" * 4,
        "lease_expires_at": "2026-11-13T20:00:00Z",
    }


class FakeClient:
    def __init__(self, job):
        self.job = job
        self.requests = []
        self.completion_failures = 0

    def post(self, path, body):
        self.requests.append((path, body))
        if path.endswith("/heartbeat"):
            return {"ok": True}
        if path.endswith("/lease"):
            return {"job": self.job}
        if self.completion_failures:
            self.completion_failures -= 1
            raise APIError("temporary failure")
        return {"ok": True}


class FakeRunner:
    def __init__(self, verdict="AC", failure=False):
        self.verdict = verdict
        self.failure = failure
        self.preflight_ran = False
        self.jobs = []
        self.cancel_ran = False
        self.ready = not failure

    def preflight(self):
        self.preflight_ran = True
        if self.failure:
            raise RuntimeError("runtime unavailable")
        self.ready = True

    def judge(self, job):
        self.jobs.append(job)
        return {
            "verdict": self.verdict,
            "summary": "private fixture output must never be exposed",
        }

    def cancel(self):
        self.cancel_ran = True
        self.ready = False


@pytest.mark.parametrize("verdict", list(SUMMARIES))
def test_completion_uses_only_closed_summary_vocabulary(job, verdict):
    client = FakeClient(job)
    runner = FakeRunner(verdict)
    worker = Worker(client, runner)
    assert worker.run_once()
    path, body = client.requests[-1]
    assert path == f"/internal/judge/jobs/{job['id']}/complete"
    assert body == {
        "worker_id": worker.worker_id,
        "lease_token": job["lease_token"],
        "verdict": verdict,
        "summary": SUMMARIES[verdict],
    }
    assert len(body["summary"].encode()) <= 512


def test_bad_runner_verdict_is_system_error(job):
    client = FakeClient(job)
    Worker(client, FakeRunner("invented")).run_once()
    assert client.requests[-1][1]["verdict"] == "SYSTEM_ERROR"


def test_runner_exception_is_sanitized(job, caplog):
    class BrokenRunner(FakeRunner):
        def judge(self, job):
            raise RuntimeError("private source and secret")

    client = FakeClient(job)
    Worker(client, BrokenRunner()).run_once()
    assert client.requests[-1][1]["verdict"] == "SYSTEM_ERROR"
    assert "private source" not in caplog.text


def test_empty_queue_never_invokes_runner():
    client = FakeClient(None)
    runner = FakeRunner()
    assert Worker(client, runner).run_once() is False
    assert runner.jobs == []


def test_completions_retry_same_lease_without_reexecution(job):
    client = FakeClient(job)
    client.completion_failures = 2
    runner = FakeRunner()
    stop = threading.Event()
    with patch.object(stop, "wait", return_value=False):
        assert Worker(client, runner, stop=stop).run_once()
    completions = [body for path, body in client.requests if path.endswith("/complete")]
    assert len(completions) == 3
    assert completions[0] == completions[1] == completions[2]
    assert runner.jobs == [job]


def test_failed_preflight_never_advertises_readiness(caplog):
    client = FakeClient(None)
    runner = FakeRunner(failure=True)
    with pytest.raises(RuntimeError):
        Worker(client, runner).run()
    assert client.requests == []
    assert "Sandbox preflight failed" in caplog.text
    assert "solver_judge.control.diagnostics" in caplog.text
    assert "runtime unavailable" not in caplog.text


def test_initial_heartbeat_retries_transport_without_repeating_preflight(monkeypatch):
    monkeypatch.setattr("solver_judge.control.worker.INITIAL_HEARTBEAT_DELAYS", (0, 0, 0, 0))
    stop = threading.Event()
    runner = FakeRunner()

    class StartingClient(FakeClient):
        def post(self, path, body):
            self.requests.append((path, body))
            assert runner.preflight_ran
            if len(self.requests) < 3:
                raise APIError("private detail")
            stop.set()
            return {"ok": True}

    client = StartingClient(None)
    Worker(client, runner, stop=stop).run()
    assert len(client.requests) == 3
    assert all(path.endswith("/heartbeat") for path, _ in client.requests)
    assert runner.cancel_ran


def test_initial_heartbeat_stops_after_five_failures(monkeypatch, caplog):
    monkeypatch.setattr("solver_judge.control.worker.INITIAL_HEARTBEAT_DELAYS", (0, 0, 0, 0))

    class UnavailableClient(FakeClient):
        def post(self, path, body):
            self.requests.append((path, body))
            raise APIError("private source or credential")

    client = UnavailableClient(None)
    runner = FakeRunner()
    with pytest.raises(APIError):
        Worker(client, runner).run()
    assert len(client.requests) == 5
    assert runner.cancel_ran
    assert "Initial API heartbeat failed" in caplog.text
    assert "private source" not in caplog.text


def test_shutdown_interrupts_initial_heartbeat_backoff():
    stop = threading.Event()

    class StoppingClient(FakeClient):
        def post(self, path, body):
            self.requests.append((path, body))
            stop.set()
            raise APIError("transport unavailable")

    client = StoppingClient(None)
    runner = FakeRunner()
    Worker(client, runner, stop=stop).run()
    assert len(client.requests) == 1
    assert runner.cancel_ran


def test_preflight_precedes_heartbeat_and_shutdown():
    stop = threading.Event()
    runner = FakeRunner()

    class CheckingClient(FakeClient):
        def post(self, path, body):
            assert runner.preflight_ran
            stop.set()
            return super().post(path, body)

    client = CheckingClient(None)
    Worker(client, runner, stop=stop).run()
    assert len(client.requests) == 1
    assert client.requests[0][0].endswith("/heartbeat")
    assert runner.cancel_ran


def test_heartbeat_continues_while_runner_is_busy(job, monkeypatch):
    monkeypatch.setattr("solver_judge.control.worker.HEARTBEAT_SECONDS", 0.01)
    stop = threading.Event()

    class BusyRunner(FakeRunner):
        def judge(self, job):
            time.sleep(0.06)
            stop.set()
            return super().judge(job)

    client = FakeClient(job)
    Worker(client, BusyRunner(), stop=stop).run()
    heartbeats = [body for path, body in client.requests if path.endswith("/heartbeat")]
    assert len(heartbeats) >= 2
    assert client.requests[-1][0].endswith("/complete")


def test_stop_cancels_active_runner_and_waits_for_cleanup(job):
    started = threading.Event()
    cancelled = threading.Event()

    class CancellableRunner(FakeRunner):
        def judge(self, job):
            started.set()
            assert cancelled.wait(timeout=2)
            return {"verdict": "SYSTEM_ERROR"}

        def cancel(self):
            super().cancel()
            cancelled.set()

    stop = threading.Event()
    runner = CancellableRunner()
    client = FakeClient(job)
    thread = threading.Thread(target=Worker(client, runner, stop=stop).run)
    thread.start()
    assert started.wait(timeout=2)
    stop.set()
    thread.join(timeout=3)
    assert not thread.is_alive()
    assert runner.cancel_ran
    assert client.requests[-1][1]["verdict"] == "SYSTEM_ERROR"


@pytest.mark.parametrize("unready", [False, True])
def test_stopped_or_unready_worker_does_not_claim_a_job(job, unready):
    runner = FakeRunner()
    client = FakeClient(job)
    worker = Worker(client, runner)
    if unready:
        runner.ready = False
    else:
        worker.stop.set()
    assert worker.run_once() is False
    assert worker.stop.is_set()
    assert client.requests == []
    assert runner.jobs == []


def test_unready_runner_stops_heartbeat_without_advertising(monkeypatch):
    monkeypatch.setattr("solver_judge.control.worker.HEARTBEAT_SECONDS", 0)
    runner = FakeRunner()
    runner.ready = False
    client = FakeClient(None)
    worker = Worker(client, runner)
    worker._heartbeat_loop()
    assert worker.stop.is_set()
    assert client.requests == []


def test_cleanup_failure_completes_inflight_job_then_stops(job, caplog):
    class CleanupFailureRunner(FakeRunner):
        def judge(self, job):
            self.jobs.append(job)
            self.ready = False
            return {"verdict": "SYSTEM_ERROR", "summary": "private source"}

        def cancel(self):
            super().cancel()
            raise RuntimeError("private daemon detail")

    runner = CleanupFailureRunner()
    client = FakeClient(job)
    worker = Worker(client, runner)
    worker.run()
    assert worker.stop.is_set()
    assert runner.cancel_ran
    assert runner.jobs == [job]
    assert [path for path, _ in client.requests] == [
        "/internal/judge/heartbeat",
        "/internal/judge/lease",
        f"/internal/judge/jobs/{job['id']}/complete",
    ]
    assert client.requests[-1][1]["verdict"] == "SYSTEM_ERROR"
    assert client.requests[-1][1]["summary"] == SUMMARIES["SYSTEM_ERROR"]
    assert "private" not in caplog.text


def test_readiness_revoked_during_lease_does_not_execute_job(job):
    runner = FakeRunner()

    class RevokingClient(FakeClient):
        def post(self, path, body):
            if path.endswith("/lease"):
                runner.ready = False
            return super().post(path, body)

    client = RevokingClient(job)
    worker = Worker(client, runner)
    assert worker.run_once()
    assert worker.stop.is_set()
    assert runner.jobs == []
    assert client.requests[-1][1]["verdict"] == "SYSTEM_ERROR"


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "http://example.org",
        "https://user:pass@example.org",
        "https://host/path",
        "https://host?query=1",
        "https://host#secret",
        "http://127.0.0.1:99999",
        "https:///missing",
    ],
)
def test_untrusted_api_origins_are_rejected(url):
    with pytest.raises(ValueError):
        validate_base_url(url)


@pytest.mark.parametrize(
    "url", ["http://127.0.0.1:8000", "http://[::1]:8000/", "https://judge.example"]
)
def test_permitted_origins(url):
    assert validate_base_url(url) == url.rstrip("/")


@pytest.mark.parametrize(
    "token", ["", "short", "x" * 31, "x" * 257, "x" * 32 + "\n", "x" * 32 + " "]
)
def test_bad_worker_token_rejected(token):
    with pytest.raises(ValueError):
        APIClient("http://127.0.0.1:8000", token)


@pytest.mark.parametrize(
    "key,value",
    [
        ("source_code", "x" * 32769),
        ("source_code", "é" * 16385),
        ("source_code", ""),
        ("language", "shell"),
        ("mode", "exec"),
        ("id", "../elsewhere"),
        ("problem_slug", "unknown"),
        ("lease_token", "short"),
    ],
)
def test_invalid_leased_job_rejected(job, key, value):
    job[key] = value
    with pytest.raises(APIError):
        validate_job(job)


@pytest.fixture
def server():
    requests = []
    response = {"status": 200, "body": b'{"ok": true}'}

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            requests.append(
                (
                    self.path,
                    self.headers.get("Authorization"),
                    self.rfile.read(int(self.headers["Content-Length"])),
                )
            )
            self.send_response(response["status"])
            if response["status"] == 302:
                self.send_header("Location", "/redirect-destination")
            self.end_headers()
            self.wfile.write(response["body"])

        def log_message(self, *_args):
            pass

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_port}", requests, response
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def test_client_bearer_post_and_bounded_json(server):
    base, requests, _response = server
    assert APIClient(base, "x" * 32).post(
        "/internal/judge/heartbeat", {"worker_id": "w"}
    ) == {"ok": True}
    assert requests[0][0:2] == ("/internal/judge/heartbeat", "Bearer " + "x" * 32)
    assert json.loads(requests[0][2]) == {"worker_id": "w"}


@pytest.mark.parametrize("body", [b"x" * (512 * 1024 + 1), b"not json", b"[]"])
def test_client_rejects_unbounded_or_invalid_response(server, body):
    base, _requests, response = server
    response["body"] = body
    with pytest.raises(APIError):
        APIClient(base, "x" * 32).post("/internal/judge/lease", {})


def test_escaped_maximum_source_fits_response_limit(server):
    base, _requests, response = server
    expected = {"job": {"source_code": "\0" * 32768}}
    response["body"] = json.dumps(expected).encode()
    assert APIClient(base, "x" * 32).post("/internal/judge/lease", {}) == expected


def test_redirect_is_not_followed_with_bearer(server):
    base, requests, response = server
    response["status"] = 302
    with pytest.raises(APIError):
        APIClient(base, "x" * 32).post("/internal/judge/lease", {})
    assert len(requests) == 1
