"""Trusted local control worker. Learner programs run only through SandboxRunner."""

from __future__ import annotations

import ipaddress
import json
import logging
import os
import signal
import threading
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Protocol
from uuid import UUID, uuid4

LOG = logging.getLogger("solver_judge.control.worker")
# A 32 KiB source can expand sixfold when JSON escapes control characters.
MAX_RESPONSE_BYTES = 512 * 1024
HEARTBEAT_SECONDS = 15
POLL_SECONDS = 1
INITIAL_HEARTBEAT_DELAYS = (0.5, 1, 2, 3)
SUMMARIES = {
    "AC": "All configured checks passed.",
    "WA": "The output did not match the expected result.",
    "CE": "The program could not be compiled.",
    "RE": "The program stopped with a runtime error.",
    "TLE": "The program exceeded the execution time limit.",
    "MLE": "The program exceeded the configured memory limit.",
    "OLE": "The program exceeded the output limit.",
    "SYSTEM_ERROR": "The isolated judge could not complete this job.",
}


class APIError(RuntimeError):
    """Deliberately excludes response bodies, tokens and submitted source."""


class Runner(Protocol):
    ready: bool

    def preflight(self) -> Any: ...

    def judge(self, job: dict[str, Any]) -> dict[str, str]: ...

    def cancel(self) -> None: ...


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Never forward the worker bearer credential to a redirect target."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validate_base_url(url: str) -> str:
    try:
        parsed = urllib.parse.urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        raise ValueError("JUDGE_API_URL is invalid") from exc
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or parsed.path not in {"", "/"}
        or (port is not None and not 1 <= port <= 65535)
    ):
        raise ValueError("JUDGE_API_URL must be an HTTP(S) origin without credentials")
    if parsed.scheme == "http":
        try:
            loopback = ipaddress.ip_address(parsed.hostname).is_loopback
        except ValueError:
            loopback = parsed.hostname == "localhost"
        if not loopback:
            raise ValueError("Use HTTPS for a judge API outside loopback")
    return url.rstrip("/")


class APIClient:
    def __init__(self, base_url: str, token: str, timeout: float = 5):
        self.base_url = validate_base_url(base_url)
        if not 32 <= len(token) <= 256 or any(
            ord(c) < 33 or ord(c) > 126 for c in token
        ):
            raise ValueError(
                "JUDGE_WORKER_TOKEN must contain 32–256 printable non-space characters"
            )
        self._token = token
        self.timeout = timeout
        self._opener = urllib.request.build_opener(NoRedirect())

    def post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        if not path.startswith("/internal/judge/") or "?" in path or "#" in path:
            raise ValueError("Invalid internal judge path")
        payload = json.dumps(body, separators=(",", ":")).encode()
        request = urllib.request.Request(
            self.base_url + path,
            data=payload,
            method="POST",
            headers={
                "Authorization": "Bearer " + self._token,
                "Content-Type": "application/json",
            },
        )
        try:
            with self._opener.open(request, timeout=self.timeout) as response:
                data = response.read(MAX_RESPONSE_BYTES + 1)
        except urllib.error.HTTPError as exc:
            exc.close()
            raise APIError("Judge API request failed") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise APIError("Judge API request failed") from exc
        if len(data) > MAX_RESPONSE_BYTES:
            raise APIError("Judge API response exceeded its limit")
        try:
            result = json.loads(data)
        except (ValueError, UnicodeError) as exc:
            raise APIError("Judge API returned invalid JSON") from exc
        if not isinstance(result, dict):
            raise APIError("Judge API returned an invalid response")
        return result


def validate_job(job: Any) -> dict[str, Any]:
    if not isinstance(job, dict):
        raise APIError("Invalid job lease")
    try:
        UUID(job["id"])
        source = job["source_code"]
        lease = job["lease_token"]
        if (
            job["language"] not in {"python", "cpp"}
            or job["mode"] not in {"run", "submit"}
            or job["problem_slug"]
            not in {"signal-sum", "steady-climb", "distinct-stations"}
            or not isinstance(source, str)
            or not 1 <= len(source.encode()) <= 32768
            or not isinstance(lease, str)
            or not 16 <= len(lease) <= 256
        ):
            raise ValueError("Invalid lease data")
    except (KeyError, TypeError, ValueError, AttributeError, UnicodeError) as exc:
        raise APIError("Invalid job lease") from exc
    return job


