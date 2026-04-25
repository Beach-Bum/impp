# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.5.x   | Yes                |
| < 0.5   | No                 |

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

If you discover a security vulnerability in IMPP, please report it privately:

1. Use GitHub's [private vulnerability reporting](https://github.com/Beach-Bum/impp/security/advisories/new)
2. Or email: security@impp.sh

Include:

- Description of the vulnerability
- Steps to reproduce
- Impact assessment
- Suggested fix (if any)

We will acknowledge receipt within 48 hours and aim to provide an initial assessment within 5 business days.

## Scope

The following are in scope:

- The `impp` CLI and Python SDK (`amm/` package)
- The verification protocol (probes, certificate chain, trust scoring)
- The reference registry API (`api_server.py`)
- The web UI (`ui/`)
- CI/CD pipeline security (`.github/workflows/`)

The following are out of scope:

- Third-party dependencies (report to the upstream project)
- The hosted registry at impp.sh (contact us directly)
- Social engineering attacks

## Disclosure Policy

- We follow coordinated disclosure. We ask that you give us 90 days to address the issue before public disclosure.
- We will credit reporters in our security advisories unless they prefer to remain anonymous.
- We will not pursue legal action against researchers who follow this policy.
