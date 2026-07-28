---
name: visual-explainer
description: Generate self-contained HTML pages that visually explain technical material — systems, code changes, plans, data. Use when the user asks for any diagram or visual explanation, when they want a slide deck or a longform document (user guide, how-to, reference page), when another skill needs one rendered, or proactively in place of a terminal ASCII table (4+ rows or 3+ columns).
license: MIT
argument-hint: "[topic] [--style <name>] [--theme light|dark] [--slides|--handbook] [--picker]"
compatibility: Requires a browser to view generated HTML files.
metadata:
  attribution: "Based on https://github.com/nicobailon/visual-explainer by nicobailon (MIT)"
  version: "0.8.1"
---

# Visual Explainer

Generate self-contained HTML files for technical diagrams, visualizations, and data tables. Never fall back to ASCII art when this skill is loaded.

**Proactive table rendering.** When you're about to present tabular data as an ASCII box-drawing table in the terminal (comparisons, audits, feature matrices, status reports, any structured rows/columns), generate an HTML page instead. The threshold: if the table has 4+ rows or 3+ columns, it belongs in the browser. Don't wait for the user to ask — render it as HTML automatically and tell them the file path. You can still include a brief text summary in the chat, but the table itself should be the HTML page.

## Available Commands

| Command | What it does |
|---------|-------------|
| `web-diagram` | Generate an HTML diagram for any topic |
| `visual-plan` | Generate a visual implementation plan for a feature |
| `slides` | Generate a magazine-quality slide deck |
| `diff-review` | Visual diff review with architecture comparison and code review |
| `plan-review` | Compare a plan against the codebase with risk assessment |
| `project-recap` | Mental model snapshot for context-switching back to a project |
| `fact-check` | Verify accuracy of a document against actual code |

## Arguments

| Flag | Values | Effect |
|---|---|---|
| `--style <name>` | see the table below | Locks the aesthetic direction. Skips the "pick one and vary it" step in Workflow §1 — the choice is made, honor it exactly. |
| `--picker` | — | **Selects a style instead of generating a page.** Short-circuits everything below — see Style Picker. |
| `--theme <light\|dark>` | — | Forces the page's *initial* mode. With no flag the page follows the OS. The toggle is always present regardless — this flag only sets the starting state. |
| `--slides` | — | Slide-deck output instead of a scrollable page. See Slide Deck Mode. |
| `--handbook` | — | Document output instead of a freeform visual page. See Handbook Mode. Mutually exclusive with `--slides`. |
| `--palette <hint>` | e.g. `terracotta+sage`, `deep-blue+gold`, or explicit hexes | Overrides accent selection. Forbidden colors are still forbidden — if the hint contains one, use the nearest allowed hue and say so. |
| `--font <hint>` | e.g. `crimson-pro+noto-sans-mono` | Overrides the font pairing. Forbidden `--font-body` values still rejected. |

**`--style` values.** One flat namespace — the five design directions and the borrowed editor schemes are interchangeable values, no prefix:

| Value | Direction |
|---|---|
| `blueprint` | Technical drawing — subtle grid background, deep slate/blue, monospace labels, precise borders |
| `editorial` | Crimson Pro throughout — 600 headlines, 400 body, so the contrast is weight, not a second face. Set headings at 600 or a text serif goes limp at display size. Generous whitespace, muted earth tones or deep navy + gold |
| `paper` | Warm cream `#faf7f5`, terracotta/sage accents, informal |
| `terminal` | Monochrome — green/amber on near-black, monospace everything |
| `data-dense` | Small type, tight spacing, maximum information, muted colors |
| `dracula` `nord` `catppuccin-mocha` `catppuccin-latte` `solarized-dark` `solarized-light` `gruvbox` `one-dark` `rose-pine` | The real editor scheme, committed to exactly. Its hex values are in `./assets/style-catalog.html` — read the card, don't approximate from memory of the vibe |

