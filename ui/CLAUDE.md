# IMPP UI

Next.js 15 + React 19 + shadcn/ui (base-nova) + Fumadocs v15 + Tailwind v4.

Dev server: `npm run dev` (port 3005)

## Design System
- Component library: shadcn/ui with base-nova style (@base-ui/react primitives)
- Styling: Tailwind CSS v4 + shadcn theme tokens (oklch)
- Fonts: Geist (sans) + Geist Mono (code)
- Theme: Default shadcn neutral, black and white. No custom IMPP green palette.
- Dark mode: `.dark` class on `<html>`, toggled via localStorage
- Animation: animate-ui (installed, available for use)
- Docs: Fumadocs v15 (owns `/docs` route with its own styling)

## Component Patterns
- Buttons as links use `render` prop: `<Button render={<Link href="..." />}>text</Button>`
- Do NOT use `asChild` — base-nova style does not support it
- Status indicators use `<Badge>` with variant mapping
- All shadcn components live in `ui/components/ui/`

## Routes
- Top-level: `/`, `/leaderboard`, `/docs`, `/paper`, `/sdk`, `/sandbox`, `/signup`, `/waitlist`
- Preview (app screens): `/preview/market`, `/preview/compare`, `/preview/me`, `/preview/payments`, `/preview/transactions`, `/preview/portfolio`, `/preview/agents/[id]`, `/preview/asset/[slug]`, `/preview/audit/[artifactId]`, `/preview/sellers/[sellerId]`, `/preview/incidents`, `/preview/policies`, `/preview/signup`
