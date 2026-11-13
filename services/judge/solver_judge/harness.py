"""Trusted image entrypoint. Learner programs run only inside the gVisor container.

Expected answers, worker tokens and application data are never sent to this process.
"""

import base64
import json
import os
import resource
import signal
import subprocess
import sys
from pathlib import Path

from bounded import limited_process

MAX_SOURCE = 32768
MAX_INPUT = 131072
MAX_CASES = 8
MAX_REQUEST = 1048576
MAX_OUTPUT = 16384
RUN_AS = 128 * 1024 * 1024
COMPILE_AS = 512 * 1024 * 1024
CHILD_ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/tmp", "LANG": "C.UTF-8"}


def limits(*, compile_stage: bool = False, cpu: int | None = None):
    def set_limits():
        memory = COMPILE_AS if compile_stage else RUN_AS
        cpu_limit = cpu or (10 if compile_stage else 2)
        count = 8 if compile_stage else 2  # Includes this supervisor and the child.
        for key, value in (
            (resource.RLIMIT_AS, memory),
            (resource.RLIMIT_CPU, cpu_limit),
            (resource.RLIMIT_NPROC, count),
            (resource.RLIMIT_FSIZE, 16 * 1024 * 1024),
            (resource.RLIMIT_NOFILE, 64),
            (resource.RLIMIT_CORE, 0),
        ):
            resource.setrlimit(key, (value, value))

    return set_limits


def execute(args, stdin="", *, compile_stage=False, cpu=None, wall=None):
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    result = limited_process(
        args,
        stdin.encode(),
        timeout=wall or (15 if compile_stage else 4),
        output_bytes=MAX_OUTPUT,
        env=CHILD_ENV,
        preexec_fn=limits(compile_stage=compile_stage, cpu=cpu),
    )
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu_used = (after.ru_utime + after.ru_stime) - (before.ru_utime + before.ru_stime)
    if result.output_limit:
        status = "OLE"
    elif (
        result.timed_out
        or result.returncode == -signal.SIGKILL
        and cpu_used + 0.000001 >= (cpu or (10 if compile_stage else 2))
    ):
        status = "TLE"
    elif result.returncode != 0:
        # Child-controlled diagnostic text is not evidence of kernel memory accounting.
        # AS limits are enforced, but ambiguous allocation failures remain runtime errors.
        status = "RE"
    else:
        status = "OK"
    return {
        "status": status,
        "stdout": base64.b64encode(result.stdout).decode("ascii"),
        "stderr": base64.b64encode(result.stderr).decode("ascii"),
        "exit_code": result.returncode,
        "cpu_seconds": cpu_used,
        "wall_timeout": result.timed_out,
    }


