"""Contract tests exercise real routes with original public catalog content."""

import re

import pytest
from fastapi.testclient import TestClient

from solver_api.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_reports_service_and_correlation_id(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "solver-api"}
    assert re.fullmatch(r"[0-9a-f]{32}", response.headers["x-request-id"])
    assert response.headers["x-content-type-options"] == "nosniff"


def test_catalog_returns_summaries_without_detail_or_private_data(client):
    page = client.get("/api/v1/problems").json()
    assert page["total"] == 3
    assert page["limit"] == 20
    assert page["offset"] == 0
    assert [item["slug"] for item in page["items"]] == [
        "signal-sum",
        "steady-climb",
        "distinct-stations",
    ]
    for item in page["items"]:
        assert set(item) == {
            "id",
            "slug",
            "title",
            "difficulty",
            "tags",
            "summary",
            "estimated_minutes",
        }


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ({"q": "SIGNAL"}, ["signal-sum"]),
        ({"q": "  rising "}, ["steady-climb"]),
        ({"q": "hash maps"}, ["distinct-stations"]),
        ({"difficulty": "Easy"}, ["signal-sum", "steady-climb"]),
        ({"tag": "arrays"}, ["signal-sum", "steady-climb"]),
        ({"difficulty": "Medium", "tag": "Arrays"}, []),
        ({"q": "no such problem"}, []),
    ],
)
def test_filters_are_applied_to_real_catalog(client, query, expected):
    response = client.get("/api/v1/problems", params=query)
    assert response.status_code == 200
    assert [item["slug"] for item in response.json()["items"]] == expected
    assert response.json()["total"] == len(expected)


def test_pagination_counts_before_slicing(client):
    response = client.get("/api/v1/problems", params={"limit": 1, "offset": 1})
    assert response.status_code == 200
    page = response.json()
    assert page["total"] == 3
    assert page["limit"] == 1
    assert page["offset"] == 1
    assert [item["slug"] for item in page["items"]] == ["steady-climb"]
    assert client.get("/api/v1/problems?offset=20").json()["items"] == []


@pytest.mark.parametrize(
    "query",
    [
        {"limit": 0},
        {"limit": 101},
        {"offset": -1},
        {"offset": 10001},
        {"offset": "not-a-number"},
        {"difficulty": "Impossible"},
        {"q": "x" * 101},
        {"tag": "x" * 51},
    ],
)
def test_invalid_queries_have_stable_non_reflecting_errors(client, query):
    response = client.get("/api/v1/problems", params=query)
    assert response.status_code == 422
    payload = response.json()
    assert payload == {
        "error": {
            "code": "INVALID_REQUEST",
            "message": "One or more request parameters are invalid.",
        },
        "request_id": response.headers["x-request-id"],
    }


@pytest.mark.parametrize("slug", ["signal-sum", "steady-climb", "distinct-stations"])
def test_problem_detail_contains_readable_public_exercise(client, slug):
    response = client.get(f"/api/v1/problems/{slug}")
    assert response.status_code == 200
    problem = response.json()
    assert problem["slug"] == slug
    assert problem["statement"]
    assert problem["input_format"]
    assert problem["output_format"]
    assert problem["constraints"]
    assert len(problem["samples"]) == 2
    assert len(problem["hints"]) == 3
    assert "def solve():" in problem["starter_code"]["python"]
    assert "int main()" in problem["starter_code"]["cpp"]
    assert problem["provenance"]["author"] == "Solver AI project"
    assert "Original seed exercise" in problem["provenance"]["source"]
    assert not ({"hidden_tests", "solution", "verdict", "test_cases"} & set(problem))


def test_missing_problem_returns_useful_error(client):
    response = client.get("/api/v1/problems/missing")
    assert response.status_code == 404
    assert response.json() == {
        "error": {"code": "PROBLEM_NOT_FOUND", "message": "This problem does not exist."},
        "request_id": response.headers["x-request-id"],
    }


def test_correlation_ids_are_generated_per_request(client):
    first = client.get("/health", headers={"X-Request-ID": "untrusted-client-value"})
    second = client.get("/health")
    assert first.headers["x-request-id"] != "untrusted-client-value"
    assert first.headers["x-request-id"] != second.headers["x-request-id"]


def test_source_code_submission_requires_authentication(client):
    response = client.post(
        "/api/v1/submissions", json={"source": "raise RuntimeError('must never execute')"}
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"
    method_error = client.post("/api/v1/problems", json={})
    assert method_error.status_code == 405
    assert "GET" in method_error.headers["allow"]


def test_unexpected_errors_do_not_disclose_internal_details(monkeypatch):
    import solver_api.main as main

    class BrokenCatalog:
        def __iter__(self):
            raise RuntimeError("sensitive-internal-information")

    monkeypatch.setattr(main, "PROBLEMS", BrokenCatalog())
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/api/v1/problems")
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "INTERNAL_ERROR"
    assert response.json()["request_id"] == response.headers["x-request-id"]
    assert "sensitive-internal-information" not in response.text


def test_original_samples_match_their_statements(client):
    for slug in ["signal-sum", "steady-climb", "distinct-stations"]:
        problem = client.get(f"/api/v1/problems/{slug}").json()
        for sample in problem["samples"]:
            values = list(map(int, sample["input"].split()))
            if slug == "signal-sum":
                answer = sum(values[1:])
            elif slug == "steady-climb":
                best = current = 1
                heights = values[1:]
                for previous, height in zip(heights, heights[1:], strict=False):
                    current = current + 1 if height > previous else 1
                    best = max(best, current)
                answer = best
            else:
                n, k = values[:2]
                stations = values[2:]
                # Tiny sample oracle, deliberately independent of the suggested window algorithm.
                answer = max(
                    end - start
                    for start in range(n + 1)
                    for end in range(start, n + 1)
                    if len(set(stations[start:end])) <= k
                )
            assert int(sample["output"]) == answer


def test_openapi_documents_the_contract(client):
    schema = client.get("/openapi.json").json()
    assert schema["info"]["version"] == "0.1.0"
    assert "/api/v1/problems" in schema["paths"]
    assert "/api/v1/problems/{slug}" in schema["paths"]
    assert "Problem" in schema["components"]["schemas"]
