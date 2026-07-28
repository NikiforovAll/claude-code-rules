# Diagram Types

Per-type generation detail. The routing decision — which approach for which content — is the table in `../SKILL.md` §2. Read only the section matching the type you picked.

## Architecture / System Diagrams

Three approaches depending on complexity:

**Simple topology (under 10 elements):** Mermaid. A `graph TD` with custom `themeVariables` produces readable diagrams with automatic edge routing.

**Text-heavy overviews (under 15 elements):** CSS Grid with explicit row/column placement. Sections as rounded cards with colored borders and monospace labels. Vertical flow arrows between sections. The reference template at `../templates/architecture.html` demonstrates this pattern. Use when cards need descriptions, code references, tool lists, or other rich content that Mermaid nodes can't hold.

**Complex architectures (15+ elements):** Use the **hybrid pattern** — a simple Mermaid overview (5-8 nodes showing module relationships) followed by detailed CSS Grid cards for each module's internals. This gives you visual topology AND readable details. The overview diagram uses module names with `<small>` tags for key function names. The cards below show full function lists with new/modified badges. Never cram 15+ elements into a single Mermaid diagram — that is a **blow-up** (see `mermaid-rules.md`).

## Flowcharts / Pipelines

Prefer `graph TD`; use `graph LR` only for simple 3-4 node linear flows. Color-code node types with Mermaid's `classDef` or rely on `themeVariables` for automatic styling. Decision diamonds and parallel branches come out dramatically better than CSS flexbox with arrow characters.

## Sequence Diagrams

Mermaid's `sequenceDiagram` syntax. Style actors and messages via CSS overrides on `.actor`, `.messageText`, `.activation` classes.

## Data Flow Diagrams

`graph TD` (or `graph LR` for simple linear flows) with edge labels for data descriptions. Thicker, colored edges for primary flows. Source/sink nodes styled differently from transform nodes via `classDef`.

## Schema / ER Diagrams

Mermaid's `erDiagram` syntax with entity attributes. Style via `themeVariables` and CSS overrides on `.er.entityBox` and `.er.relationshipLine`.

## State Machines / Decision Trees

`stateDiagram-v2` for states with labeled transitions — supports nested states, forks, joins, and notes. Decision trees can use `graph TD` with diamond decision nodes.

**`stateDiagram-v2` label caveat:** Transition labels have a strict parser — colons, parentheses, `<br/>`, HTML entities, and most special characters cause silent parse failures ("Syntax error in text"). If your labels need any of these (e.g., `cancel()`, `curate: true`, multi-line labels), use `flowchart TD` instead with rounded nodes and quoted edge labels (`|"label text"|`). Flowcharts handle all special characters and support `<br/>` for line breaks. Reserve `stateDiagram-v2` for simple single-word or plain-text labels.

## Mind Maps / Hierarchical Breakdowns

Mermaid's `mindmap` syntax for hierarchical branching from a root node. Mermaid handles the radial layout automatically. Style with `themeVariables` to control node colors at each depth level.

## Class Diagrams

`classDiagram` syntax for domain modeling, OOP design, and entity relationships with typed properties and methods. Relationships: association (`-->`), composition (`*--`), aggregation (`o--`), inheritance (`<|--`). Add multiplicity labels (e.g., `"1" --> "*"`) and abstract/interface markers (`<<interface>>`, `<<abstract>>`). For simple entity boxes without OOP semantics (no methods, no inheritance), prefer `erDiagram` — it produces cleaner output for pure data modeling.

## C4 Architecture Diagrams

**Use Mermaid flowchart syntax — NOT native C4.** `graph TD` with `subgraph` blocks for C4 boundaries. Native `C4Context` hardcodes sharp corners, its own font, blue icons, and inline SVG colors that ignore `themeVariables` — it always clashes with custom palettes.

**Flowchart-as-C4 pattern:** Persons → rounded nodes `(("Name"))`, systems → rectangles `["Name"]`, databases → cylinders `[("Name")]`, boundaries → `subgraph` blocks, relationships → labeled arrows `-->|"protocol"|`. Use `classDef` + `:::className` to visually differentiate external systems (e.g., dashed borders). This inherits `themeVariables`, `fontFamily`, and CSS overrides like every other Mermaid diagram.