def probe():
    """Finite tests; absence of any required control prevents worker advertising readiness."""
    py = [sys.executable, "-I", "-B", "-c"]
    checks = {}
    memory = execute(
        py
        + [
            (
                "try:\n x=bytearray(200*1024*1024)\n print('FAIL')\n"
                "except MemoryError: print('AS_OK')"
            )
        ]
    )
    checks["address_space"] = base64.b64decode(memory["stdout"]).strip() == b"AS_OK"
    forks = execute(
        py
        + [
            (
                "import os\ntry:\n p=os.fork()\n"
                "except OSError as e:\n print('NPROC_OK' if e.errno==11 else 'FAIL')\n"
                "else:\n"
                " if p==0: os._exit(0)\n"
                " os.waitpid(p,0); print('FAIL')"
            )
        ]
    )
    checks["processes"] = base64.b64decode(forks["stdout"]).strip() == b"NPROC_OK"
    cpu = execute(
        py + ["import time\ns=time.monotonic()\nwhile time.monotonic()-s<3: pass"],
        cpu=1,
        wall=10,
    )
    checks["cpu"] = (
        cpu["status"] == "TLE"
        and cpu["exit_code"] == -signal.SIGKILL
        and not cpu["wall_timeout"]
        and cpu["cpu_seconds"] + 0.000001 >= 1
    )
    files = execute(
        py
        + [
            (
                "import resource,os\nresource.setrlimit(resource.RLIMIT_FSIZE,(1024,1024))\n"
                "try:\n"
                " with open('/work/probe-file','wb',buffering=0) as f:\n"
                "  f.write(b'x'*2048); f.write(b'x')\n"
                "except OSError as e: print('FSIZE_OK' if e.errno==27 else 'FAIL')"
            )
        ]
    )
    checks["file_size"] = base64.b64decode(files["stdout"]).strip() == b"FSIZE_OK"
    isolation = execute(
        py
        + [
            (
                "import os,socket\n"
                "assert not os.path.exists('/workspace')\n"
                "assert not os.path.exists('/var/run/docker.sock')\n"
                "assert 'JUDGE_WORKER_TOKEN' not in os.environ\n"
                "try: socket.create_connection(('1.1.1.1',80),timeout=.2)\n"
                "except OSError: print('ISOLATION_OK')\n"
                "else: print('FAIL')"
            )
        ]
    )
    checks["isolation"] = (
        base64.b64decode(isolation["stdout"]).strip() == b"ISOLATION_OK"
    )
    Path("/work/probe.cpp").write_text("int main() { return 0; }\n")
    compiled = execute(
        ["/usr/bin/g++", "-std=c++17", "/work/probe.cpp", "-o", "/work/probe"],
        compile_stage=True,
    )
    checks["compiler"] = (
        compiled["status"] == "OK" and execute(["/work/probe"])["status"] == "OK"
    )
    return {"protocol": 1, "checks": checks, "ok": all(checks.values())}


def main():
    raw = sys.stdin.buffer.read(MAX_REQUEST + 1)
    # Close the supervisor's input before learner code can inspect /proc/1/fd/0.
    sys.stdin.close()
    if len(raw) > MAX_REQUEST:
        raise ValueError("Request too large")
    request = json.loads(raw)
    if request.get("preflight") is True:
        response = probe()
    else:
        source, language, inputs = (
            request["source_code"],
            request["language"],
            request["inputs"],
        )
        if (
            not isinstance(source, str)
            or len(source.encode()) > MAX_SOURCE
            or language not in ("python", "cpp")
            or not isinstance(inputs, list)
            or not 1 <= len(inputs) <= MAX_CASES
            or any(
                not isinstance(i, str) or len(i.encode()) > MAX_INPUT for i in inputs
            )
        ):
            raise ValueError("Invalid sandbox request")
        os.chdir("/work")
        Path("solution.py" if language == "python" else "solution.cpp").write_text(
            source
        )
        if language == "cpp":
            compiled = execute(
                [
                    "/usr/bin/g++",
                    "-std=c++17",
                    "-O2",
                    "-pipe",
                    "solution.cpp",
                    "-o",
                    "/work/solution",
                ],
                compile_stage=True,
            )
            if compiled["status"] != "OK":
                response = {"protocol": 1, "compile": "CE", "results": []}
            else:
                response = {
                    "protocol": 1,
                    "compile": "OK",
                    "results": [execute(["/work/solution"], stdin) for stdin in inputs],
                }
        else:
            compiled = execute(
                [
                    sys.executable,
                    "-I",
                    "-B",
                    "-c",
                    "import ast; ast.parse(open('/work/solution.py').read())",
                ],
                compile_stage=True,
            )
            if compiled["status"] != "OK":
                response = {"protocol": 1, "compile": "CE", "results": []}
            else:
                response = {
                    "protocol": 1,
                    "compile": "OK",
                    "results": [
                        execute(
                            [sys.executable, "-I", "-B", "/work/solution.py"], stdin
                        )
                        for stdin in inputs
                    ],
                }
    print(json.dumps(response, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    try:
        main()
    except (
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
        OSError,
        RuntimeError,
        subprocess.SubprocessError,
    ):
        # Never expose supervisor internals or the submitted payload on errors.
        print('{"protocol":1,"error":"SANDBOX_ERROR"}', flush=True)
        raise SystemExit(1)
