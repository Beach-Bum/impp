# Agent Memory Markets — Project Memory

> State as of 2026-04-24. For any developer (human or AI) picking this up.

## What this project is

A research paper + working protocol + marketplace UI for trading verified AI agent memory artifacts. An agent trains, exports what it learned as structured text, another agent (even on a different model) uses it to perform better. The paper proves this works, the protocol verifies artifacts aren't poisoned, and the marketplace lets people buy and sell them.

**Live site:** https://memorymarket.ai (alias: https://memory-market-gray.vercel.app)
**Repo:** https://github.com/Beach-Bum/memory-market

## What was completed (2026-04-23 → 2026-04-24)

### Paper (paper/agent-memory-markets-v2.md)
- Revised from initial draft to submission-ready working paper
- Narrowed prior work claim (13 citations added: ExpeL, Reflexion, Voyager, MemCollab, Akerlof, Parfit, MINJA, AgentPoison, Sleeper Agents, eTAMP, AutoSkill, Memento-Skills, Memory Transfer Learning)
- Added cross-model transfer results (Claude→GPT-4o, Section 3.5)
- Added leakage ablation (sanitized vs full artifact, Section 3.6) — key finding: framework-only artifacts outperform lookup-table artifacts
- Added multi-dimensional evaluation scorecard S(a) = (E, R, F, A, C, Ξ) (Section 3.7)
- Replaced qualitative economics with formal models: buyer utility, adverse selection/Akerlof, pricing formula, collateral/slashing, Shapley (Section 7)
- Added 8-family attack taxonomy + 6-layer defense-in-depth (Section 9)
- Added governance table (Section 9.4), Limitations section (Section 10)
- Honest statistical reporting: Wilcoxon p-values, held-out-only metrics, power analysis
- Two Deep Research reviews processed and all actionable items addressed

### Protocol code (amm/)
- Domain registry with `--domain defi|cybersec` CLI flag
- Configurable training_rounds per domain
- Bootstrap confidence intervals for transfer efficiency
- Negative TE auto-FAIL override + warn threshold lowered to 50
- Trust score penalizes negative TE (-100 to 100 range)
- Cross-model support: LLMClient protocol → AnthropicClient, OpenAIClient, OllamaClient
- Sanitized export mode (`--sanitized` flag) for leakage ablation
- Paired Wilcoxon signed-rank test (pure Python, no scipy)
- Held-out-only metrics split in compute_transfer_efficiency()
- Marketplace skeleton: identity, listing, preview modules + DB tables
- FastAPI server (api_server.py) with endpoints for listings, previews, trust, feedback, identity, portfolio
- Database seeder (seed_marketplace.py) with 5 artifacts, 4 sellers, verification certs

### Corpus
- DeFi: expanded from 8 → 32 items (20 training, 12 held-out), 8 scenarios, 6 trap items
- CyberSec: expanded from 8 → 24 items (13 training, 11 held-out), 8 scenarios, 6 traps
- CyberSec includes 16 real CVEs: Log4Shell, MOVEit, ProxyShell, Spring4Shell, CitrixBleed, SolarWinds SUNBURST, PrintNightmare, Follina, ESXi OpenSLP, GoAnywhere MFT, PaperCut, Zerologon, FortiGate SSL-VPN, Atlassian Confluence, F5 BIG-IP, Apache path traversal

### Cross-model experiments (manual, GPT-4o as buyer)
- GPT novice: avg error 6.0 (all), 7.0 (held-out)
- GPT buyer + full artifact: avg error 5.97, TE 0.5%
- GPT buyer + sanitized artifact: avg error 5.19, TE 13.5%
- Wilcoxon p=0.37 (directional, not significant at n=32)

### UI (ui/)
- GitHub Primer design system (v38, @primer/react)
- Pages: Market, Compare, Portfolio, Transactions, Payments, Policies, Incidents, Me, Asset detail, Audit, Seller profile, Agent detail
- Real AMM logomark SVG (from designer files at ~/Desktop/SVG/)
- Light/dark mode toggle with full theme switching (header, body, cards, tables, code blocks)
- Fetches from FastAPI backend, falls back to mock data when API unreachable
- Deployed to Vercel: project `acidinfo/memory-market`, root directory `ui/`

## What's left to build

### High priority
- **Purchase flow**: Acquire button → create order → escrow → deliver artifact content → confirm
- **Wire Compare page to API**: currently uses directory mock data
- **Wire Transactions/Payments pages to API**: currently static
- **More experiment trials**: need Anthropic API credits, then run 10+ automated trials for statistical power
- **memorymarket.ai custom domain**: DNS propagated but may need Vercel domain alias verification