An editor scheme sets the *palette*; it doesn't excuse skipping typography and layout decisions. `--style nord` still needs a font pairing and a considered structure.

**`--style` never sets layout.** Structure is the job of `--slides` and `--handbook`, and the two axes compose freely: `--handbook --style nord` is a document in the Nord palette. `--style handbook` is not a value — read it as `--handbook`, apply it as the mode, and say so.

Unknown `--style` value: don't silently fall back. Name the closest supported value, use it, and tell the user. `neon` and `gradient-mesh` are rejected outright (see Anti-Patterns) — substitute a constrained direction and say which.

With no flags, infer the aesthetic from audience and content, and vary it from the previous generation.

## Style Picker

`--picker` **selects a style; it does not generate a page.** It short-circuits everything below — no reference files read, no HTML written.

Open `./assets/style-catalog.html`, the prebuilt catalog that ships with the skill: one specimen card per `--style` value showing the palette at real hex values, the font pairing, and the flag to copy. Three tabs — Styles, Commands, Formats — landing on Styles, so name the other two when you hand it over or the user won't know they exist. **Never regenerate or edit it to serve a picker request;** open it where it lives. Its command cards mirror the Available Commands table above, and their section lists mirror each command's own "Diagram structure" block — so adding a command, or renumbering one's sections, means editing the catalog too.

Then print one line telling the user to reply with a style name or paste the copied flag. **Done when the catalog is open and that line is printed** — nothing else. A picker run ends at the selection: if a topic came with it, say it was ignored rather than generating once they answer.

The catalog is also the **hex authority** for the editor schemes. When honoring `--style gruvbox` and the rest, read its card rather than recalling the palette — that is a read of one file, not a picker run, and the Workflow proceeds normally.

## Workflow

### 1. Think (5 seconds, not 5 minutes)

Before writing HTML, commit to a direction. Don't default to "dark theme with blue accents" every time.

**Visual is always default.** Even essays, blog posts, and articles get visual treatment — extract structure into cards, diagrams, grids, tables.

Prose patterns (lead paragraphs, pull quotes, callout boxes) are **accent elements** within visual pages, not a separate mode. Use them to highlight key points or provide breathing room, but the page structure remains visual.

For prose accents, read both halves: "Prose Accent Elements" in `./references/diagram-types.md` for which accent a page has earned and when, and "Prose Page Elements" in `./references/css-patterns.md` for the CSS that builds it. For everything else, use the standard freeform approach with aesthetic directions below.

**Who is looking?** A developer understanding a system? A PM seeing the big picture? A team reviewing a proposal? This shapes information density and visual complexity.

**What type of content?** Architecture, flowchart, sequence, data flow, schema/ER, state machine, mind map, class diagram, C4 architecture, data table, timeline, dashboard, implementation plan, longform documentation, or prose-first page. Each has distinct layout needs and rendering approaches — route via the table in §2, then read its section in `./references/diagram-types.md`.

**What aesthetic?** Pick one value from the `--style` table in Arguments and commit. The constrained directions (`blueprint`, `editorial`, `paper`, `terminal`) carry visual requirements that crowd out generic output, so prefer them; the editor schemes are flexible and need more discipline to stay distinctive.

**If `--style` / `--palette` / `--font` were passed, the choice is already made** — honor the flags and skip this selection.

Neon dashboard and gradient mesh are **slop** — see Anti-Patterns for the full list before you commit.

Vary the choice each time. If the last diagram was dark and technical, make the next one light and editorial. The swap test: if you replaced your styling with a generic dark theme and nobody would notice the difference, you haven't designed anything.

### 2. Structure

