"""Read-only local runtime diagnostics; never print credentials or learner data."""

import json
import os

from solver_judge.control.runner import SandboxRunner


def main() -> int:
    runner = SandboxRunner(
        os.environ.get("JUDGE_SANDBOX_IMAGE", "solver-ai-sandbox:local")
    )
    try:
        runner.preflight()
    except (RuntimeError, OSError, ValueError) as error:
        # These are controlled runner/preflight errors; no job or token is supplied.
        response = {"ready": False, "stage": "sandbox preflight", "reason": str(error)}
        if runner.last_preflight:
            response["checks"] = runner.last_preflight.get("checks", {})
        print(json.dumps(response))
        return 1
    print(
        json.dumps(
            {
                "ready": True,
                "stage": "sandbox preflight",
                "checks": runner.last_preflight["checks"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
