"""Check the trusted original oracles independently of sandbox execution."""

import random

import pytest
from solver_judge.grading.cases import (
    cases_for,
    distinct_stations,
    signal_sum,
    steady_climb,
)


@pytest.mark.parametrize("slug", ["signal-sum", "steady-climb", "distinct-stations"])
def test_public_samples_and_generated_case_bounds(slug):
    public = cases_for(slug, "run")
    generated = cases_for(slug, "submit", seed=42)
    assert len(public) == 2
    assert len(generated) == 8
    assert generated[:2] == public
    assert generated == cases_for(slug, "submit", seed=42)
    for case in generated:
        words = list(map(int, case.stdin.split()))
        n = words[0]
        assert 1 <= n <= 5_000
        assert case.stdin.endswith("\n")
        assert case.expected.endswith("\n")
        if slug == "distinct-stations":
            k = words[1]
            assert 0 <= k <= n
            assert len(words[2:]) == n
            assert all(1 <= value <= 1_000_000_000 for value in words[2:])
            expected = distinct_stations(words[2:], k)
        else:
            assert len(words[1:]) == n
            assert all(-1_000_000_000 <= value <= 1_000_000_000 for value in words[1:])
            if slug == "steady-climb":
                assert min(words[1:]) >= 0
            oracle = signal_sum if slug == "signal-sum" else steady_climb
            expected = oracle(words[1:])
        assert int(case.expected) == expected


@pytest.mark.parametrize("mode", ["", "RUN", "private", None])
def test_unsupported_modes_fail_closed(mode):
    with pytest.raises(ValueError, match="Unsupported judging mode"):
        cases_for("signal-sum", mode)


def test_unknown_problem_fails_closed():
    with pytest.raises(ValueError, match="Unsupported problem"):
        cases_for("untrusted-path", "submit")


def test_sum_includes_negative_readings_and_uses_large_integers():
    assert signal_sum([1_000_000_000] * 64) == 64_000_000_000
    assert signal_sum([-1_000_000_000, 0, 1_000_000_000]) == 0


@pytest.mark.parametrize(
    ("values", "expected"),
    [([], 0), ([1], 1), ([5, 5, 5], 1), ([9, 6, 2], 1), ([1, 2, 1, 2, 3, 4], 4)],
)
def test_climb_requires_strict_and_contiguous_increases(values, expected):
    assert steady_climb(values) == expected


def test_station_oracle_matches_brute_force_for_small_arrays():
    rng = random.Random(100)
    for n in range(10):
        for _ in range(40):
            stations = [rng.randint(1, 4) for _ in range(n)]
            for k in range(5):
                best = max(
                    (
                        right - left
                        for left in range(n + 1)
                        for right in range(left, n + 1)
                        if len(set(stations[left:right])) <= k
                    ),
                    default=0,
                )
                assert distinct_stations(stations, k) == best


def test_negative_station_limit_is_rejected():
    with pytest.raises(ValueError, match="nonnegative"):
        distinct_stations([1], -1)


def test_submissions_cover_zero_k_and_overflow_cases():
    station_cases = cases_for("distinct-stations", "submit", seed=1)
    assert any(case.stdin.splitlines()[0].endswith(" 0") for case in station_cases[2:])
    assert any(int(case.expected) > 2**31 - 1 for case in cases_for("signal-sum", "submit"))
