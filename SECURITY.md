# Security policy

**Project stage:** planning. No deployed production environment or supported version yet.

## Reporting security vulnerabilities

Please do **not** publish exploit details, credentials, other users' data or vulnerable endpoints in a public issue. Contact a repository maintainer privately through an appropriate GitHub profile contact method, or use GitHub private vulnerability reporting if the maintainers enable it. Do not assume a private reporting channel is enabled until verified.

## Critical security boundaries

Generated/user-submitted code must be considered malicious until proven otherwise. Never run user code in the API process, web server or contributor laptop without an isolated development environment. See [Judge Security](docs/JUDGE_SECURITY.md) for required sandbox and resource limits.

Protect authentication, test-set secrecy, model provider credentials, database access, private submissions and personally identifiable information. All use of datasets or third-party problems must respect applicable licenses and permissions.

## Development requirements

Security findings should be included in dependency and architecture reviews; do not expose any live judge endpoints until isolation, abuse controls and incident procedures are tested.

This file does not promise a response SLA or formal support policy.