**Read the reference material** before generating — each time, not from memory. Name the files you read before you write any HTML; if you can't, you haven't done this step.
- For text-heavy architecture overviews (card content matters more than topology): read `./templates/architecture.html`
- For flowcharts, sequence diagrams, ER, state machines, mind maps, class diagrams, C4: read `./templates/mermaid-flowchart.html`
- For data tables, comparisons, audits, feature matrices: read `./templates/data-table.html`
- For slide deck presentations (when `--slides` flag is present or `/slides` is invoked): read `./templates/slide-deck.html` and `./references/slide-patterns.md`
- For prose-heavy publishable pages (READMEs, articles, blog posts, essays): read the "Prose Page Elements" section in `./references/css-patterns.md` and "Typography by Content Voice" in `./references/libraries.md`
- For documents (longform documentation, or `--handbook`): read `./templates/handbook.html` — see Handbook Mode

**For CSS/layout patterns and SVG connectors**, read `./references/css-patterns.md`.

**For pages with 4+ sections** (reviews, recaps, dashboards), also read `./references/responsive-nav.md` for section navigation with sticky sidebar TOC on desktop and horizontal scrollable bar on mobile.

**Choosing a rendering approach:**

**Is it even a chart?** Ask before reaching for one. One to three numbers are KPI cards, not a bar chart with three bars. A two-point change is a sentence carrying the delta. A ranking of five things is a table with an inline bar column. A chart earns its space when the *shape* of the data — trend, distribution, part-to-whole, correlation — is the point.

| Content type | Approach | Why |
|---|---|---|
| 1–3 standalone numbers | KPI cards / stat band | A chart with three bars is chrome around three numbers |
| Architecture (text-heavy) | CSS Grid cards + flow arrows | Rich card content (descriptions, code, tool lists) needs CSS control |
| Architecture (topology-focused) | **Mermaid** | Visible connections between components need automatic edge routing |
| Flowchart / pipeline | **Mermaid** | Automatic node positioning and edge routing |
| Sequence diagram | **Mermaid** | Lifelines, messages, and activation boxes need automatic layout |
| Data flow | **Mermaid** with edge labels | Connections and data descriptions need automatic edge routing |
| ER / schema diagram | **Mermaid** | Relationship lines between many entities need auto-routing |
| State machine | **Mermaid** | State transitions with labeled edges need automatic layout |
| Mind map | **Mermaid** | Hierarchical branching needs automatic positioning |
| Class diagram | **Mermaid** | Inheritance, composition, aggregation lines with automatic routing |
| C4 architecture | **Mermaid** | Use `graph TD` + `subgraph` for C4 (not native `C4Context` — it ignores themes) |
| Data table | HTML `<table>` | Semantic markup, accessibility, copy-paste behavior |
| Timeline | CSS (central line + cards) | Simple linear layout doesn't need a layout engine |
| Dashboard | CSS Grid + Chart.js | Card grid with embedded charts |
| Implementation plan / feature spec | CSS cards + a Mermaid flow, code as excerpts | Understanding the approach is the goal, so file structure and 5–10 line snippets carry it — never full source |
| Documentation / longform guide | **Handbook Mode** | Navigable, scannable prose is the payload — no diagram required |

**Once you've picked the approach**, read the matching section of `./references/diagram-types.md` for the syntax, caveats, and CSS override classes for that type.

**If the page contains any Mermaid diagram**, read `./references/mermaid-rules.md` first. It covers the **blow-up** — the one failure that makes a diagram unreadably small — plus the required container structure, theming, labels, and the `.node` collision.

### 3. Style

The forbidden half of every rule below lives in one place: **Anti-Patterns**. Read it before you write CSS.

**Typography is the diagram.** Pick a distinctive font pairing from the list in `./references/libraries.md`. Every page should use a different pairing from recent generations.

**Good pairings (use these):**
- DM Sans + Fira Code (technical, precise)
- Crimson Pro + Noto Sans Mono (editorial, refined — set headlines at 600)
- IBM Plex Sans + IBM Plex Mono (reliable, readable)
- Bricolage Grotesque + Fragment Mono (bold, characterful)
- Plus Jakarta Sans + Azeret Mono (rounded, approachable)

