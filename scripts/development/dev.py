"""Run the local API and web app; stop both when either exits or Ctrl-C arrives."""

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from local_config import worker_token

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--judge", action="store_true", help="Start the gVisor-only control worker")
    options = parser.parse_args()
    uvicorn = ROOT / "services/api/.venv/bin/uvicorn"
    if not uvicorn.exists():
        print("Install API dependencies first: uv sync --project services/api --frozen", file=sys.stderr)
        return 1
    api_environment = {**os.environ}
    if options.judge:
        api_environment["JUDGE_WORKER_TOKEN"] = worker_token()
    else:
        # An explicit independently configured worker can still connect.
        api_environment.setdefault("JUDGE_WORKER_TOKEN", "")
    children: list[subprocess.Popen] = []
    stopping = False

    def stop(_signum: int, _frame: object) -> None:
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    try:
        children.append(subprocess.Popen(
            [str(uvicorn), "solver_api.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=ROOT / "services/api", start_new_session=True,
            env=api_environment,
        ))
        children.append(subprocess.Popen(
            ["npm", "run", "dev:web"], cwd=ROOT, start_new_session=True,
            env={
                **{key: value for key, value in os.environ.items() if key != "JUDGE_WORKER_TOKEN"},
                "API_BASE_URL": os.environ.get("API_BASE_URL", "http://127.0.0.1:8000"),
            },
        ))
        if options.judge:
            children.append(subprocess.Popen(
                [sys.executable, "-m", "solver_judge.control.worker"],
                cwd=ROOT / "services/judge", start_new_session=True,
                env={**os.environ, "JUDGE_WORKER_TOKEN": api_environment["JUDGE_WORKER_TOKEN"]},
            ))
        while not stopping:
            for child in children:
                if child.poll() is not None:
                    return child.returncode or 1
            time.sleep(0.2)
        return 0
    finally:
        for child in children:
            try:
                os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        shutdown_deadline = time.monotonic() + 20
        for child in children:
            try:
                child.wait(timeout=max(0.1, shutdown_deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                child.wait()


if __name__ == "__main__":
    raise SystemExit(main())
