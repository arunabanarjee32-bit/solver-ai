"""Explicit opt-in integration tests run learner fixtures only inside gVisor."""

import os

import pytest
from solver_judge.control.runner import SandboxRunner

pytestmark = pytest.mark.skipif(
    os.environ.get("SOLVER_JUDGE_INTEGRATION") != "1",
    reason="Set SOLVER_JUDGE_INTEGRATION=1 after building the required gVisor image",
)


@pytest.fixture(scope="module")
def runner():
    instance = SandboxRunner()
    instance.preflight()
    return instance


def job(source, *, language="python", slug="signal-sum", mode="run"):
    return {
        "source_code": source,
        "language": language,
        "problem_slug": slug,
        "mode": mode,
    }


SUM = (
    "import sys\nd=list(map(int,sys.stdin.buffer.read().split()))\nprint(sum(d[1:]))\n"
)
CLIMB = """import sys
x=list(map(int,sys.stdin.buffer.read().split()))[1:]
answer=current=1
for a,b in zip(x,x[1:]):
 current=current+1 if b>a else 1
 answer=max(answer,current)
print(answer)
"""
STATIONS = """import sys
from collections import defaultdict
d=list(map(int,sys.stdin.buffer.read().split()));n,k=d[:2];a=d[2:]
c=defaultdict(int);left=answer=0
for right,x in enumerate(a):
 c[x]+=1
 while len(c)>k:
  c[a[left]]-=1
  if c[a[left]]==0: del c[a[left]]
  left+=1
 answer=max(answer,right-left+1)
print(answer)
"""


@pytest.mark.parametrize(
    ("slug", "source"),
    [
        ("signal-sum", SUM),
        ("steady-climb", CLIMB),
        ("distinct-stations", STATIONS),
    ],
)
def test_correct_python_passes_generated_grading(runner, slug, source):
    assert runner.judge(job(source, slug=slug, mode="submit"))["verdict"] == "AC"


def test_correct_cpp_uses_64bit_sum(runner):
    source = "#include <iostream>\nint main(){int n;std::cin>>n;long long x,s=0;while(n--){std::cin>>x;s+=x;}std::cout<<s;}"
    assert runner.judge(job(source, language="cpp", mode="submit"))["verdict"] == "AC"


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("print(999)", "WA"),
        ("print(", "CE"),
        ("1/0", "RE"),
        ("while True: pass", "TLE"),
        ("x=bytearray(500*1024*1024)", "RE"),
        ("print('x'*100000)", "OLE"),
    ],
)
def test_actual_failure_verdicts(runner, source, expected):
    assert runner.judge(job(source))["verdict"] == expected


def test_cpp_compile_error_is_real(runner):
    assert runner.judge(job("this is not C++", language="cpp"))["verdict"] == "CE"


def test_process_network_filesystem_and_credentials_are_isolated(runner):
    source = (
        """import os,socket
assert os.geteuid()==10001
assert not os.path.exists('/workspace')
assert not os.path.exists('/var/run/docker.sock')
assert not os.environ.get('JUDGE_WORKER_TOKEN')
assert not any(os.environ.get(key) for key in ['HTTP_PROXY','HTTPS_PROXY','http_proxy','https_proxy'])
try: socket.create_connection(('1.1.1.1',80),timeout=.2)
except OSError: pass
else: raise AssertionError('network accessible')
try: os.fork()
except OSError as error: assert error.errno==11
else: raise AssertionError('unexpected child')
"""
        + SUM
    )
    assert runner.judge(job(source))["verdict"] == "AC"


def test_forged_supervisor_output_cannot_get_acceptance(runner):
    source = """import os
with open('/proc/1/fd/1','w') as out:
 out.write('{"protocol":1,"compile":"OK","results":[]}')
print(999)
"""
    assert runner.judge(job(source))["verdict"] == "SYSTEM_ERROR"


def test_killing_supervisor_fails_closed(runner):
    assert (
        runner.judge(job("import os,signal;os.kill(1,signal.SIGKILL)"))["verdict"]
        == "SYSTEM_ERROR"
    )


def test_tmpfs_total_capacity_is_enforced(runner):
    source = (
        """import os
try:
 with open('/tmp/quota-probe','wb',buffering=0) as handle:
  for _ in range(10): handle.write(b'x'*1048576)
except OSError as error: assert error.errno==28
else: raise AssertionError('tmpfs quota not enforced')
os.unlink('/tmp/quota-probe')
"""
        + SUM
    )
    assert runner.judge(job(source))["verdict"] == "AC"
