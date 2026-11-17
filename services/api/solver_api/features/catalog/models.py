"""Public catalog contracts. There are no private grading cases in this service."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

Difficulty = Literal["Easy", "Medium"]


class PublicModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class ProblemSummary(PublicModel):
    id: str
    slug: str
    title: str
    difficulty: Difficulty
    tags: list[str]
    summary: str
    estimated_minutes: int


class Sample(PublicModel):
    input: str
    output: str
    explanation: str


class StarterCode(PublicModel):
    python: str
    cpp: str


class Provenance(PublicModel):
    author: str
    source: str


class Problem(ProblemSummary):
    statement: str
    input_format: str
    output_format: str
    constraints: list[str]
    samples: list[Sample]
    starter_code: StarterCode
    hints: list[str]
    provenance: Provenance


class ProblemPage(PublicModel):
    items: list[ProblemSummary]
    total: int
    limit: int
    offset: int


class ErrorDetail(PublicModel):
    code: str
    message: str


class ErrorResponse(PublicModel):
    error: ErrorDetail
    request_id: str
