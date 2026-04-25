# IMPP — Project Memory

> State as of 2026-04-25. For any developer (human or AI) picking this up.

## What this project is

An open package registry for verified AI agent memory artifacts — modeled after Packagist/npm, not a marketplace. An agent trains, exports what it learned as structured text, another agent (even on a different model) uses it to perform better. The paper proves this works, the protocol verifies artifacts aren't poisoned, and the registry lets developers install, publish, and manage them via a CLI (`impp install`, `impp publish`, `impp verify`).

**This is a package registry, not a marketplace.** Think Packagist for AI agent memory. The framing is "install packages" not "buy products."

**Live site:** https://impp.sh (alias: https://memorymarket.ai)
**Repo:** https://github.com/Beach-Bum/memory-market

## Current stack

### Frontend (ui/)
- **Framework:** Next.js 15 + React 19
- **Components:** shadcn/ui (base-nova style, @base-ui/react primitives)
- **Styling:** Tailwind CSS v4 + shadcn theme tokens (oklch)
- **Animation:** animate-ui (animated tabs, ripple buttons, tooltips — installed via shadcn CLI)
- **Docs:** Fumadocs v15 (MDX, owns `/docs` route)
- **Fonts:** Geist + Geist Mono (via next/font)
- **Theme:** Default shadcn neutral (black and white). No custom palette.
- **Dark mode:** `.dark` class toggle on `<html>`, persisted in localStorage
- **Deploy:** Vercel, project `acidinfo/memory-market`, root directory `ui/`

### Backend
- **API:** FastAPI (api_server.py), migrated to Supabase
- **Database:** Supabase (was SQLite, migrated 2026-04-24)
- **Deploy:** Railway at `memory-market-api-production.up.railway.app`
- **Protocol library:** Python in `amm/` (verification, adversarial probes, trust scoring)

### Key patterns
- Buttons as links: `<Button render={<Link href="..." />}>` (NOT `asChild`)
- Select `onValueChange` needs null guard: `(v) => v && setValue(v)`
- animate-ui components installed via: `npx shadcn@latest add "https://animate-ui.com/r/<name>.json"`

## Routes

### Top-level (public)
- `/` — Landing page (Packagist-style: search, getting started, publishing, announcements, package feed)
- `/leaderboard` — Browse all 56 artifacts with filtering/sorting/search
- `/docs` — Fumadocs MDX documentation
- `/paper` — Research paper overview
- `/sdk` — Python SDK + REST API reference
- `/sandbox` — Test artifacts against evaluation packs
- `/sandbox/[runId]` — Evaluation run detail with scorecard
- `/signup` — Account creation (Privy-ready)
- `/waitlist` — Interest capture form (posts to API)
- `/seller-apply` — Seller onboarding application (posts to API)

### Preview (app screens, under /preview/*)
- `/preview/market` — Market listing view
- `/preview/compare` — Side-by-side artifact comparison
- `/preview/me` — Buyer profile
- `/preview/portfolio` — Owned artifacts
- `/preview/payments` — Payment rails
- `/preview/transactions` — Transaction history
- `/preview/incidents` — Incident log
- `/preview/policies` — Policy management
- `/preview/agents/[id]` — Agent detail
- `/preview/asset/[slug]` — Artifact detail with tabs (animated)
- `/preview/audit/[artifactId]` — Audit trail
- `/preview/sellers/[sellerId]` — Seller profile

## What was completed

### Paper (paper/agent-memory-markets-v2.md)
- Revised from initial draft to submission-ready working paper
- 13 citations added (ExpeL, Reflexion, Voyager, MemCollab, Akerlof, etc.)
- Cross-model transfer results (Claude→GPT-4o, Section 3.5)
- Leakage ablation (sanitized vs full artifact, Section 3.6)
- Multi-dimensional evaluation scorecard
- Formal economics: buyer utility, adverse selection, pricing, Shapley
- 8-family attack taxonomy + 6-layer defense-in-depth
- Honest statistical reporting: Wilcoxon p-values, held-out-only metrics

### Protocol code (amm/)
- Domain registry with `--domain defi|cybersec` CLI flag
- Cross-model support: LLMClient protocol → AnthropicClient, OpenAIClient, OllamaClient
- Adversarial probes, trust scoring, Ed25519 certificate signing
- CLI (`amm/cli.py`): install, publish, verify commands
- JWT config, API base URL, cert directory management

### Corpus
- DeFi: 32 items (20 training, 12 held-out), 8 scenarios, 6 traps
- CyberSec: 24 items (13 training, 11 held-out), 16 real CVEs

