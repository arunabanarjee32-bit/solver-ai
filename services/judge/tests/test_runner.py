"""Protocol and grading boundary tests do not execute learner programs on the host."""

import base64
import json
from unittest.mock import patch

import pytest
from solver_judge.runner import SandboxRunner, result

JOB = {
    "problem_slug": "signal-sum",
    "mode": "run",
    "language": "python",
    "source_code": "print(7)",
}


def encoded(text):
    return base64.b64encode(text.encode()).decode()


def response(outputs=("7\n", "0\n")):
    return {
        "protocol": 1,
        "compile": "OK",
        "results": [
            {"status": "OK", "exit_code": 0, "stdout": encoded(text), "stderr": ""}
            for text in outputs
        ],
    }


@pytest.fixture
def runner():
    instance = SandboxRunner()
    instance.ready = True
    return instance


def test_expected_answers_are_not_sent_to_sandbox(runner):
    with patch.object(runner, "_container", return_value=response()) as send:
        assert runner.judge(JOB)["verdict"] == "AC"
        payload = send.call_args.args[0]
        assert set(payload) == {"source_code", "language", "inputs"}
        assert all(isinstance(stdin, str) for stdin in payload["inputs"])
        assert "expected" not in payload


def test_wrong_answer_does_not_expose_test_data(runner):
    with patch.object(
        runner, "_container", return_value=response(("secret input echo", "0"))
    ):
        assert runner.judge(JOB) == result("WA")
        assert "secret" not in runner.judge(JOB)["summary"]


@pytest.mark.parametrize("status", ["RE", "TLE", "MLE", "OLE"])
def test_non_success_result_cannot_be_accepted(runner, status):
    payload = response()
    payload["results"][0]["status"] = status
    with patch.object(runner, "_container", return_value=payload):
        assert runner.judge(JOB)["verdict"] == status


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"compile": "OK", "results": []},
        {"compile": "OK", "results": [None, None]},
        {"compile": "OK", "results": [{"status": "AC"}, {"status": "AC"}]},
        {
            "compile": "OK",
            "results": [{"status": "OK", "exit_code": 1}, {"status": "OK"}],
        },
    ],
)
def test_incomplete_or_forged_case_counts_fail_closed(runner, payload):
    with patch.object(runner, "_container", return_value=payload):
        assert runner.judge(JOB)["verdict"] == "SYSTEM_ERROR"


@pytest.mark.parametrize("output", ["!invalid base64!", None, encoded("x" * 17000)])
def test_invalid_or_excessive_encoded_output_fails_closed(runner, output):
    payload = response()
    payload["results"][0]["stdout"] = output
    with patch.object(runner, "_container", return_value=payload):
        assert runner.judge(JOB)["verdict"] == "SYSTEM_ERROR"


def test_unavailable_runner_never_executes():
    runner = SandboxRunner()
    with patch.object(runner, "_container") as execute:
        assert runner.judge(JOB)["verdict"] == "SYSTEM_ERROR"
        execute.assert_not_called()


def test_oversize_source_never_executes(runner):
    with patch.object(runner, "_container") as execute:
        assert (
            runner.judge({**JOB, "source_code": "x" * 32769})["verdict"]
            == "SYSTEM_ERROR"
        )
        execute.assert_not_called()


def test_no_runc_fallback_when_runsc_is_absent():
    runner = SandboxRunner()
    with (
        patch.object(runner, "_docker", return_value=json.dumps({"runc": {}}).encode()),
        pytest.raises(RuntimeError, match="gVisor/runsc"),
    ):
        runner.preflight()
    assert runner.ready is False


def test_duplicate_protocol_keys_are_rejected():
    from solver_judge.runner import strict_object

    with pytest.raises(ValueError, match="Duplicate sandbox field"):
        json.loads('{"protocol":1,"protocol":1}', object_pairs_hook=strict_object)


@pytest.mark.parametrize("exit_code", [False, 0.0, "0"])
def test_non_integer_exit_status_cannot_grant_acceptance(runner, exit_code):
    payload = response()
    payload["results"][0]["exit_code"] = exit_code
    with patch.object(runner, "_container", return_value=payload):
        assert runner.judge(JOB)["verdict"] == "SYSTEM_ERROR"
