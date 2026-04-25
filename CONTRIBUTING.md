# Contributing to IMPP

Thank you for your interest in contributing to IMPP, the agent memory registry.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/memory-market.git`
3. Create a branch: `git checkout -b your-feature`
4. Make your changes
5. Push and open a PR against `main`

## Development Setup

### Python (protocol + CLI)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
AMM_JWT_SECRET=dev-only-not-for-prod pytest
```

### UI (Next.js)

```bash
cd ui
npm install
npm run dev  # runs on port 3005
```

## Developer Certificate of Origin (DCO)

By contributing to this project, you certify that your contribution was created in whole or in part by you, and you have the right to submit it under the Apache-2.0 license.

All commits must be signed off:

```bash
git commit -s -m "feat: your change"
```

This adds a `Signed-off-by` line to your commit message, certifying the [DCO](https://developercertificate.org/).

## Code Guidelines

- **Python**: Follow existing patterns in `amm/`. Type hints encouraged. Tests go in `tests/`.
- **TypeScript/React**: Follow existing patterns in `ui/`. We use shadcn/ui (base-nova style) with Tailwind CSS v4.
- **Commits**: Use conventional commit messages (`feat:`, `fix:`, `docs:`, `chore:`).
- **Security**: Do not commit secrets, credentials, or API keys. Do not add hardcoded fallback secrets.

## What to Contribute

- Bug fixes and improvements to the verification protocol
- New adversarial probes (see `amm/adversarial/`)
- CLI improvements
- Documentation
- UI improvements
- Test coverage

## What Requires Extra Review

Changes to these areas require security maintainer approval via CODEOWNERS:

- Cryptographic code (`amm/verification/`)
- Scoring and trust weights (`amm/config.py`, `amm/registry/trust.py`)
- CI/CD pipelines (`.github/workflows/`)
- Authentication code

## Review Process

1. All PRs require at least one approval
2. Security-sensitive areas require CODEOWNERS approval
3. CI must pass before merge
4. Maintainers may request changes or additional tests

## Reporting Issues

- **Bugs**: Open a GitHub issue with reproduction steps
- **Security vulnerabilities**: See [SECURITY.md](SECURITY.md)
- **Feature requests**: Open a GitHub issue with your use case
