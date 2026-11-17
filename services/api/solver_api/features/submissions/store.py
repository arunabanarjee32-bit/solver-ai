"""Durable, owned submission queue. This module never executes learner programs."""

import hashlib
import json
import os
import secrets
import sqlite3
import time
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from solver_api.http.errors import APIError

Language = Literal["python", "cpp"]
Mode = Literal["run", "submit"]
Verdict = Literal["AC", "WA", "CE", "RE", "TLE", "MLE", "OLE", "SYSTEM_ERROR"]
Status = Literal["QUEUED", "RUNNING", "FINISHED"]
MAX_SOURCE_BYTES = 32_768
LEASE_SECONDS = 180
HEARTBEAT_SECONDS = 60


class SubmissionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    problem_slug: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9-]+$")
    language: Language
    source_code: str = Field(min_length=1, max_length=MAX_SOURCE_BYTES)
    mode: Mode

    @field_validator("source_code")
    @classmethod
    def bound_source_bytes(cls, value: str) -> str:
        if len(value.encode("utf-8")) > MAX_SOURCE_BYTES:
            raise ValueError("Source code exceeds the byte limit.")
        return value


class SubmissionSummary(BaseModel):
    id: str
    status: Status
    verdict: Verdict | None
    mode: Mode
    problem_slug: str
    problem_title: str
    language: Language
    created_at: str
    completed_at: str | None
    summary: str | None


class SubmissionDetail(SubmissionSummary):
    source_code: str


class SubmissionPage(BaseModel):
    items: list[SubmissionSummary]
    total: int
    limit: int
    offset: int


class Capabilities(BaseModel):
    judge_available: bool
    languages: list[Language]
    reason: str | None


class WorkerHeartbeat(BaseModel):
    model_config = ConfigDict(extra="forbid")
    worker_id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9._-]+$")
    runtime: Literal["gvisor"]
    languages: list[Language] = Field(min_length=1, max_length=2)


class WorkerLease(BaseModel):
    model_config = ConfigDict(extra="forbid")
    worker_id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9._-]+$")