These five mirror the **Rec** rows of the pairing table in `./references/libraries.md`, which holds eight more for when none of them fits the content. Its unmarked display faces — Instrument Serif, Playfair Display — earn a masthead, a pull quote, or a slide, where the type is large enough to carry them. Below roughly 16px they go limp, so a display face as `--font-body` on a scrollable page is the wrong call even though the pairing is listed.

Load via `<link>` in `<head>`. Include a system font fallback in the `font-family` stack for offline resilience.

**Color tells a story.** Use CSS custom properties for the full palette. Define at minimum: `--bg`, `--surface`, `--border`, `--text`, `--text-dim`, and 3-5 accent colors. Each accent should have a full and a dim variant (for backgrounds). Name variables semantically when possible (`--pipeline-step` not `--blue-3`). Support both themes.

**Good accent palettes (use these):**
- Terracotta + sage (`#c2410c`, `#65a30d`) — warm, earthy
- Teal + slate (`#0891b2`, `#0369a1`) — technical, precise
- Rose + cranberry (`#be123c`, `#881337`) — editorial, refined
- Amber + emerald (`#d97706`, `#059669`) — data-focused
- Deep blue + gold (`#1e3a5f`, `#d4a73a`) — premium, sophisticated

**Color has a ceiling: eight categories, three when marks sit apart.** Past eight distinguishable hues the reader stops decoding color and starts hunting the legend, so fold the tail into "Other" or facet into small multiples instead of minting a ninth. Scatter, bubble, and choropleth cap at **three** — their marks are separated in space, which is far less forgiving than the adjacent bars and stacked bands the eight are chosen for. The cap governs Mermaid node colors and diagram accents too, not just charts: a graph coloring nine kinds of node has no color story left.

**Every page ships a theme toggle. This is not optional.** Both modes are attribute-driven so the user can override the OS choice, and the choice persists across reloads. `@media (prefers-color-scheme: ...)` alone is **not** sufficient — it gives the viewer no control.

```css
/* Light-first (editorial, paper/ink, blueprint): */
:root, :root[data-theme="light"] { /* light values */ }
:root[data-theme="dark"]         { /* dark values  */ }

/* Dark-first (IDE-inspired, terminal): */
:root, :root[data-theme="dark"]  { /* dark values  */ }
:root[data-theme="light"]        { /* light values */ }
```

One palette per mode, declared once — no media-query duplicate. A blocking inline script in `<head>` resolves the initial mode (`localStorage` → `--theme` flag → OS) and stamps `data-theme` before first paint, so there is no flash. Copy the "Theme Toggle" section from `./references/css-patterns.md` wholesale: boot script, button markup, CSS, and the `themechange` event that Mermaid pages listen to in order to re-render with the new `themeVariables`.

**Surfaces whisper, they don't shout.** Build depth through subtle lightness shifts (2-4% between levels), not dramatic color changes. Borders should be low-opacity rgba (`rgba(255,255,255,0.08)` in dark mode, `rgba(0,0,0,0.08)` in light) — visible when you look, invisible when you don't.

**Backgrounds create atmosphere.** Don't use flat solid colors for the page background. Subtle gradients, faint grid patterns via CSS, or gentle radial glows behind focal areas. The background should feel like a space, not a void.

**Visual weight signals importance.** Not every section deserves equal visual treatment, and depth is how you say so. Executive summaries and key metrics dominate the viewport on load — larger type, more padding, elevated shadow, accent-tinted background (`ve-card--hero`). Body content stays flat (default `.ve-card`). Code blocks and secondary content feel recessed (`ve-card--recessed`). Reference sections (file maps, dependency lists, decision logs) stay compact and out of the way; use `<details>/<summary>` for what's useful but not primary. See the depth tiers and the collapsible pattern in `./references/css-patterns.md`. When everything pops, nothing does.

