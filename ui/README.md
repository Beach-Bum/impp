# Agentic Memory Market - Carbon prototype scaffold

This version upgrades the starter into a more realistic frontend handoff:
- Carbon App Router scaffold for `/market`, `/asset/[slug]`, `/portfolio`, `/policies`, and `/incidents`
- real `DataTable` usage on the market and control-tower screens
- a fuller diligence page centered on evidence, provenance, rights, containment, and rollback
- mock data shaped for typed API replacement later

## Stack
- Next.js App Router
- React
- `@carbon/react`
- Sass for Carbon styles

## Getting started

```bash
npm install
npm run dev
```

Then open `http://localhost:3000/market`.

## Notes
- This is still a prototype scaffold: static mock data, no auth, no API integration, no persistence.
- The product hierarchy is intentional: lighter market, heavier diligence, dense ops.
- The static clickable prototype is the fastest way to review flows without a local build.

## Suggested next steps
1. Replace mock tables with typed API contracts and real search state.
2. Add compare tray state and audit exports.
3. Replace the AI hint placeholder with your production explainability pattern.
4. Add role-based controls for acquire, revoke, and rollback.
5. Connect charts and lineage records.
