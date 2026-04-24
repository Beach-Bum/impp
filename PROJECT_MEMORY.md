# Project Memory

This file is a working memory summary for the `Beach-Bum/memory-market` project so future contributors can quickly understand the current product direction, repo structure, and recent decisions.

## What this repo is

This is the monorepo for **Memory Market / Agentic Memory Exchange**.

- `amm/` — Python protocol and backend logic
- `paper/` — paper and research artifacts
- `api_server.py` — backend API server
- `ui/` — live Next.js frontend deployed from Vercel
- `tests/` — protocol/backend tests

## Product framing

Core positioning:

**The marketplace for verified agent memory.**

Expanded message:

Buy, compare, audit, and deploy verified memory artifacts for AI agents with seller verification, sandbox testing, and controlled payment rails.

## Key product ideas

The platform is not just a listing site. It is a governed marketplace and control plane for tradable agent memory artifacts.

Important product surfaces:
- market discovery
- asset due diligence
- seller trust and verification
- compare
- audit envelope
- payments and transactions
- control tower / portfolio
- sandbox scorecard

## Repo / deployment truth

- The old separate `memory-market-ui` repo is considered stale/dead.
- The active frontend lives in `ui/` inside this monorepo.
- Vercel must deploy from the `ui` root directory.
- The public domain `memorymarket.ai` is intended to point to the `ui/` app.

## Current frontend stack

Frontend in `ui/` uses:
- Next.js
- React
- Primer (`@primer/react`)
- `@primer/octicons-react`
- styled-components

## Current live route set

Implemented routes in `ui/app` include:
- `/` — landing page target or redirect entry
- `/market`
- `/compare`
- `/portfolio`
- `/transactions`
- `/payments`
- `/policies`
- `/incidents`
- `/me`
- `/asset/[slug]`
- `/agents/[id]`
- `/audit/[artifactId]`
- `/sellers/[sellerId]`

Additional public onboarding routes should exist / be added:
- `/signup`
- `/waitlist`
- `/seller-apply`
- `/sandbox`
- `/sandbox/[runId]`

## Branding

Brand mark direction:
- use the provided black/white memory-market mark
- black version for light backgrounds
- white/inverse version for dark header contexts

Branding already started in the Primer shell:
- header should use the logo mark next to `AMM`
- icon routes are generated in-app for favicon / app icon behavior

## Navigation

Shared route config should reflect the current product IA:
- Market
- Compare
- Portfolio
- Transactions
- Payments
- Policies
- Incidents
- Me

## Seller / buyer / account model

Account types:
- Buyer
- Seller
- Agent Wallet

Verification tiers:
- Verified
- Institutional
- Agent Wallet

Seller trust posture should include:
- verification tier
- stake / collateral
- dispute rate
- successful deliveries
- wallet/payment rail
- listed assets

## Payments

Planned payment rails:
- USDC escrow
- x402 / A2A wallet flow
- fiat / card fallback

Recommended direction:
- use **Privy** for human auth and wallet onboarding
- use embedded or connected wallets for buyers/sellers
- keep x402 / agent-wallet flow as advanced capability layer

## Revenue model

Working business model:
- marketplace take rate on primary sales
- verification / premium listing fees
- sandbox / evaluation credits
- escrow / payout routing fees
- enterprise subscriptions for private markets, policy controls, and team features

## Sandbox direction

Sandbox should become a first-class trust surface.

Recommended scorecard fields:
- transfer lift
- negative transfer risk
- adversarial cleanliness
- freshness
- seller tier
- estimated cost
- recommended scope
- rollback recommendation

Example output:
- Transfer lift: +14.2%
- Negative transfer risk: Low
- Adversarial profile: Clean
- Seller tier: Institutional
- Freshness: 12 days
- Estimated monthly cost: $420
- Recommended scope: Retrieval only
- Rollback rule: Auto-detach if negative transfer > 5%

## Landing page direction

Primary one-liner:

**The marketplace for verified agent memory.**

Hero structure:
- headline
- subheadline about buying, comparing, auditing, and deploying memory artifacts
- CTAs for market, signup, sandbox, waitlist
- trust strip showing verified sellers, sandboxing, escrow, rollback controls

## Immediate next work

1. Finish / polish landing page
2. Add signup and waitlist flows
3. Add seller application flow
4. Add sandbox scorecard flow
5. Connect acquire / checkout to payments
6. Increase internal linking between market, assets, sellers, compare, audit, and payments
7. Runtime QA on live Vercel deployment
8. Add backend APIs for real profile, transaction, and sandbox data

## Deployment notes

If Vercel says it cannot detect Next.js, the project is usually pointed at the wrong root directory.

Correct setup:
- repository: `Beach-Bum/memory-market`
- root directory: `ui`
- framework: Next.js
- production branch: `main`

## Why this file exists

This file is intended as a lightweight handoff memory so contributors do not have to reconstruct:
- the repo split
- the UI stack decision
- the branding direction
- the account / payment model
- the key product surfaces
- the current priorities
