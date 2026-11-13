"""Exercise pipe supervision with fixed trusted probes, never submitted source."""

import sys

from solver_judge.bounded import limited_process


def test_output_limit_stops_child_and_caps_buffer():
    value = limited_process(
        [sys.executable, "-c", "import sys;sys.stdout.write('x'*1000000)"],
        timeout=5,
        output_bytes=1024,
    )
    assert value.output_limit
    assert len(value.stdout) + len(value.stderr) == 1024


def test_wall_limit_stops_sleeping_child():
    value = limited_process(
        [sys.executable, "-c", "import time;time.sleep(2)"],
        timeout=0.1,
        output_bytes=1024,
    )
    assert value.timed_out
    assert value.returncode != 0


def test_large_input_does_not_deadlock_output():
    value = limited_process(
        [sys.executable, "-c", "import sys;d=sys.stdin.buffer.read();print(len(d))"],
        b"x" * 200000,
        timeout=5,
        output_bytes=1024,
    )
    assert value.returncode == 0
    assert value.stdout == b"200000\n"
