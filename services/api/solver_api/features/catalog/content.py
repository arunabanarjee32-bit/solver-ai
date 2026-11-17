"""Original, public teaching exercises authored for this project.

These are statements, samples, starter templates and authored hints, not hidden
judge cases or generated AI advice. No third-party problem text is imported.
"""

from solver_api.features.catalog.models import Problem, Provenance, Sample, StarterCode

PROVENANCE = Provenance(
    author="Solver AI project",
    source=(
        "Original seed exercise authored for Solver AI; no third-party problem content imported."
    ),
)

PROBLEMS: tuple[Problem, ...] = (
    Problem(
        id="SA-001",
        slug="signal-sum",
        title="Signal Sum",
        difficulty="Easy",
        tags=["Arrays", "Implementation"],
        summary="Combine a sequence of signed signal readings into one total.",
        estimated_minutes=10,
        statement=(
            "A field sensor records a sequence of signed signal readings. Positive readings "
            "increase the signal total and negative readings reduce it. Given all readings "
            "in their recorded order, find the final total."
        ),
        input_format=(
            "The first line contains n. The second line contains n space-separated integers."
        ),
        output_format="Print one integer: the sum of all n readings.",
        constraints=["1 ≤ n ≤ 200,000", "−1,000,000,000 ≤ reading ≤ 1,000,000,000"],
        samples=[
            Sample(
                input="5\n4 -2 7 -3 1\n",
                output="7\n",
                explanation="The total is 4 − 2 + 7 − 3 + 1 = 7.",
            ),
            Sample(
                input="3\n-8 0 8\n",
                output="0\n",
                explanation="The positive and negative readings cancel out.",
            ),
        ],
        starter_code=StarterCode(
            python=(
                "import sys\n\n\ndef solve():\n"
                "    data = list(map(int, sys.stdin.buffer.read().split()))\n"
                "    n = data[0]\n    readings = data[1:1 + n]\n"
                "    # Compute and print the total.\n    pass\n\n\n"
                'if __name__ == "__main__":\n    solve()\n'
            ),
            cpp=(
                "#include <iostream>\n#include <vector>\nusing namespace std;\n\n"
                "int main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n"
                "    int n;\n    cin >> n;\n    vector<long long> readings(n);\n"
                "    for (auto& value : readings) cin >> value;\n"
                "    // Compute and print the total.\n    return 0;\n}\n"
            ),
        ),
        hints=[
            "Keep a running total as you visit the readings.",
            "You need one pass and no sorting. In C++, the total may exceed a 32-bit integer.",
            "Aim for O(n) time. A 64-bit integer can hold the largest possible total.",
        ],
        provenance=PROVENANCE,
    ),
    Problem(
        id="SA-002",
        slug="steady-climb",
        title="Steady Climb",
        difficulty="Easy",
        tags=["Arrays", "Two pointers"],
        summary="Find the longest uninterrupted stretch of strictly rising trail markers.",
        estimated_minutes=15,
        statement=(
            "A trail has n markers, each with a measured elevation. A steady climb is a "
            "nonempty contiguous stretch in which each marker is strictly higher than the "
            "previous marker. Find the largest number of markers in a steady climb. "
            "Equal elevations break a climb."
        ),
        input_format=(
            "The first line contains n. The second line contains the n marker elevations "
            "in trail order."
        ),
        output_format=(
            "Print the maximum number of markers in a strictly increasing contiguous stretch."
        ),
        constraints=["1 ≤ n ≤ 200,000", "0 ≤ elevation ≤ 1,000,000,000"],
        samples=[
            Sample(
                input="7\n2 5 8 4 6 9 10\n",
                output="4\n",
                explanation="The final four markers, 4 6 9 10, form the longest steady climb.",
            ),
            Sample(
                input="4\n5 5 5 5\n",
                output="1\n",
                explanation=(
                    "Equal elevations cannot extend a climb, so each stretch has one marker."
                ),
            ),
        ],
        starter_code=StarterCode(
            python=(
                "import sys\n\n\ndef solve():\n"
                "    data = list(map(int, sys.stdin.buffer.read().split()))\n"
                "    n = data[0]\n    elevations = data[1:1 + n]\n"
                "    # Find and print the longest steady climb.\n    pass\n\n\n"
                'if __name__ == "__main__":\n    solve()\n'
            ),
            cpp=(
                "#include <iostream>\n#include <vector>\nusing namespace std;\n\n"
                "int main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n"
                "    int n;\n    cin >> n;\n    vector<int> elevations(n);\n"
                "    for (auto& value : elevations) cin >> value;\n"
                "    // Find and print the longest steady climb.\n    return 0;\n}\n"
            ),
        ),
        hints=[
            "Compare each marker with the marker immediately before it.",
            "When elevation rises, extend the current stretch. Otherwise, restart with one marker.",
            "Track the best stretch separately from the current stretch for an O(n) scan.",
        ],
        provenance=PROVENANCE,
    ),
    Problem(
        id="SA-003",
        slug="distinct-stations",
        title="Distinct Stations",
        difficulty="Medium",
        tags=["Sliding window", "Hash maps"],
        summary="Choose the longest listening window containing at most k station IDs.",
        estimated_minutes=25,
        statement=(
            "A radio records the station ID heard at each moment. You want to keep one "
            "contiguous, possibly empty, segment of the recording that contains at most k "
            "distinct station IDs. Find the largest number of recorded moments you can keep. "
            "If k is zero, only the empty segment is allowed."
        ),
        input_format=(
            "The first line contains n and k. "
            "The second line contains n space-separated station IDs."
        ),
        output_format=(
            "Print the maximum length of a contiguous segment with at most k distinct IDs."
        ),
        constraints=["1 ≤ n ≤ 200,000", "0 ≤ k ≤ n", "1 ≤ station ID ≤ 1,000,000,000"],
        samples=[
            Sample(
                input="7 2\n1 2 1 3 3 2 2\n",
                output="4\n",
                explanation=(
                    "The segment 3 3 2 2 has length four and uses two distinct station IDs."
                ),
            ),
            Sample(
                input="3 0\n8 8 9\n",
                output="0\n",
                explanation="With no distinct IDs allowed, the empty segment is the only choice.",
            ),
        ],
        starter_code=StarterCode(
            python=(
                "import sys\n\n\ndef solve():\n"
                "    data = list(map(int, sys.stdin.buffer.read().split()))\n"
                "    n, k = data[:2]\n    stations = data[2:2 + n]\n"
                "    # Find and print the longest valid segment.\n    pass\n\n\n"
                'if __name__ == "__main__":\n    solve()\n'
            ),
            cpp=(
                "#include <iostream>\n#include <vector>\n#include <unordered_map>\n"
                "using namespace std;\n\nint main() {\n"
                "    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n"
                "    int n, k;\n    cin >> n >> k;\n    vector<int> stations(n);\n"
                "    for (auto& value : stations) cin >> value;\n"
                "    // Find and print the longest valid segment.\n    return 0;\n}\n"
            ),
        ),
        hints=[
            "Extend a window to the right and keep a count for every station ID inside it.",
            "If the window has over k distinct IDs, move its left edge until it is valid again.",
            "Remove zero-count IDs. Both edges move only forward, giving O(n) expected time.",
        ],
        provenance=PROVENANCE,
    ),
)
