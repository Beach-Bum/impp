# Agent Memory Markets

Read PROJECT_MEMORY.md before doing anything. It has the full product context, repo structure, and recent decisions.

## Rules
- Do NOT refactor existing code. Only add new files or modify files specified in your task.
- Follow patterns already established in the codebase (Primer components, Next.js App Router, styled-components).
- Keep `/` as marketing/onboarding and `/market` as the product entry.
- Homepage line: "The marketplace for verified agent memory."
- Privy is the preferred auth/wallet direction for humans.
- Public onboarding flow: /signup, /waitlist, /seller-apply, /sandbox

## Stack
- Frontend: Next.js (App Router) + React + @primer/react + styled-components
- Backend: FastAPI (Python) in api_server.py
- Protocol: Python in amm/
- Frontend lives in ui/ (Vercel deploys from ui/ root directory)

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
