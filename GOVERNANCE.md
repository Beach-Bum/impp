# IMPP Governance

## Roles

### Maintainers

Maintainers have write access and can merge PRs. They are responsible for code review, release management, and project direction.

Current maintainers:
- @Beach-Bum (project lead)

### Security Maintainers

Security maintainers have additional review authority over cryptographic code, scoring algorithms, CI/CD pipelines, and authentication. Changes to these areas require their approval.

### Contributors

Anyone who submits a PR, opens an issue, or improves documentation. Contributors do not have write access but can influence direction through issues and PRs.

## Decision Making

- **Routine changes** (bug fixes, docs, tests): One maintainer approval required.
- **Feature additions**: Discussion in an issue first, then PR with maintainer approval.
- **Protocol changes** (trust scoring, verification, certificate format): Requires discussion, RFC-style write-up, and security maintainer approval.
- **Breaking changes**: Require consensus among active maintainers.

## Releases

- Maintainers decide when to cut releases.
- All releases are signed and published via CI/CD with trusted publishing (OIDC).
- Security patches are prioritized and may be released out of cycle.

## Adding Maintainers

New maintainers are nominated by existing maintainers based on sustained, high-quality contributions. There is no formal voting process at this stage.
