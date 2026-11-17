"""Original bounded teaching cases generated in the trusted worker.

The two public samples match the catalog. Additional submission cases are
generated for each job; this module is not a private dataset or a claim of
complete correctness coverage. Expected answers stay outside the sandbox.
"""

import random
import secrets
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    stdin: str
    expected: str


def signal_sum(readings: list[int]) -> int:
    return sum(readings)


def steady_climb(elevations: list[int]) -> int:
    best = current = 0
    previous = None
    for elevation in elevations:
        current = current + 1 if previous is not None and elevation > previous else 1
        best = max(best, current)
        previous = elevation
    return best


def distinct_stations(stations: list[int], k: int) -> int:
    if k < 0:
        raise ValueError("The station limit must be nonnegative.")
    counts: dict[int, int] = defaultdict(int)
    left = best = 0
    for right, station in enumerate(stations):
        counts[station] += 1
        while len(counts) > k:
            removed = stations[left]
            counts[removed] -= 1
            if counts[removed] == 0:
                del counts[removed]
            left += 1
        best = max(best, right - left + 1)
    return best


def _array_case(values: list[int], oracle) -> Case:
    return Case(f"{len(values)}\n{' '.join(map(str, values))}\n", f"{oracle(values)}\n")


def _station_case(values: list[int], k: int) -> Case:
    return Case(
        f"{len(values)} {k}\n{' '.join(map(str, values))}\n",
        f"{distinct_stations(values, k)}\n",
    )


PUBLIC_SAMPLES: dict[str, tuple[Case, Case]] = {
    "signal-sum": (
        Case("5\n4 -2 7 -3 1\n", "7\n"),
        Case("3\n-8 0 8\n", "0\n"),
    ),
    "steady-climb": (
        Case("7\n2 5 8 4 6 9 10\n", "4\n"),
        Case("4\n5 5 5 5\n", "1\n"),
    ),
    "distinct-stations": (
        Case("7 2\n1 2 1 3 3 2 2\n", "4\n"),
        Case("3 0\n8 8 9\n", "0\n"),
    ),
}


def cases_for(problem_slug: str, mode: str, *, seed: int | None = None) -> list[Case]:
    """Return two public run cases or eight bounded submission cases.

    A supplied seed makes unit checks reproducible. Production jobs obtain an
    unpredictable seed from the OS; the seed is not returned to API clients.
    Every generated array has at most 5,000 elements, below catalog limits.
    """
    if mode not in {"run", "submit"}:
        raise ValueError("Unsupported judging mode.")
    if problem_slug not in PUBLIC_SAMPLES:
        raise ValueError("Unsupported problem.")
    cases = list(PUBLIC_SAMPLES[problem_slug])
    if mode == "run":
        return cases

    rng = random.Random(secrets.randbits(128) if seed is None else seed)
    if problem_slug == "signal-sum":
        magnitude = rng.randint(1, 1_000_000_000)
        pairs = [rng.randint(-1_000_000_000, 1_000_000_000) for _ in range(32)]
        cases.extend(
            _array_case(values, signal_sum)
            for values in (
                [rng.randint(-1_000_000_000, 1_000_000_000)],
                [0] * 64,
                [value for pair in pairs for value in (pair, -pair)],
                [1_000_000_000] * 64,
                [-magnitude] * 64,
                [rng.randint(-1_000_000_000, 1_000_000_000) for _ in range(5_000)],
            )
        )
    elif problem_slug == "steady-climb":
        base = rng.randint(0, 100_000)
        cases.extend(
            _array_case(values, steady_climb)
            for values in (
                [rng.randint(0, 1_000_000_000)],
                [base] * 64,
                list(range(base + 64, base, -1)),
                list(range(base, base + 5_000)),
                [base + index // 2 for index in range(128)],
                [rng.randint(0, 1_000_000_000) for _ in range(512)],
            )
        )
    else:
        station = rng.randint(1, 1_000_000_000)
        cases.extend(
            _station_case(values, k)
            for values, k in (
                ([rng.randint(1, 12) for _ in range(128)], 0),
                (list(range(1, 101)), 100),
                ([station] * 5_000, 1),
                (list(range(1, 129)), 32),
                ([1 + index % 5 for index in range(512)], 3),
                ([rng.randint(1, 17) for _ in range(5_000)], 7),
            )
        )
    return cases
