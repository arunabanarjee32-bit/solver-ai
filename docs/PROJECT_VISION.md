# Solver AI — project charter and vision

Status: proposed product vision, updated 2026-11-13. This is not a claim that the software exists yet.

## Mission

Create an independently controlled, AI-native platform for data structures and algorithms (DSA), competitive programming, Codeforces/AtCoder-style preparation and ICPC team practice. We aspire to compete with the usefulness of LeetCode, Codeforces and other established platforms, but do not claim to be a market leader.

The project is more than a chatbot. Its differentiation should be an end-to-end learning and problem-solving workflow with real judging, verifiable feedback, progressive tutoring, personalized training and rigorous model evaluation.

## Target users

- DSA learners preparing for interviews and seeking structured progress.
- Competitive programmers practicing graphs, DP, greedy, number theory, geometry, strings, data structures and advanced algorithms.
- ICPC teams and coaches practicing timed contests and post-contest analysis.
- Educators/problem setters who need reliable judging and problem management.
- Researchers who want reproducible evaluations of algorithm-solving AI.
- Later: organizations conducting coding assessments, with appropriate integrity controls.

## Product pillars

1. Practice: authorized problem library, tags, difficulty, editor, test cases, submissions, explanations, history and progress.
2. Judge: untrusted-code isolation, C++17/C++20 and Python support, grading, limits, verdicts, queues and diagnostics.
3. AI solver: algorithm plans, candidate solutions, compiler/test feedback, counterexamples, bounded repair and transparent uncertainty.
4. AI tutor: progressive hints, conceptual guidance, code review, adaptive practice and post-solve reflection.
5. Competition: virtual contests, teams, ICPC scoring, scoreboards, ratings and anti-abuse (later phases).
6. Research and ML: consented/licensed datasets, SFT/LoRA/QLoRA, provider-neutral inference and contamination-resistant benchmarks.
7. Sustainable platform: accounts, observability, accessibility, deployment, payments only after proving core learning value.

## Differentiation

- Teach the reasoning behind solutions rather than only return code.
- Show real observed evidence from the judge; never equate sample tests with a proof.
- Adapt practice to weaknesses and track learning over time.
- Build a strong post-contest debugging and counterexample experience.
- Let the platform use interchangeable external or self-hosted models.
- Keep the original product code, data model and brand under project control while respecting upstream licenses.

## Success metrics to instrument (not invented targets)

Weekly returning learners, successful problem submissions, accuracy of verdicts, helpfulness of hints, time to first meaningful feedback, judge latency/failure rate, pass@1/pass@k on unseen benchmark sets, model cost per useful result, safe-execution incidents, and learning retention.

## First release versus long-term ambition

The first release must support a learner opening an original or permissioned problem, writing code in a browser editor, getting a legitimate judge verdict, using an optional hint, and reviewing submission history. It is not a full LeetCode replacement on day one.

## Non-goals and boundaries

- No promise of guaranteed ICPC-hard solution correctness.
- No cloning competitors' proprietary problems, hidden tests, editorials or branding.
- No cheating features for contests where AI help is forbidden.
- No training large models inside Codex Cloud.
- No blanket copying of multiple GitHub repositories.
- No fabricated features, analytics, rankings or deployment claims.

See PRODUCT_REQUIREMENTS.md, ROADMAP.md and PROJECT_STATUS.md.