class WorkerCompletion(WorkerLease):
    lease_token: str = Field(min_length=32, max_length=128)
    verdict: Verdict
    # Accepted for protocol compatibility, but never trusted or reflected to learners.
    summary: str = Field(default="", max_length=512)

    @field_validator("summary")
    @classmethod
    def bound_summary_bytes(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 512:
            raise ValueError("Summary exceeds the byte limit.")
        return value


def iso_timestamp(timestamp: float) -> str:
    return (
        datetime.fromtimestamp(timestamp, UTC)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def safe_summary(verdict: str, mode: str) -> str:
    return {
        "AC": "All public samples passed." if mode == "run" else "All grading checks passed.",
        "WA": "The solution did not match the expected result.",
        "CE": "The solution could not be compiled. Check the language and syntax.",
        "RE": "The solution stopped with a runtime error.",
        "TLE": "The solution exceeded the time limit.",
        "MLE": "The solution exceeded the memory limit.",
        "OLE": "The solution exceeded an output or file size limit.",
        "SYSTEM_ERROR": "The judging service could not finish this attempt. Please try again.",
    }[verdict]


def idempotency_uuid(value: str | None) -> str:
    try:
        return str(UUID(value or ""))
    except (ValueError, AttributeError) as exc:
        raise APIError(
            422, "INVALID_IDEMPOTENCY_KEY", "Provide a UUID Idempotency-Key header."
        ) from exc


class SubmissionStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
        fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
        os.close(fd)
        os.chmod(path, 0o600)
        with self.connect() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
                CREATE TABLE IF NOT EXISTS submissions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    request_hash TEXT NOT NULL,
                    problem_slug TEXT NOT NULL,
                    problem_title TEXT NOT NULL,
                    language TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    source_code TEXT NOT NULL,
                    status TEXT NOT NULL,
                    verdict TEXT,
                    summary TEXT,
                    created_at REAL NOT NULL,
                    completed_at REAL,
                    worker_id TEXT,
                    lease_hash TEXT,
                    lease_expires_at REAL,
                    UNIQUE(user_id, idempotency_key)
                );
                CREATE INDEX IF NOT EXISTS submissions_owner_time
                    ON submissions(user_id, created_at);
                CREATE INDEX IF NOT EXISTS submissions_queue ON submissions(status, created_at);
                CREATE TABLE IF NOT EXISTS judge_workers (
                    worker_id TEXT PRIMARY KEY,
                    runtime TEXT NOT NULL,
                    languages TEXT NOT NULL,
                    heartbeat_at REAL NOT NULL
                );
            """)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA busy_timeout=5000")
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def _expire(db: sqlite3.Connection, now: float) -> None:
        db.execute(
            """UPDATE submissions SET status='FINISHED', verdict='SYSTEM_ERROR', summary=?,
                      completed_at=?, lease_hash=NULL
                      WHERE (status='RUNNING' AND lease_expires_at < ?)
                         OR (status='QUEUED' AND created_at < ?)""",
            (safe_summary("SYSTEM_ERROR", "submit"), now, now, now - 600),
        )

    @staticmethod
    def _detail(row: sqlite3.Row) -> SubmissionDetail:
        return SubmissionDetail(
            id=row["id"],
            status=row["status"],
            verdict=row["verdict"],
            mode=row["mode"],
            problem_slug=row["problem_slug"],
            problem_title=row["problem_title"],
            language=row["language"],
            created_at=iso_timestamp(row["created_at"]),
            completed_at=(iso_timestamp(row["completed_at"]) if row["completed_at"] else None),
            summary=row["summary"],
            source_code=row["source_code"],
        )

    def capabilities(self) -> Capabilities:
        if not os.environ.get("JUDGE_WORKER_TOKEN"):
            return Capabilities(
                judge_available=False,
                languages=["python", "cpp"],
                reason="The isolated judge is not configured.",
            )
        with self.connect() as db:
            rows = db.execute(
                "SELECT languages FROM judge_workers WHERE heartbeat_at > ?",
                (time.time() - HEARTBEAT_SECONDS,),
            ).fetchall()
        languages = sorted({language for row in rows for language in json.loads(row["languages"])})
        return Capabilities(
            judge_available=bool(languages),
            languages=languages or ["python", "cpp"],
            reason=None if languages else "The isolated judging worker is offline.",
        )

    def existing(
        self,
        user_id: str,
        key: str,
        payload: SubmissionRequest,
    ) -> SubmissionDetail | None:
        with self.connect() as db:
            self._expire(db, time.time())
            row = db.execute(
                "SELECT * FROM submissions WHERE user_id=? AND idempotency_key=?", (user_id, key)
            ).fetchone()
        if row is None:
            return None
        if row["request_hash"] != self._request_hash(payload):
            raise APIError(
                409,
                "IDEMPOTENCY_CONFLICT",
                "This idempotency key was already used for a different request.",
            )
        return self._detail(row)

    @staticmethod
    def _request_hash(payload: SubmissionRequest) -> str:
        return hashlib.sha256(payload.model_dump_json().encode()).hexdigest()

    def create(
        self,
        user_id: str,
        key: str,
        payload: SubmissionRequest,
        problem_title: str,
    ) -> SubmissionDetail:
        now = time.time()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            self._expire(db, now)
            existing = db.execute(
                "SELECT * FROM submissions WHERE user_id=? AND idempotency_key=?", (user_id, key)
            ).fetchone()
            if existing:
                if existing["request_hash"] != self._request_hash(payload):
                    raise APIError(
                        409,
                        "IDEMPOTENCY_CONFLICT",
                        "This idempotency key was already used for a different request.",
                    )
                return self._detail(existing)
            if db.execute(
                "SELECT 1 FROM submissions WHERE user_id=? AND status!='FINISHED' LIMIT 1",
                (user_id,),
            ).fetchone():
                raise APIError(
                    429,
                    "SUBMISSION_IN_PROGRESS",
                    "Wait for your current attempt to finish before starting another.",
                    {"Retry-After": "5"},
                )
            count = db.execute(
                "SELECT count(*) FROM submissions WHERE user_id=? AND created_at>?",
                (user_id, now - 60),
            ).fetchone()[0]
            if count >= 10:
                raise APIError(
                    429,
                    "RATE_LIMITED",
                    "Too many attempts. Please try again in a minute.",
                    {"Retry-After": "60"},
                )
            if (
                db.execute("SELECT count(*) FROM submissions WHERE status!='FINISHED'").fetchone()[
                    0
                ]
                >= 100
            ):
                raise APIError(
                    503,
                    "QUEUE_FULL",
                    "The judging queue is full. Please try again later.",
                    {"Retry-After": "10"},
                )
            job_id = uuid4().hex
            db.execute(
                """INSERT INTO submissions
                (id,user_id,idempotency_key,request_hash,problem_slug,problem_title,language,mode,
                 source_code,status,created_at) VALUES (?,?,?,?,?,?,?,?,?,'QUEUED',?)""",
                (
                    job_id,
                    user_id,
                    key,
                    self._request_hash(payload),
                    payload.problem_slug,
                    problem_title,
                    payload.language,
                    payload.mode,
                    payload.source_code,
                    now,
                ),
            )
            row = db.execute("SELECT * FROM submissions WHERE id=?", (job_id,)).fetchone()
        return self._detail(row)

    def get(self, user_id: str, job_id: str) -> SubmissionDetail:
        with self.connect() as db:
            self._expire(db, time.time())
            row = db.execute(
                "SELECT * FROM submissions WHERE id=? AND user_id=?", (job_id, user_id)
            ).fetchone()
        if row is None:
            raise APIError(404, "SUBMISSION_NOT_FOUND", "This attempt does not exist.")
        return self._detail(row)

    def list(self, user_id: str, limit: int, offset: int) -> SubmissionPage:
        with self.connect() as db:
            self._expire(db, time.time())
            total = db.execute(
                "SELECT count(*) FROM submissions WHERE user_id=?", (user_id,)
            ).fetchone()[0]
            rows = db.execute(
                """SELECT * FROM submissions WHERE user_id=?
                                 ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?""",
                (user_id, limit, offset),
            ).fetchall()
        return SubmissionPage(
            items=[
                SubmissionSummary.model_validate(self._detail(row).model_dump()) for row in rows
            ],
            total=total,
            limit=limit,
            offset=offset,
        )

    def heartbeat(self, heartbeat: WorkerHeartbeat) -> None:
        with self.connect() as db:
            db.execute(
                """INSERT INTO judge_workers(worker_id,runtime,languages,heartbeat_at)
                          VALUES (?,?,?,?) ON CONFLICT(worker_id) DO UPDATE SET
                          runtime=excluded.runtime,languages=excluded.languages,
                          heartbeat_at=excluded.heartbeat_at""",
                (
                    heartbeat.worker_id,
                    heartbeat.runtime,
                    json.dumps(sorted(set(heartbeat.languages))),
                    time.time(),
                ),
            )

    def lease(self, worker_id: str) -> dict:
        now = time.time()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            self._expire(db, now)
            worker = db.execute(
                "SELECT * FROM judge_workers WHERE worker_id=? AND heartbeat_at>?",
                (worker_id, now - HEARTBEAT_SECONDS),
            ).fetchone()
            if worker is None:
                raise APIError(
                    409, "WORKER_NOT_READY", "Send a current worker heartbeat before leasing."
                )
            languages = json.loads(worker["languages"])
            placeholders = ",".join("?" for _ in languages)
            row = db.execute(
                f"""SELECT * FROM submissions WHERE status='QUEUED'
                                AND language IN ({placeholders}) ORDER BY created_at,id LIMIT 1""",
                languages,
            ).fetchone()
            if row is None:
                return {"job": None}
            token = secrets.token_urlsafe(32)
            expires = now + LEASE_SECONDS
            db.execute(
                """UPDATE submissions SET status='RUNNING',worker_id=?,lease_hash=?,
                          lease_expires_at=? WHERE id=?""",
                (worker_id, hashlib.sha256(token.encode()).hexdigest(), expires, row["id"]),
            )
        return {
            "job": {
                "id": row["id"],
                "problem_slug": row["problem_slug"],
                "language": row["language"],
                "source_code": row["source_code"],
                "mode": row["mode"],
                "lease_token": token,
                "lease_expires_at": iso_timestamp(expires),
            }
        }

    def complete(self, job_id: str, result: WorkerCompletion) -> None:
        now = time.time()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            self._expire(db, now)
            row = db.execute("SELECT * FROM submissions WHERE id=?", (job_id,)).fetchone()
            if row is None:
                raise APIError(404, "SUBMISSION_NOT_FOUND", "This attempt does not exist.")
            supplied = hashlib.sha256(result.lease_token.encode()).hexdigest()
            if (
                row["worker_id"] != result.worker_id
                or not row["lease_hash"]
                or not secrets.compare_digest(row["lease_hash"], supplied)
            ):
                raise APIError(
                    409, "INVALID_LEASE", "The lease is invalid, expired or already completed."
                )
            if row["status"] != "RUNNING" or row["lease_expires_at"] < now:
                raise APIError(
                    409, "INVALID_LEASE", "The lease is invalid, expired or already completed."
                )
            db.execute(
                """UPDATE submissions SET status='FINISHED',verdict=?,summary=?,
                          completed_at=?,lease_hash=NULL WHERE id=?""",
                (result.verdict, safe_summary(result.verdict, row["mode"]), now, job_id),
            )


@lru_cache(maxsize=16)
def _store_at(path: str) -> SubmissionStore:
    return SubmissionStore(Path(path))


def get_store() -> SubmissionStore:
    default = Path(__file__).resolve().parents[3] / ".local" / "solver.sqlite3"
    return _store_at(str(Path(os.environ.get("SOLVER_DB_PATH", str(default))).resolve()))
