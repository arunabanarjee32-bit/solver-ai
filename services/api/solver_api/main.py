"""Practice catalog and authenticated queue; learner code only runs in isolated workers."""

import os
import secrets
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from solver_api.features.catalog.content import PROBLEMS
from solver_api.features.catalog.models import (
    Difficulty,
    ErrorResponse,
    Problem,
    ProblemPage,
    ProblemSummary,
)
from solver_api.features.hints.service import HintRequest, HintResponse, request_hint
from solver_api.features.identity.verification import require_user
from solver_api.features.submissions.store import (
    Capabilities,
    SubmissionDetail,
    SubmissionPage,
    SubmissionRequest,
    WorkerCompletion,
    WorkerHeartbeat,
    WorkerLease,
    get_store,
    idempotency_uuid,
)
from solver_api.http.body_limit import BodyLimitMiddleware
from solver_api.http.errors import APIError

app = FastAPI(
    title="Solver AI practice API",
    version="0.1.0",
    description=(
        "Original problem catalog and authenticated submission queue. "
        "Only a separately isolated worker executes learner programs. AI inference is not enabled."
    ),
)

app.add_middleware(BodyLimitMiddleware)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    # Generate IDs here instead of reflecting arbitrary client-provided header values.
    request.state.request_id = uuid4().hex
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


def error_response(
    request: Request,
    status: int,
    code: str,
    message: str,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        headers={
            **(headers or {}),
            "X-Request-ID": request.state.request_id,
            "X-Content-Type-Options": "nosniff",
        },
        content={
            "error": {"code": code, "message": message},
            "request_id": request.state.request_id,
        },
    )


@app.exception_handler(APIError)
async def public_error(request: Request, exc: APIError) -> JSONResponse:
    return error_response(request, exc.status, exc.code, exc.message, headers=exc.headers)


@app.exception_handler(RequestValidationError)
async def invalid_request(request: Request, _exc: RequestValidationError) -> JSONResponse:
    # Avoid reflecting user input or framework-internal validation structures.
    return error_response(
        request, 422, "INVALID_REQUEST", "One or more request parameters are invalid."
    )


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException) -> JSONResponse:
    code = {404: "NOT_FOUND", 405: "METHOD_NOT_ALLOWED"}.get(exc.status_code, "HTTP_ERROR")
    message = {
        404: "The requested resource was not found.",
        405: "This method is not supported.",
    }.get(exc.status_code, "The request could not be completed.")
    return error_response(request, exc.status_code, code, message, headers=exc.headers)


@app.exception_handler(Exception)
async def unexpected_error(request: Request, _exc: Exception) -> JSONResponse:
    return error_response(
        request, 500, "INTERNAL_ERROR", "An unexpected error occurred. Please try again later."
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "solver-api"}


@app.get("/api/v1/problems", response_model=ProblemPage, responses={422: {"model": ErrorResponse}})
def list_problems(
    q: Annotated[str, Query(max_length=100)] = "",
    difficulty: Annotated[Difficulty | None, Query()] = None,
    tag: Annotated[str | None, Query(max_length=50)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0, le=10000)] = 0,
) -> ProblemPage:
    query = q.strip().casefold()
    matching = [
        problem
        for problem in PROBLEMS
        if (difficulty is None or problem.difficulty == difficulty)
        and (tag is None or tag.strip().casefold() in {t.casefold() for t in problem.tags})
        and (
            not query
            or query in " ".join([problem.title, problem.summary, *problem.tags]).casefold()
        )
    ]
    return ProblemPage(
        items=[
            ProblemSummary.model_validate(problem.model_dump())
            for problem in matching[offset : offset + limit]
        ],
        total=len(matching),
        limit=limit,
        offset=offset,
    )


@app.get(
    "/api/v1/problems/{slug}",
    response_model=Problem,
    responses={404: {"model": ErrorResponse}},
)
def get_problem(slug: str, request: Request) -> Problem | JSONResponse:
    for problem in PROBLEMS:
        if problem.slug == slug:
            return problem
    return error_response(request, 404, "PROBLEM_NOT_FOUND", "This problem does not exist.")


@app.post("/api/v1/hints", response_model=HintResponse)
async def create_hint(
    payload: HintRequest,
    _user_id: Annotated[str, Depends(require_user)],
) -> HintResponse:
    # Only a signed account and a publicly readable seed problem may request help.
    problem = next((p for p in PROBLEMS if p.slug == payload.problem_slug), None)
    if problem is None:
        raise APIError(404, "PROBLEM_NOT_FOUND", "This problem does not exist.")
    return await request_hint(problem, payload.level)


@app.get("/api/v1/capabilities", response_model=Capabilities)
def capabilities() -> Capabilities:
    return get_store().capabilities()


@app.post("/api/v1/submissions", response_model=SubmissionDetail, status_code=202)
def create_submission(
    payload: SubmissionRequest,
    user_id: Annotated[str, Depends(require_user)],
    idempotency_key: Annotated[str | None, Header()] = None,
) -> SubmissionDetail:
    key = idempotency_uuid(idempotency_key)
    store = get_store()
    existing = store.existing(user_id, key, payload)
    if existing is not None:
        return existing
    problem = next((problem for problem in PROBLEMS if problem.slug == payload.problem_slug), None)
    if problem is None:
        raise APIError(404, "PROBLEM_NOT_FOUND", "This problem does not exist.")
    available = store.capabilities()
    if not available.judge_available or payload.language not in available.languages:
        raise APIError(
            503,
            "JUDGE_UNAVAILABLE",
            available.reason or "The selected language is currently unavailable.",
        )
    return store.create(user_id, key, payload, problem.title)


@app.get("/api/v1/submissions", response_model=SubmissionPage)
def list_submissions(
    user_id: Annotated[str, Depends(require_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0, le=10000)] = 0,
) -> SubmissionPage:
    return get_store().list(user_id, limit, offset)


@app.get("/api/v1/submissions/{job_id}", response_model=SubmissionDetail)
def submission_detail(
    job_id: str, user_id: Annotated[str, Depends(require_user)]
) -> SubmissionDetail:
    return get_store().get(user_id, job_id)


def require_worker(request: Request) -> None:
    configured = os.environ.get("JUDGE_WORKER_TOKEN", "")
    supplied = request.headers.getlist("authorization")
    if (
        not configured
        or len(supplied) != 1
        or not secrets.compare_digest(supplied[0].encode(), f"Bearer {configured}".encode())
    ):
        raise APIError(403, "WORKER_FORBIDDEN", "Worker authorization is required.")


@app.post("/internal/judge/heartbeat", dependencies=[Depends(require_worker)])
def worker_heartbeat(payload: WorkerHeartbeat) -> dict[str, bool]:
    get_store().heartbeat(payload)
    return {"ok": True}


@app.post("/internal/judge/lease", dependencies=[Depends(require_worker)])
def worker_lease(payload: WorkerLease) -> dict:
    return get_store().lease(payload.worker_id)


@app.post("/internal/judge/jobs/{job_id}/complete", dependencies=[Depends(require_worker)])
def worker_completion(job_id: str, payload: WorkerCompletion) -> dict[str, bool]:
    get_store().complete(job_id, payload)
    return {"ok": True}
