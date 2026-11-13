"""Bounded pipe I/O for trusted Docker control and sandbox subprocess supervision."""

import os
import selectors
import signal
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessResult:
    returncode: int
    stdout: bytes
    stderr: bytes
    timed_out: bool = False
    output_limit: bool = False


def limited_process(
    args: list[str],
    data: bytes = b"",
    *,
    timeout: float,
    output_bytes: int,
    env: dict[str, str] | None = None,
    preexec_fn: Callable[[], None] | None = None,
    cancel: Callable[[], None] | None = None,
) -> ProcessResult:
    """Never buffer unbounded output, and keep input writes under the wall deadline."""
    process = subprocess.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
        bufsize=0,
        env=env,
        preexec_fn=preexec_fn,  # noqa: PLW1509 - only the single-threaded sandbox harness sets it
    )
    assert process.stdin and process.stdout and process.stderr
    selector = selectors.DefaultSelector()
    output = {"stdout": bytearray(), "stderr": bytearray()}
    position = 0
    expired = overflow = False
    deadline = time.monotonic() + timeout
    streams = [process.stdin, process.stdout, process.stderr]
    try:
        for stream in streams:
            os.set_blocking(stream.fileno(), False)
        selector.register(process.stdout, selectors.EVENT_READ, "stdout")
        selector.register(process.stderr, selectors.EVENT_READ, "stderr")
        if data:
            selector.register(process.stdin, selectors.EVENT_WRITE, "stdin")
        else:
            process.stdin.close()
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                expired = True
                break
            for key, _ in selector.select(min(remaining, 0.1)):
                stream, kind = key.fileobj, key.data
                if kind == "stdin":
                    try:
                        position += os.write(
                            stream.fileno(), data[position : position + 65536]
                        )
                    except BrokenPipeError:
                        position = len(data)
                    if position == len(data):
                        selector.unregister(stream)
                        stream.close()
                else:
                    chunk = os.read(stream.fileno(), 65536)
                    if not chunk:
                        selector.unregister(stream)
                        stream.close()
                        continue
                    used = len(output["stdout"]) + len(output["stderr"])
                    available = max(0, output_bytes - used)
                    output[kind].extend(chunk[:available])
                    if len(chunk) > available:
                        overflow = True
                        break
            if overflow:
                break
        if expired or overflow:
            if cancel:
                cancel()
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        try:
            process.wait(timeout=max(0.1, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            expired = True
            if cancel:
                cancel()
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=3)
    finally:
        selector.close()
        if process.poll() is None:
            if cancel:
                cancel()
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=3)
        for stream in streams:
            if not stream.closed:
                stream.close()
    return ProcessResult(
        process.returncode,
        bytes(output["stdout"]),
        bytes(output["stderr"]),
        expired,
        overflow,
    )