**Animation earns its place.** Staggered fade-ins on page load are almost always worth it — they guide the eye through the diagram's hierarchy. Mix animation types by role: `fadeUp` for cards, `fadeScale` for KPIs and badges, `drawIn` for SVG connectors, `countUp` for hero numbers. Hover transitions on interactive-feeling elements make the diagram feel alive. Always respect `prefers-reduced-motion`. CSS transitions and keyframes handle most cases. For orchestrated multi-element sequences, anime.js via CDN is available (see `./references/libraries.md`).

Keep animations purposeful: entrance reveals, hover feedback, and user-initiated interactions. Nothing should glow or pulse on its own.

### 4. Deliver

**Output location:** Write to `~/.agent/diagrams/`. Use a descriptive filename based on content: `modem-architecture.html`, `pipeline-flow.html`, `schema-overview.html`. The directory persists across sessions.

**Tell the user** the file path so they can open or share it. Whether to launch a browser is not this skill's call — decide it from the situation like any other action.

**Run every Quality Check below before you say it's done.** When iterating on a file, hard-refresh (Ctrl+F5): browsers cache `file://` pages and CDN assets aggressively, which makes stale versions look like failed fixes.

## Slide Deck Mode

A magazine-quality slide presentation instead of a scrollable page. **Opt-in only — never auto-select slide format.**

**Before generating slides**, read `./references/slide-patterns.md` (engine CSS, slide types, transitions, nav chrome, presets) and `./templates/slide-deck.html` (which demonstrates 10 of them — CSS Pipeline is reference-only). Also read `./references/css-patterns.md` for shared patterns and `./references/libraries.md` for Mermaid/Chart.js theming.

**Slides are not pages reformatted.** They're a different medium. Each slide is exactly one viewport tall (100dvh) with no scrolling. Typography is 2–3× larger. Compositions are bolder. The agent composes a narrative arc (impact → context → deep dive → resolution) rather than mechanically paginating the source.

**Content completeness.** Changing the medium does not mean dropping content — the Quality Checks coverage enumeration applies unchanged. Follow the "Planning a Deck from a Source Document" process in `slide-patterns.md` before writing any HTML. Collapsible details in the source become their own slides. Add more slides rather than cutting content: a 22-slide deck that covers everything beats a 13-slide deck that looks polished but is missing 40% of the source. Content that exceeds a slide's density limit splits across slides — it never scrolls within one.

**Compositional variety:** Consecutive slides must vary spatial approach — centered, left-heavy, right-heavy, split, edge-aligned, full-bleed. Three centered slides in a row means push one off-axis. Visual-first, text-second: SVG accents, per-slide background gradients, inline sparklines, small Mermaid diagrams.

`slide-patterns.md` holds the 11 slide types and the four curated presets (Midnight Editorial, Warm Signal, Terminal Mono, Swiss Clean); the `--style` values also adapt to slides. Pick one and commit.

## Handbook Mode

A **document** — read top to bottom, then returned to — instead of a freeform visual page. **Unlike slides, auto-select this** for longform documentation: user guides, how-tos, reference pages, anything with 4+ ordered sections a reader comes back to.

**Before generating**, read `./templates/handbook.html` — contents rail, counter-numbered chapters, stat band, marginalia, annotated output blocks, `<dl>` Q&A. It is the layout, not the palette: **`--handbook` fixes structure and leaves color and type open**, so choose a `--style` as on any other page. The template's own clay/teal palette illustrates the mode; it isn't part of it.

**The payload is the structure of the prose.** The template contains no diagram at all, which is normal here — a document earns its keep by making sections navigable and scannable, not by adding a graphic. Per-content treatments are in the Documentation section of `./references/diagram-types.md`; don't just format the prose, transform it.

If both `--slides` and `--handbook` are passed, honor `--slides` and say why — a deck isn't a document.

## File Structure

Every diagram is a single self-contained `.html` file. No external assets except CDN links (fonts, optional libraries) — CSS and JS inline.

