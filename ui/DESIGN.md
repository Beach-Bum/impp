# Design System — IMPP (Agent Memory Registry)

## Product Context
- **What this is:** Open registry for verified AI agent memory artifacts, with a referee protocol for trust verification
- **Who it's for:** AI/ML engineers, agent developers, researchers working with transferable agent memory
- **Space/industry:** Developer tools, AI infrastructure, package registries
- **Project type:** Web app (registry/marketplace hybrid)
- **Reference:** Packagist (PHP registry) for visual language and information density

## Aesthetic Direction
- **Direction:** Industrial/Utilitarian
- **Decoration level:** Minimal. Typography and whitespace do the work. No decorative elements.
- **Mood:** Serious developer tool. Feels like infrastructure, not a marketing site. Dense but readable. The kind of site where you trust the data because the interface doesn't try to impress you.

## Tech Stack
- **Component library:** shadcn/ui (base-nova style, @base-ui/react primitives)
- **Styling:** Tailwind CSS v4 + shadcn theme tokens (oklch color space)
- **Animation:** animate-ui (for meaningful motion)
- **Docs:** Fumadocs v15 (MDX, owns `/docs` route)
- **Icons:** Lucide React

## Typography
- **Sans:** Geist (via `next/font/google`, CSS var `--font-sans`)
- **Mono:** Geist Mono (via `next/font/google`, CSS var `--font-mono`)
- **Scale:** Uses Tailwind's default type scale (`text-xs` through `text-3xl`)
- **Code:** Geist Mono for package names, hashes, CLI output, code blocks

## Color
- **Approach:** Default shadcn neutral theme. Black and white. No custom accent palette.
- **Tokens:** oklch-based CSS custom properties from shadcn (see `globals.css`)
- **Dark mode:** Toggled via `.dark` class on `<html>`, persisted in localStorage
- **Semantic tokens:** `--background`, `--foreground`, `--muted`, `--muted-foreground`, `--border`, `--primary`, `--secondary`, `--destructive`, `--accent`, etc.

## Spacing
- **Base unit:** 4px (Tailwind default)
- **Density:** Comfortable. Registry data needs breathing room but not magazine whitespace.
- **Max content width:** `max-w-5xl` (64rem / 1024px)

## Layout
- **Approach:** Grid-disciplined. Strict columns, predictable alignment.
- **Grid:** Single-column for most content. 2-column for detail pages (`lg:grid-cols-2`). Table-based for listings.
- **Breakpoints:** Tailwind defaults (`sm`, `md`, `lg`, `xl`, `2xl`)
- **Border radius:** shadcn `--radius` token (default 0.625rem)

## Motion
- **Approach:** Minimal-functional. Only transitions that aid comprehension.
- **Library:** animate-ui available for meaningful animations
- **Rule:** If you can't explain why an animation helps the user understand state, remove it.

## Component Patterns
- **Buttons as links:** `<Button render={<Link href="..." />}>text</Button>` (NOT `asChild`)
- **Cards:** shadcn `Card` / `CardHeader` / `CardContent` / `CardTitle`
- **Tables:** shadcn `Table` / `TableHeader` / `TableBody` / `TableRow` / `TableHead` / `TableCell`
- **Status:** `Badge` with variant mapping (`default`, `secondary`, `destructive`, `outline`)
- **Forms:** shadcn `Input`, `Select`, `Textarea`
- **Loading:** shadcn `Spinner`
- **Alerts:** shadcn `Alert` / `AlertDescription`
- **Tabs:** shadcn `Tabs` / `TabsList` / `TabsTrigger` / `TabsContent`

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-25 | Initial design system created | Formalized from existing implementation. Packagist-inspired industrial aesthetic. |
| 2026-04-25 | Migrated from Primer + styled-components to shadcn/ui + Tailwind | Cleaner component model, better dark mode, no styled-components overhead. |
| 2026-04-25 | Default neutral theme, no custom palette | Black and white first. Custom theming deferred. |
| 2026-04-25 | Geist + Geist Mono fonts | Modern, clean, good for data-dense UI. Native Next.js font loading. |
| 2026-04-25 | base-nova style (render prop, not asChild) | shadcn default for new projects. Uses @base-ui/react primitives. |