## Data Tables / Comparisons / Audits

Use a real `<table>` element — not CSS Grid pretending to be a table. Tables get accessibility, copy-paste behavior, and column alignment for free. The reference template at `../templates/data-table.html` demonstrates all patterns below.

Layout patterns:
- Sticky `<thead>` so headers stay visible when scrolling long tables
- Alternating row backgrounds via `tr:nth-child(even)` (subtle, 2-3% lightness shift)
- First column optionally sticky for wide tables with horizontal scroll
- Responsive wrapper with `overflow-x: auto` for tables wider than the viewport
- Column width hints via `<colgroup>` or `th` widths — let text-heavy columns breathe
- Row hover highlight for scanability

Status indicators (styled `<span>` elements — emoji are **slop**):
- Match/pass/yes: colored dot or checkmark with green background
- Gap/fail/no: colored dot or cross with red background
- Partial/warning: amber indicator
- Neutral/info: dim text or muted badge

Cell content:
- Wrap long text naturally — don't truncate or force single-line
- Use `<code>` for technical references within cells
- Secondary detail text in `<small>` with dimmed color
- Keep numeric columns right-aligned with `tabular-nums`

## Timeline / Roadmap Views

Vertical or horizontal timeline with a central line (CSS pseudo-element). Phase markers as circles on the line. Content cards branching left/right (alternating) or all to one side. Date labels on the line. Color progression from past (muted) to future (vivid).

## Dashboard / Metrics Overview

Card grid layout. Hero numbers large and prominent. Sparklines via inline SVG `<polyline>`. Progress bars via CSS `linear-gradient` on a div. For real charts (bar, line, pie), use **Chart.js via CDN** — see "Mark Specs", "Tooltips and Hit Targets", "Direct Labels", and "Webfont Measurement" in `libraries.md`, and give each chart the `<details>` table twin the skill's Quality Checks require. Values go on the marks and the legend is HTML; Chart.js's own legend fails the hit-target floor. KPI cards with trend indicators (up/down arrows, percentage deltas).

Most dashboard tiles are not charts. Run the "Is it even a chart?" gate in the skill's §2 per tile, not once for the page.

## Implementation Plans

For visualizing implementation plans, extension designs, or feature specifications. The goal is **understanding the approach**, not reading the full source code — so don't dump full files:

- Show **file structure with descriptions** — list functions/exports with one-line explanations
- Show **key snippets only** — the 5-10 lines that illustrate the core logic
- Use **collapsible sections** for full code if truly needed

**Code blocks require explicit formatting.** Without `white-space: pre-wrap`, code runs together into an unreadable wall. See "Code Blocks" in `css-patterns.md`.

Structure:
1. Overview/purpose (what problem does this solve?)
2. Flow diagram (Mermaid or CSS cards)
3. File structure with descriptions (not full code)
4. Key implementation details (snippets)
5. API/interface summary
6. Usage examples

## Documentation (READMEs, Library Docs, API References)

Generate this type in **Handbook Mode** (see `../SKILL.md`); its layout is `../templates/handbook.html`.

Extract the prose structure into visual elements:

| Content | Visual Treatment |
|---------|------------------|
| Features | Card grid (2-3 columns) |
| Install/setup steps | Numbered cards or vertical flow |
| API endpoints/commands | Table with sticky header |
| Config options | Table |
| Architecture | Mermaid diagram or CSS card layout |
| Comparisons | Side-by-side panels or table |
| Warnings/notes | Callout boxes |

Don't just format the prose — transform it. A feature list becomes a card grid. Install steps become a numbered flow. An API reference becomes a table.

## Prose Accent Elements

Use sparingly within visual pages to highlight key points or provide breathing room. See "Prose Page Elements" in `css-patterns.md` for CSS patterns.

- **Lead paragraph** — larger intro text to set context before diving into cards/grids
- **Pull quote** — highlight a key insight; one per page maximum
- **Callout box** — warnings, tips, important notes
- **Section divider** — visual break between major sections

**When to use:** A visual page explaining an essay might use a lead paragraph for the thesis, then cards for key arguments. A README visualization might use callout boxes for warnings but otherwise stay card/table-focused.