**Order in `<head>` is load-bearing:** the theme boot script must run *before* the `<style>` block and before any body content, or the page flashes the wrong palette. Font `<link>`, then boot script, then styles.

## Quality Checks

Before delivering, verify:
- **The squint test**: hierarchy must survive with color and text stripped away. Name the section that dominates the first viewport and the property that makes it dominate — type scale, padding, or depth tier. If every section resolves to the same answer, there is no hierarchy.
- **The swap test**: Would replacing your fonts and colors with a generic dark theme make this indistinguishable from a template? If yes, push the aesthetic further.
- **Theme toggle present and working**: the page has a visible toggle button, `grep` finds both a `:root[data-theme="light"]` and a `:root[data-theme="dark"]` palette, the boot script stamps `data-theme` before paint, and clicking the button flips *every* surface — including Mermaid SVGs, which must re-render via the `themechange` listener. A `data-theme` ruleset with nothing setting the attribute is a bug, not a feature.
- **Both themes are complete**: every custom property set in one `[data-theme]` block has a counterpart in the other. A variable defined only in the dark palette inherits the light value and breaks one direction silently. Check the two blocks against each other key by key.
- **Coverage is accounted for, item by item**: before delivering, walk the source — every section, decision, data point, specification, and collapsible detail — and name where each one landed on the page. A source with 7 sections yields a page covering all 7; 6 decisions means all 6 present, not the 2 that fit the layout. Anything you deliberately left out, say so to the user. "Looks complete" is not the check; the enumeration is. Pretty but incomplete is a failure.
- **Every chart ships its numbers**: a Chart.js canvas is an image to a screen reader, to a printer, and to anyone who wants to copy a value out. Pair each one with the same data as a `<details>` table twin (`.data-table` inside `details.collapsible` — both patterns are in `./references/css-patterns.md`), labelled so the reader knows what it opens. Sparklines and progress bars are exempt when the number they annotate is already in the text beside them.
- **Section nav survives a jump**: on any page with a TOC, click the **last** link and confirm a link still carries `.active`. Scrolling by hand passes even with a broken scroll-spy; only the jump separates them. Track scroll position, never `IntersectionObserver` — see "JavaScript — Scroll Spy" in `./references/responsive-nav.md`.
- **No overflow**: every grid and flex child needs `min-width: 0` — `grep` the child selectors and confirm it, since one missing declaration is what clips content at narrow widths. Side-by-side panels need `overflow-wrap: break-word`. Never use `display: flex` on `<li>` for marker characters — it creates anonymous flex items that can't shrink, causing lines with many inline `<code>` badges to overflow. Use absolute positioning for markers instead. See the Overflow Protection section in `./references/css-patterns.md`.
- **Mermaid zoom controls**: on pages and documents, every `.mermaid-wrap` gets the five-button set — `zoom-in` `zoom-out` `zoom-fit` `zoom-one` `zoom-expand` — plus Ctrl/Cmd+wheel zoom, drag-to-pan once zoomed, and double-click to fit; `zoom-expand` (⛶) calls `openInNewTab()`. See "Zoom Controls" in `./references/css-patterns.md`. Slide decks run a lighter engine — four buttons (`+ − reset ⛶`) and click-without-drag to expand; see "Diagram Slide" in `./references/slide-patterns.md`. Either way, check the controls against the hint line you shipped: a hint promising an interaction you didn't wire is the common failure.
- **Works over `file://`**: no absolute-path or root-relative asset references (`src="/..."`, `href="/..."`) — they resolve against the filesystem root and fail. No `fetch`/XHR either: `file://` is not a secure context, so anything gated on one needs a fallback. A *single-digit* zoom label is a **blow-up** — check for a mixed subgraph `direction` (see `./references/mermaid-rules.md`); a tall or wide diagram sitting under 50% is fine, contain-only fit working as designed. Note: Mermaid/Chart.js pages need the CDN reachable on first load; CSS-only pages (tables, architecture cards) work fully offline.