### Medium priority
- **Baseline comparisons**: show artifacts beat few-shot exemplars, not just memory-less novice
- **Real DeFi data**: DeFi domain is still fully synthetic (cybersec has real CVEs)
- **Port remaining ChatGPT designs**: Compare side-by-side view, Audit evidence package (HTML prototypes at ~/Projects/agent-research/agent-memory-market/Website/agentic-memory-market-carbon-clickable-prototype/)
- **API authentication**: currently no auth on FastAPI endpoints
- **Vercel + API deployment**: API runs locally only — need Railway/Fly.io for production backend

### Lower priority
- **Red-team the adversarial framework**: test against MINJA, AgentPoison, BackdoorAgent attack families
- **Economic model simulation**: run the pricing/slashing formulas with real data
- **Paper submission prep**: final proofread, compile LaTeX, ArXiv upload
- **Delete stale `Beach-Bum/memory-market-ui` repo** on GitHub (was Carbon version, now dead)

## Key decisions a developer needs to know

### Architecture
- **Monorepo**: Python backend + Next.js frontend in one repo. Vercel deploys from `ui/` subdirectory.
- **SQLite**: good for prototype, will need Postgres for production.
- **FastAPI**: lightweight, no auth. Production needs API keys or JWT.
- **Primer v38**: does NOT have `Box`, `Text`, `TabNav`, or `sx` props. Use plain `<div>` + `style`. Every new screen must follow this pattern or the build breaks.

### UI framework
- Evaluated Carbon (IBM), PatternFly (Red Hat), and Primer (GitHub). **Chose Primer** for its developer-native feel.
- Dark mode uses CSS attribute selectors on `[data-color-mode]` to override inline styles. This is a workaround because Primer's theme variables don't resolve for all components in Next.js SSR. Fragile but works.
- Header is white in light mode, dark in dark mode. Logo swaps between dark fill (`#020202`) and white fill (`#ffffff`).

### Paper
- The "no prior work" claim is DEAD. Must cite "Infrastructure for Valuable, Tradable, and Verifiable Agent Memory" (March 2026) as direct overlap.
- The >100% transfer efficiency is noise, not a finding. Reported honestly as within-run variance.
- The sanitized artifact outperforming the full artifact is the strongest finding. This refutes the "benchmark tutoring" critique.
- Statistical power is insufficient at n=32. Need ~100-150 held-out items for significance at moderate effect size.

### API keys
- **BOTH Anthropic and OpenAI keys were exposed in chat during this session. They MUST be rotated.**
- Anthropic account needs credits added at console.anthropic.com before automated experiments can run.

## File structure

```
├── amm/                    # Python protocol library
│   ├── adversarial/        # 4 probes + runner
│   ├── artifact/           # Schema, export
│   ├── benchmark/          # Training, sandbox, engine
│   ├── domains/            # DeFi (32 items), CyberSec (24 items)
│   ├── marketplace/        # Identity, listing, preview
│   ├── registry/           # SQLite DB, trust computation
│   ├── verification/       # Referee, certificates
│   ├── api.py              # Anthropic client (legacy compat)
│   ├── api_base.py         # LLMClient protocol
│   ├── api_openai.py       # OpenAI client
│   ├── api_ollama.py       # Ollama client
│   └── config.py           # Model, thresholds, weights
├── ui/                     # Next.js + Primer (Vercel deploys this)
│   ├── app/                # Routes
│   ├── components/         # Screens + shared components
│   └── lib/                # API client, mock data, routes
├── paper/                  # Working paper
├── tests/                  # 26 unit tests
├── api_server.py           # FastAPI marketplace server
├── seed_marketplace.py     # Database seeder
├── cross_model_test.py     # GPT cross-model experiment scorer
├── run_experiment.py       # Automated experiment CLI
├── run_verify.py           # Artifact verification CLI
├── run_feedback.py         # Buyer feedback CLI
├── run_trust_report.py     # Trust report CLI
├── artifact-expert-defi-v2.md      # Full expert artifact
├── artifact-sanitized-defi-v2.md   # Sanitized (framework-only) artifact
└── gpt-*-scores.json       # Cross-model experiment results
```

## Update — public landing and onboarding pass (2026-04-24 later)

### 1. What was just completed
- `/` now renders a public landing page instead of redirecting to `/market`
- Added public landing content with hero, trust strip, how-it-works, business-model, and CTA sections
- Added onboarding screens/components for signup, waitlist, seller application, and sandbox scorecard
- Wired public routes for `/signup`, `/waitlist`, `/seller-apply`, and `/sandbox`
- Added `PROJECT_MEMORY.md` handoff updates so the next developer can see the current state quickly