class Worker:
    def __init__(
        self,
        client: APIClient,
        runner: Runner,
        *,
        stop: threading.Event | None = None,
        worker_id: str | None = None,
    ):
        self.client = client
        self.runner = runner
        self.stop = stop if stop is not None else threading.Event()
        self.worker_id = worker_id or uuid4().hex

    def heartbeat(self) -> None:
        if self.stop.is_set() or not self.runner.ready:
            self.stop.set()
            raise APIError("Sandbox readiness is unavailable")
        result = self.client.post(
            "/internal/judge/heartbeat",
            {
                "worker_id": self.worker_id,
                "runtime": "gvisor",
                "languages": ["python", "cpp"],
            },
        )
        if result.get("ok") is not True:
            raise APIError("Judge heartbeat was not accepted")

    def _heartbeat_loop(self) -> None:
        while not self.stop.wait(HEARTBEAT_SECONDS):
            try:
                self.heartbeat()
            except APIError:
                if self.stop.is_set():
                    return
                LOG.warning(
                    "Judge heartbeat failed; readiness will expire unless restored"
                )

    def _initial_heartbeat(self) -> bool:
        for attempt in range(len(INITIAL_HEARTBEAT_DELAYS) + 1):
            try:
                self.heartbeat()
                return True
            except APIError:
                if attempt == len(INITIAL_HEARTBEAT_DELAYS):
                    LOG.error(
                        "Initial API heartbeat failed; verify the API is running and the worker token matches"
                    )
                    raise
                LOG.warning(
                    "Initial API heartbeat unavailable; retrying startup transport"
                )
                if self.stop.wait(INITIAL_HEARTBEAT_DELAYS[attempt]):
                    return False
        return False

    def _cancel_when_stopped(self) -> None:
        self.stop.wait()
        try:
            self.runner.cancel()
        except Exception:  # noqa: BLE001 -- do not expose runner or Docker exception details
            LOG.error("Sandbox cancellation failed; inspect the local worker runtime")

    def run_once(self) -> bool:
        if self.stop.is_set() or not self.runner.ready:
            self.stop.set()
            return False
        leased = self.client.post(
            "/internal/judge/lease", {"worker_id": self.worker_id}
        )
        if not self.runner.ready:
            self.stop.set()
        if leased.get("job") is None:
            return False
        job = validate_job(leased["job"])
        try:
            if self.stop.is_set():
                verdict = "SYSTEM_ERROR"
            else:
                result = self.runner.judge(job)
                verdict = result.get("verdict", "SYSTEM_ERROR")
                if verdict not in SUMMARIES:
                    verdict = "SYSTEM_ERROR"
        except Exception:  # noqa: BLE001 -- fail closed without leaking runner exception details
            # Never log exception details: a runner failure could contain source or private output.
            LOG.error("Isolated judge failed; reporting SYSTEM_ERROR")
            verdict = "SYSTEM_ERROR"
        if not self.runner.ready:
            LOG.error("Sandbox readiness was revoked; stopping worker")
            self.stop.set()
        completion = {
            "worker_id": self.worker_id,
            "lease_token": job["lease_token"],
            "verdict": verdict,
            # Use a closed vocabulary; runner output and diagnostics never reach the API.
            "summary": SUMMARIES[verdict],
        }
        for attempt in range(3):
            try:
                result = self.client.post(
                    f"/internal/judge/jobs/{job['id']}/complete", completion
                )
                if result.get("ok") is not True:
                    raise APIError("Completion was not accepted")
                return True
            except APIError:
                if attempt == 2:
                    raise
                self.stop.wait(0.5 * (2**attempt))
        return True

    def run(self) -> None:
        # Cleanup runs outside Python's signal handler, including during preflight.
        cancellation = threading.Thread(
            target=self._cancel_when_stopped, name="judge-cancellation", daemon=True
        )
        cancellation.start()
        heartbeat = None
        try:
            try:
                self.runner.preflight()
            except Exception as exc:
                LOG.error(
                    "Sandbox preflight failed; run python3 -m solver_judge.control.diagnostics"
                )
                raise RuntimeError("Sandbox preflight failed") from exc
            if self.stop.is_set():
                return
            if not self._initial_heartbeat() or self.stop.is_set():
                return
            heartbeat = threading.Thread(
                target=self._heartbeat_loop, name="judge-heartbeat", daemon=True
            )
            heartbeat.start()
            LOG.info("Isolated judge preflight passed; worker is ready")
            while not self.stop.is_set():
                try:
                    worked = self.run_once()
                    if not worked:
                        self.stop.wait(POLL_SECONDS)
                except APIError:
                    LOG.warning(
                        "Judge API transport failed; retrying while jobs remain tracked by the API"
                    )
                    self.stop.wait(2)
        finally:
            self.stop.set()
            cancellation.join(timeout=8)
            if heartbeat is not None:
                heartbeat.join(timeout=6)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        client = APIClient(
            os.environ.get("JUDGE_API_URL", "http://127.0.0.1:8000"),
            os.environ.get("JUDGE_WORKER_TOKEN", ""),
        )
    except ValueError:
        LOG.error(
            "Worker configuration invalid; check JUDGE_API_URL and JUDGE_WORKER_TOKEN"
        )
        return 1
    try:
        from solver_judge.control.runner import SandboxRunner

        runner = SandboxRunner(
            image=os.environ.get("JUDGE_SANDBOX_IMAGE", "solver-ai-sandbox:local")
        )
    except (ImportError, ValueError, RuntimeError, OSError):
        LOG.error("Sandbox runner unavailable; run python3 -m solver_judge.control.diagnostics")
        return 1
    try:
        worker = Worker(client, runner)
        for signum in (signal.SIGINT, signal.SIGTERM):
            signal.signal(signum, lambda _signum, _frame: worker.stop.set())
        worker.run()
    except (ValueError, RuntimeError, OSError):
        LOG.error("Judge worker stopped during startup; see the failing stage above")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
