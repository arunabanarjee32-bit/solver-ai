"""Versioned, authenticated hint contract. No AI provider or code execution is enabled.

The offline backend returns only the problem author's public hints. Model backends
can be introduced behind the HintBackend protocol after a separate security review.
"""

import asyncio
import os
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator, model_validator

from solver_api.features.catalog.models import Problem, Sample
from solver_api.http.errors import APIError

HINT_TIMEOUT_SECONDS = 3.0


class HintRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    problem_slug: str = Field(
        min_length=1,
        max_length=80,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )
    level: Literal[1, 2, 3]

    @field_validator("level", mode="before")
    @classmethod
    def reject_non_integer_levels(cls, value):
        # Python bool is an int subtype; Pydantic Literal otherwise accepts true as 1.
        if type(value) is not int:
            raise ValueError("The hint level must be an integer")
        return value


class PublicHintContext(BaseModel):
    """Only catalog-visible information may cross a future model boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    slug: str
    title: str
    statement: str
    input_format: str
    output_format: str
    constraints: tuple[str, ...]
    samples: tuple[Sample, ...]


class HintContent(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    hint: str = Field(min_length=1, max_length=1600)
    source: Literal["authored", "mock", "model"]
    provider: str | None = Field(default=None, min_length=1, max_length=80)

    @model_validator(mode="after")
    def validate_provenance(self):
        if (self.source == "authored") != (self.provider is None):
            raise ValueError("Hint provenance must identify an external or mock provider")
        return self


class HintResponse(HintContent):
    schema_version: Literal["1"] = "1"
    problem_slug: str
    level: Literal[1, 2, 3]

    @computed_field
    @property
    def ai_generated(self) -> bool:
        return self.source == "model"


class HintBackend(Protocol):
    async def generate(self, context: PublicHintContext, level: int) -> HintContent:
        """Return bounded hint text and honest provenance."""


class AuthoredHintBackend:
    async def generate(self, context: PublicHintContext, level: int) -> HintContent:
        # Author-written hints are intentionally kept in the existing catalog;
        # the calling API retrieves the chosen hint without invoking a model.
        problem = next((p for p in _public_problems() if p.slug == context.slug), None)
        if problem is None:
            raise ValueError("Unknown authorized problem")
        return HintContent(hint=problem.hints[level - 1], source="authored")


def _public_problems() -> tuple[Problem, ...]:
    # Late import permits a single catalog source of truth, with no private tests.
    from solver_api.features.catalog.content import PROBLEMS

    return PROBLEMS


def public_hint_context(problem: Problem) -> PublicHintContext:
    return PublicHintContext(
        slug=problem.slug,
        title=problem.title,
        statement=problem.statement,
        input_format=problem.input_format,
        output_format=problem.output_format,
        constraints=tuple(problem.constraints),
        samples=tuple(problem.samples),
    )


def select_hint_backend() -> HintBackend:
    # No network or paid model is configured here. Unknown settings fail closed.
    if os.getenv("SOLVER_HINT_BACKEND", "authored") == "authored":
        return AuthoredHintBackend()
    raise APIError(
        503,
        "HINT_PROVIDER_UNAVAILABLE",
        "Generated hints are not configured. Original hints remain on the problem page.",
    )


async def request_hint(problem: Problem, level: Literal[1, 2, 3]) -> HintResponse:
    backend = select_hint_backend()
    try:
        candidate = await asyncio.wait_for(
            backend.generate(public_hint_context(problem), level),
            timeout=HINT_TIMEOUT_SECONDS,
        )
        content = HintContent.model_validate(candidate)
    except Exception as exc:
        # Never reflect model output, raw HTTP errors, stack traces or prompts.
        raise APIError(
            503,
            "HINT_PROVIDER_UNAVAILABLE",
            "Hints are temporarily unavailable. Original hints remain on the problem page.",
        ) from exc

    return HintResponse(
        problem_slug=problem.slug,
        level=level,
        **content.model_dump(),
    )