## Anti-Patterns (AI Slop)

These patterns are explicitly forbidden. They signal "AI-generated template" and undermine the skill's purpose of producing distinctive, high-quality diagrams. Review every generated page against this list.

### Typography

**Forbidden fonts as primary `--font-body`:**
- Inter — the single most overused AI default
- Roboto, Arial, Helvetica — generic system fallbacks promoted to primary
- system-ui, sans-serif alone — no character, no intent

**Required:** Pick from the font pairings in `./references/libraries.md`. Every generation should use a different pairing from the last.

### Color Palette

**Forbidden accent colors:**
- Indigo-500/violet-500 (`#8b5cf6`, `#7c3aed`, `#a78bfa`) — Tailwind's default purple range
- The cyan + magenta + pink neon gradient combination (`#06b6d4` → `#d946ef` → `#f472b6`)
- Any palette that could be described as "Tailwind defaults with purple/pink/cyan accents"

**Forbidden color effects:**
- Gradient text on headings (`background: linear-gradient(...); background-clip: text;`) — this screams AI-generated
- Animated glowing box-shadows on cards (`box-shadow: 0 0 20px var(--glow); animation: glow 2s...`)
- Multiple overlapping radial glows in accent colors creating a "neon haze"

**Required:** Build palettes from the reference templates (terracotta/sage, teal/cyan, rose/cranberry, slate/blue) or derive from real IDE themes (Dracula, Nord, Solarized, Gruvbox, Catppuccin). Accents should feel intentional, not default.

### Animation

**Forbidden:**
- Animated glowing box-shadows (see Color Palette above)
- Pulsing or breathing effects on static content
- Any animation still running after page load — the sole exception is a progress indicator

**Required:** Entrance reveals, hover feedback, and user-initiated interactions only. Respect `prefers-reduced-motion`.

### Section Headers

**Forbidden:**
- Emoji icons in section headers (🏗️, ⚙️, 📁, 💻, 📅, 🔗, ⚡, 🔧, 📦, 🚀, etc.)
- Section headers that all use the same icon-in-rounded-box pattern

**Required:** Use styled monospace labels with colored dot indicators (see `.section-label` in templates), numbered badges (`section__num` pattern), or asymmetric section dividers. If an icon is genuinely needed, use an inline SVG that matches the palette — not emoji.

### Layout & Hierarchy

**Forbidden:**
- Perfectly centered everything with uniform padding
- All cards styled identically with the same border-radius, shadow, and spacing
- Every section getting equal visual treatment — no hero/primary vs. secondary distinction
- Symmetric layouts where left and right halves mirror each other

**Required:** Vary visual weight. Hero sections should dominate (larger type, more padding, accent-tinted background). Reference sections should feel compact. Use the depth tiers (hero → elevated → default → recessed). Asymmetric layouts create interest.

### Template Patterns

**Forbidden:**
- Three-dot window chrome (red/yellow/green dots) on code blocks — this is a cliché
- KPI cards where every metric has identical gradient text treatment
- "Neon Dashboard" as an aesthetic choice — it always produces generic results
- Gradient meshes with pink/purple/cyan blobs in the background

**Required:** Code blocks use a simple header with filename or language label. KPI cards vary by importance — hero numbers for the primary metric, subdued treatment for supporting metrics. Pick aesthetics with natural constraints: Blueprint (must feel technical/precise), Editorial (must have generous whitespace and serif typography), Paper/ink (must feel warm and informal).

### The Slop Test

Before delivering, apply this test: **Would a developer looking at this page immediately think "AI generated this"?** Count the forbidden items above that are present. Two or more and the page is slop — regenerate with a different `--style`. The constrained directions (editorial, blueprint, paper) and the real editor schemes are harder to mess up, because their specific visual requirements crowd out the generic defaults.
