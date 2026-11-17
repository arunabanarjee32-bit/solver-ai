"""Host-side trusted gVisor controller. There is deliberately no runc fallback."""

import base64
import json
import os
import subprocess
import threading
import uuid

from solver_judge.bounded import limited_process
from solver_judge.grading.cases import cases_for

DOCKER = ["docker", "--host=unix:///var/run/docker.sock"]
MAX_RESULT = 262144
PROXY_VARIABLES = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "NO_PROXY",
    "FTP_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
    "no_proxy",
    "ftp_proxy",
)
SUMMARIES = {
    "AC": "All selected checks passed. This does not prove correctness for every input.",
    "WA": "The program produced an incorrect answer on a selected check.",
    "CE": "The program could not be compiled. Check its syntax and language selection.",
    "RE": "The program exited unsuccessfully during a selected check.",
    "TLE": "The program exceeded a time limit.",
    "MLE": "The program reported allocation failure under the per-process memory limit.",
    "OLE": "The program exceeded the output limit.",
    "SYSTEM_ERROR": "The isolated judge could not complete this job. Please retry later.",
}


def strict_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("Duplicate sandbox field")
        value[key] = item
    return value


def result(verdict: str) -> dict[str, str]:
    return {"verdict": verdict, "summary": SUMMARIES[verdict]}


def docker_env() -> dict[str, str]:
    """Select the local daemon while preserving managed registry/proxy configuration."""
    return {
        key: value
        for key, value in os.environ.items()
        if key
        not in {
            "DOCKER_HOST",
            "DOCKER_CONTEXT",
            "DOCKER_TLS",
            "DOCKER_TLS_VERIFY",
            "DOCKER_CERT_PATH",
        }
    }