### 2. What is still left to build
- runtime QA on the deployed site after the latest pushes
- ~~CSS/layout polish for the new landing page helpers~~ **DONE** — responsive hero, 3col, 2col grids
- ~~real Privy auth wiring~~ **DONE** — PrivyWrapper added, conditional on NEXT_PUBLIC_PRIVY_APP_ID. Install @privy-io/react-auth and set env var to activate.
- ~~waitlist and seller-application form submission handlers~~ **DONE** — POST /api/waitlist and POST /api/seller-apply with SQLite storage
- ~~`/sandbox/[runId]` detail page~~ **DONE** — scorecard, accuracy comparison, recommendation. Uses mock data until API endpoint exists.
- ~~actual purchase / checkout flow~~ **DONE** — CheckoutDialog component, POST /api/orders + confirm flow, orders table in SQLite
- Wire Compare page to real API (still uses mock data)
- Wire Transactions/Payments pages to real API
- More experiment trials for statistical power
- Deploy backend to Railway/Fly.io (API runs locally only)

### 3. Decisions the next developer needs to know
- Keep the public site split from the product app: `/` is now marketing / onboarding, `/market` is the product entry
- The homepage one-liner is: **The marketplace for verified agent memory.**
- Public onboarding direction is:
  - `/signup` for account creation
  - `/waitlist` for general interest capture
  - `/seller-apply` for seller onboarding
  - `/sandbox` for pre-purchase evaluation
- Privy is the preferred auth/wallet direction for humans; x402 / A2A wallets remain the advanced rail
- PrivyWrapper is a passthrough until NEXT_PUBLIC_PRIVY_APP_ID is set. When ready: install @privy-io/react-auth, uncomment the provider code in PrivyWrapper.tsx, set env var.
- Order confirmation uses atomic UPDATE WHERE status='pending' to prevent double-confirm races.
- The frontend forms (waitlist, seller-apply) post to the FastAPI backend. They gracefully degrade when the API is unreachable (show error message).

## Update — form wiring, purchase flow, and polish (2026-04-24 evening)

### What was completed
- CSS/layout polish: responsive hero grid, 3-column cards, section spacing in public.css
- Privy auth scaffolding: PrivyWrapper component, privy.ts config, conditional provider in layout.tsx
- Signup screen: controlled form state, Privy-ready auth buttons, fallback to waitlist
- Waitlist form: wired to POST /api/waitlist with loading/success/error states
- Seller-apply form: wired to POST /api/seller-apply with loading/success/error states
- Backend: waitlist_entries and seller_applications tables + endpoints with email validation
- Backend: orders table + POST /api/orders, GET /api/orders/{id}, POST /api/orders/{id}/confirm
- Sandbox detail page: /sandbox/[runId] with scorecard, accuracy comparison, recommendation
- Checkout dialog: modal with create→confirm order flow, wired to Acquire button on asset pages
- Review fixes: Next.js 15 params await, atomic order confirmation

## Update — Supabase + Railway production infrastructure (2026-04-24 night)

### What was completed
- **Supabase migration**: `supabase/migrations/20260424000000_initial_schema.sql` with all 11 tables matching SQLite schema
- **api_server.py migrated to Supabase**: replaced all sqlite3 usage with supabase-py client. Removed dependency on amm.registry.db and amm.marketplace.listing (which use SQLite connections). Kept pure-function imports (create_identity, format_trust_report).
- **requirements-api.txt**: added `supabase>=2.0.0`
- **CORS updated**: added `https://memory-market-api-production.up.railway.app` to allow_origins
- **Frontend API URL**: already reads `NEXT_PUBLIC_API_URL` env var in all 5 files (api.ts, CheckoutDialog, WaitlistScreen, SellerApplyScreen, PortfolioScreen). Set `NEXT_PUBLIC_API_URL=https://memory-market-api-production.up.railway.app` in Vercel env vars to connect.

### Supabase details
- Project ref: `wfwhttevczinakrbvswr`
- URL: `https://wfwhttevczinakrbvswr.supabase.co`
- Env vars needed on Railway: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `MARKETPLACE_API_KEY`
- Run the migration SQL in Supabase SQL Editor to create tables

### What is still left
- Run migration SQL in Supabase dashboard (SQL Editor → paste the migration file)
- Set Vercel env var `NEXT_PUBLIC_API_URL=https://memory-market-api-production.up.railway.app`
- Seed Supabase with initial data (port seed_marketplace.py or seed manually)
- The amm/ library modules (db.py, listing.py, identity.py) still use SQLite — they were not modified per CLAUDE.md rules. Only api_server.py was migrated.
