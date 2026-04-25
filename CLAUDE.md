# IMPP — The Agent Memory Package Registry

Read PROJECT_MEMORY.md before doing anything. It has the full product context, repo structure, and recent decisions.

## Rules
- Do NOT refactor existing code. Only add new files or modify files specified in your task.
- Follow patterns in the codebase: shadcn/ui (base-nova), Tailwind CSS v4, Next.js App Router.
- This is a **package registry** (like Packagist/npm), NOT a marketplace. Frame everything as "install packages" not "buy products."
- Homepage line: "IMPP is the agent memory registry."
- `/` is the Packagist-style landing page. `/leaderboard` is the package browser.
- Privy is the preferred auth/wallet direction for humans.
- Public onboarding flow: /signup, /waitlist, /seller-apply, /sandbox

## Stack
- Frontend: Next.js 15 + React 19 + shadcn/ui (base-nova) + Tailwind v4 + Fumadocs v15 + animate-ui
- Backend: FastAPI (Python) in api_server.py, Supabase DB
- Protocol: Python in amm/
- Frontend lives in ui/ (Vercel deploys from ui/ root directory)
- Domains: impp.sh (primary), memorymarket.ai (alias)

## UI Patterns
- Buttons as links use `render` prop: `<Button render={<Link href="..." />}>` — NOT `asChild`
- Select `onValueChange` needs null guard: `(v) => v && setValue(v)`
- All shadcn components in `ui/components/ui/`, animate-ui in `ui/components/animate-ui/`
- Add animate-ui components via: `npx shadcn@latest add "https://animate-ui.com/r/<name>.json"`

## Git Discipline
- Commit after every completed task. Never batch multiple tasks into one commit.
- Commit message format: "feat: short description" or "fix: short description"
- Push to origin after every 3 commits or when finishing your assigned task.
- Never force push. Never rebase.
- If you are about to make a risky change, commit what you have FIRST.

## Handoff Protocol
- Before finishing, update PROJECT_MEMORY.md with what you did and what is left.
- If you made architectural decisions, document them in PROJECT_MEMORY.md.

## Quality Gates (leader agent only)
- After implementation, run /review on the diff before pushing.
- After UI changes, run /design-review on the live preview.
- Before creating a PR, run /ship.
- If something breaks, run /investigate. Do not guess.
- Workers: do NOT run these skills. Only the leader runs quality gates.
