"""Start the trusted control worker using the local credential without logging it."""

import os
import sys

from local_config import ROOT, worker_token

os.chdir(ROOT / "services/judge")
os.environ["JUDGE_WORKER_TOKEN"] = worker_token()
os.execv(sys.executable, [sys.executable, "-m", "solver_judge.control.worker", *sys.argv[1:]])
