"""Local worker credential shared only with the API and trusted control worker."""

import os
import secrets
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def worker_token() -> str:
    supplied = os.environ.get("JUDGE_WORKER_TOKEN")
    if supplied:
        if len(supplied) < 32:
            raise ValueError("JUDGE_WORKER_TOKEN must contain at least 32 characters")
        return supplied
    directory = ROOT / ".local"
    directory.mkdir(mode=0o700, exist_ok=True)
    path = directory / "judge-worker-token"
    if not path.exists():
        # Publish a fully written key atomically, preserving another initializer's key.
        with tempfile.NamedTemporaryFile(mode="w", dir=directory, delete=False) as file:
            temporary = Path(file.name)
            file.write(secrets.token_urlsafe(32) + "\n")
        try:
            try:
                os.link(temporary, path)
            except FileExistsError:
                pass
        finally:
            temporary.unlink()
    token = path.read_text().strip()
    if len(token) < 32:
        raise ValueError("Saved worker token is invalid; restore the local worker credential")
    path.chmod(0o600)
    return token