class SandboxRunner:
    def __init__(self, image: str = "solver-ai-sandbox:local"):
        self.image = image
        self.image_id: str | None = None
        self.ready = False
        self.last_preflight: dict | None = None
        self._active: set[str] = set()
        self._active_lock = threading.Lock()
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True
        self.ready = False
        with self._active_lock:
            names = list(self._active)
        failed = False
        for name in names:
            if not self._remove(name):
                failed = True
        if failed:
            raise RuntimeError("Sandbox cleanup failed; readiness was revoked")

    def _docker(self, args: list[str], *, timeout: float = 15) -> bytes:
        completed = limited_process(
            DOCKER + args, timeout=timeout, output_bytes=32768, env=docker_env()
        )
        if completed.returncode or completed.timed_out or completed.output_limit:
            raise RuntimeError("The required local Docker/gVisor operation failed")
        return completed.stdout

    def _remove(self, name: str) -> bool:
        """Forget a container only after removal or a successful absence query."""
        try:
            self._docker(["rm", "--force", name], timeout=10)
        except (RuntimeError, OSError, subprocess.SubprocessError):
            # A failed rm can mean an absent container or an unavailable daemon.
            # Only a successful bounded query can establish absence. A name filter
            # can also match a longer name, which conservatively leaves cleanup pending.
            try:
                remaining = self._docker(
                    [
                        "container", "ls", "--all", "--filter", f"name={name}",
                        "--format", "{{.Names}}",
                    ],
                    timeout=5,
                )
            except (RuntimeError, OSError, subprocess.SubprocessError):
                remaining = None
            if remaining is None or remaining.strip():
                self.ready = False
                with self._active_lock:
                    self._active.add(name)
                return False
        with self._active_lock:
            self._active.discard(name)
        return True

    def _container(self, payload: dict, *, timeout: float = 85) -> dict:
        if self.image_id is None:
            raise RuntimeError("Sandbox image was not resolved")
        if self._cancelled:
            raise RuntimeError("Worker was stopped")
        name = "solver-job-" + uuid.uuid4().hex
        with self._active_lock:
            self._active.add(name)
        args = [
            "create",
            "--name",
            name,
            "--pull=never",
            "--interactive",
            "--runtime=runsc",
            "--network=none",
            "--read-only",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges",
            "--user=10001:10001",
            "--tmpfs",
            "/work:rw,exec,nosuid,nodev,size=32m",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,nodev,size=8m",
            "--shm-size=1m",
            "--ulimit",
            "nproc=8:8",
            "--ulimit",
            "cpu=70:70",
            "--ulimit",
            "fsize=16777216:16777216",
            "--ulimit",
            "nofile=128:128",
            "--ulimit",
            "core=0:0",
        ]
        for key in PROXY_VARIABLES:
            args.extend(["--env", key + "="])
        args.append(self.image_id)
        try:
            self._docker(args)
            if self._cancelled:
                raise RuntimeError("Worker was stopped")
            response = limited_process(
                DOCKER + ["start", "--attach", "--interactive", name],
                json.dumps(payload, separators=(",", ":")).encode(),
                timeout=timeout,
                output_bytes=MAX_RESULT,
                env=docker_env(),
                cancel=lambda: self._remove(name),
            )
            if response.returncode or response.timed_out or response.output_limit:
                raise RuntimeError("Sandbox execution failed")
            decoded = json.loads(response.stdout, object_pairs_hook=strict_object)
            if (
                not isinstance(decoded, dict)
                or type(decoded.get("protocol")) is not int
                or decoded["protocol"] != 1
            ):
                raise RuntimeError("Invalid sandbox protocol")
            return decoded
        except (ValueError, UnicodeError, OSError) as exc:
            raise RuntimeError("Sandbox response could not be validated") from exc
        finally:
            if not self._remove(name):
                raise RuntimeError("Sandbox cleanup failed; readiness was revoked") from None

    def preflight(self) -> None:
        self.ready = False
        with self._active_lock:
            if self._active:
                raise RuntimeError("Unresolved sandbox cleanup prevents readiness")
        runtimes = json.loads(self._docker(["info", "--format", "{{json .Runtimes}} "]))
        if "runsc" not in runtimes:
            raise RuntimeError(
                "gVisor/runsc is required; plain containers are not a fallback"
            )
        security = json.loads(
            self._docker(["info", "--format", "{{json .SecurityOptions}} "])
        )
        if "name=rootless" not in security:
            raise RuntimeError(
                "This development worker requires the reviewed rootless daemon"
            )
        image = self._docker(["image", "inspect", self.image, "--format", "{{.Id}}"])
        self.image_id = image.decode().strip()
        if not self.image_id.startswith("sha256:") or len(self.image_id) != 71:
            raise RuntimeError("Sandbox image identity is invalid")
        probe = self._container({"preflight": True}, timeout=50)
        self.last_preflight = probe
        if (
            probe.get("ok") is not True
            or set(probe.get("checks", {}))
            != {
                "address_space",
                "processes",
                "cpu",
                "file_size",
                "isolation",
                "compiler",
            }
            or not all(value is True for value in probe["checks"].values())
        ):
            failed = [
                name
                for name in (
                    "address_space",
                    "processes",
                    "cpu",
                    "file_size",
                    "isolation",
                    "compiler",
                )
                if probe.get("checks", {}).get(name) is not True
            ]
            raise RuntimeError(
                "Sandbox preflight failed: " + ", ".join(failed or ["protocol"])
            )
        self.ready = True

    def judge(self, job: dict) -> dict[str, str]:
        if not self.ready:
            return result("SYSTEM_ERROR")
        try:
            source = job["source_code"]
            if (
                not isinstance(source, str)
                or len(source.encode()) > 32768
                or job["language"] not in {"python", "cpp"}
            ):
                return result("SYSTEM_ERROR")
            cases = cases_for(job["problem_slug"], job["mode"])
            response = self._container(
                {
                    "source_code": source,
                    "language": job["language"],
                    # Expected answers remain only in this trusted control process.
                    "inputs": [case.stdin for case in cases],
                }
            )
            if response.get("compile") == "CE":
                return result("CE")
            values = response.get("results")
            if (
                response.get("compile") != "OK"
                or not isinstance(values, list)
                or len(values) != len(cases)
            ):
                return result("SYSTEM_ERROR")
            for case, actual in zip(cases, values, strict=True):
                if not isinstance(actual, dict) or actual.get("status") not in {
                    "OK",
                    "RE",
                    "TLE",
                    "MLE",
                    "OLE",
                }:
                    return result("SYSTEM_ERROR")
                status = actual["status"]
                if status != "OK":
                    return result(status)
                if type(actual.get("exit_code")) is not int or actual["exit_code"] != 0:
                    return result("SYSTEM_ERROR")
                stdout = base64.b64decode(actual.get("stdout", ""), validate=True)
                if len(stdout) > 16384:
                    return result("SYSTEM_ERROR")
                if stdout.split() != case.expected.encode().split():
                    return result("WA")
            return result("AC")
        except (
            KeyError,
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            subprocess.SubprocessError,
        ):
            return result("SYSTEM_ERROR")