### UI migration (2026-04-25)
- **Full migration from Primer + styled-components to shadcn/ui + Tailwind CSS v4**
- All 20+ screens rewritten to shadcn components
- Landing page rebuilt as Packagist-style package registry (search, getting started, publishing docs, announcements, package feed)
- animate-ui: animated tabs on asset detail, ripple buttons on landing
- Fumadocs v15 for `/docs` route with 7 MDX pages
- Leaderboard page: 56 artifacts (28 DeFi + 28 Cybersec) with filtering/sorting
- ClawTeam components migrated: CheckoutDialog, SandboxDetailScreen, SellerApplyScreen
- New routes: /leaderboard, /docs, /paper, /sdk, /seller-apply
- App screens moved under /preview/* prefix

### Infrastructure (2026-04-24)
- Supabase migration: 11 tables matching SQLite schema
- api_server.py migrated from SQLite to supabase-py
- Railway deploy config
- Checkout flow: orders + confirm endpoints
- Waitlist + seller-apply form submission handlers
- Privy auth scaffolding (passthrough until NEXT_PUBLIC_PRIVY_APP_ID set)

## What's left to build

### Next major deliverable: Import Pipeline + Staged Trust
- **Spec**: `spec/import-pipeline.md` — full spec for bootstrapping registry with real artifacts
- **Staged trust**: Imported → Parsed → Evaluated → Verified → Curated (not everything is "verified" on import)
- **Sources**: GitHub (priority 1), HuggingFace, academic repos, awesome-lists
- **Pipeline**: discover → normalize → fingerprint → evaluate → sign → publish
- **Public framing**: "247 artifacts: 18 verified · 47 evaluated · 183 parsed" (honest counts)
- **Phase 1**: Schema + GitHub adapter + trust state badges in UI
- **Phase 2**: Evaluation pipeline wired to existing verification engine
- **Phase 3**: HuggingFace + academic adapters + manual curation
- **Phase 4**: Scheduled crawls, cross-source dedup, community submissions

### High priority
- **Seed Supabase**: SUPABASE_URL and SUPABASE_SERVICE_KEY not set locally. Need migration SQL first, then seed.
- **Run migration SQL** in Supabase dashboard: `supabase/migrations/20260424000000_initial_schema.sql`
- **DB schema update**: Add trust_state, source columns, import_runs table (see spec)
- **More experiment trials**: need Anthropic API credits for statistical power
- **Add /api/transactions endpoint** to api_server.py (currently falls back to mock data in UI)

### Completed 2026-04-25
- ✅ Full shadcn/ui migration from Primer + styled-components
- ✅ CodeBlock component with copy-to-clipboard across all screens
- ✅ Accordion, Tooltip, Breadcrumb, HoverCard, AlertDialog, Progress, Collapsible enrichment
- ✅ Fumadocs MDX overrides (pre→CodeBlock, Accordion, Alert, Tabs, Card, Badge)
- ✅ Enriched quickstart.mdx + cli.mdx with interactive components
- ✅ `NEXT_PUBLIC_API_URL` set on Vercel production → Railway
- ✅ CompareScreen, TransactionsScreen, PaymentsScreen wired to live API with mock fallback
- ✅ Fumadocs /docs 500 fixed
- ✅ Old design files confirmed removed
- ✅ Build passes (23+ static pages, /docs dynamic)

### Medium priority
- **Baseline comparisons**: show artifacts beat few-shot exemplars
- **Real DeFi data**: DeFi domain is still fully synthetic
- **API authentication**: Privy session tokens for order endpoints
- **Custom theme**: replace neutral black/white with branded palette when ready

### Lower priority
- **Red-team adversarial framework**: test against MINJA, AgentPoison, BackdoorAgent
- **Economic model simulation**: run pricing/slashing with real data
- **Paper submission**: final proofread, compile LaTeX, ArXiv upload

## Key decisions

### Identity
- **IMPP** = Interoperable Memory Publishing Protocol
- **Package registry**, not marketplace. Framing: "install packages" not "buy products"
- Domains: impp.sh (primary), memorymarket.ai (alias)
- The homepage one-liner: **"IMPP is the agent memory registry."**

### Architecture
- Monorepo: Python backend + Next.js frontend. Vercel deploys from `ui/` subdirectory.
- Supabase for production DB. Railway for API.
- FastAPI with Supabase client. Privy for auth (not yet active).

### UI
- shadcn/ui with base-nova style (uses `render` prop, NOT `asChild`)
- Default neutral theme — no custom palette yet
- Dark mode via `.dark` class toggle
- animate-ui for meaningful animations only

### Paper
- The "no prior work" claim is DEAD — must cite "Infrastructure for Valuable, Tradable, and Verifiable Agent Memory"
- Sanitized artifact outperforming full artifact is the strongest finding
- Statistical power insufficient at n=32, need ~100-150 held-out items

## File structure

```
├── amm/                    # Python protocol library
│   ├── adversarial/        # 4 probes + runner
│   ├── artifact/           # Schema, export
│   ├── benchmark/          # Training, sandbox, engine
│   ├── domains/            # DeFi (32 items), CyberSec (24 items)
│   ├── marketplace/        # Identity, listing, preview
│   ├── registry/           # DB, trust computation
│   ├── verification/       # Referee, certificates, Ed25519 signing
│   ├── cli.py              # CLI: install, publish, verify
│   └── config.py           # Model, thresholds, JWT, API config
├── ui/                     # Next.js + shadcn/ui (Vercel deploys this)
│   ├── app/                # Routes (top-level + preview/*)
│   ├── components/         # Screens, shared components, shadcn ui/, animate-ui/
│   ├── content/docs/       # Fumadocs MDX pages
│   └── lib/                # API client, mock data, routes, utils
├── paper/                  # Working paper
├── supabase/               # Migration SQL
├── api_server.py           # FastAPI server (Supabase)
├── seed_marketplace.py     # Database seeder
└── tests/                  # Unit tests
```

## Supabase details
- Project ref: `wfwhttevczinakrbvswr`
- URL: `https://wfwhttevczinakrbvswr.supabase.co`
- Env vars needed on Railway: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `MARKETPLACE_API_KEY`
