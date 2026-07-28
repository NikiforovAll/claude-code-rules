# Mermaid Rules

Read before generating any page containing a Mermaid diagram. Theming values and syntax guidance live in `libraries.md`; this file is the constraint list.

## The blow-up

**A blow-up is a diagram that renders unreadably small.** Mermaid lays out in its own coordinate space, then the fit engine scales the whole canvas to fit the viewport — contain-only, so it always shows the *entire* diagram. Anything that inflates the canvas therefore shrinks the content. A zoom label in the single digits is a blow-up; the diagram is technically present and practically useless.

Five causes, all avoidable:

- **`layout: 'elk'`** — mis-measures HTML labels in some environments and scatters tiny nodes across a giant canvas. Use the default dagre layout.
- **Mixed subgraph `direction`** — never put a per-subgraph `direction` override (e.g. `direction LR` inside a `flowchart TD`). Each subgraph gets its own coordinate space and, depending on the viewer's font metrics, outer nodes can be flung thousands of px apart. It renders fine in some browsers and blows up in others, so you won't catch it locally. One direction for the whole graph.
- **`LR` on a complex graph** — spreads horizontally and makes labels unreadable. Prefer `flowchart TD`; reserve `LR` for simple 3-4 node linear flows.
- **Too many nodes** — beyond 10-12, readability collapses even with zoom and a larger `fontSize`. At 15+ elements don't try to scale: use the hybrid pattern (see "Architecture" in `diagram-types.md`).
- **Extreme aspect ratio** — a long top-down chain or a wide fan-out fits small by definition. Keep the shape moderate rather than leaning on scale. (A tall or wide diagram legitimately reading under 50% is *not* a blow-up — contain-only fit is working as designed.)

For 10-12 nodes, raise `fontSize` in `themeVariables` to 18-20px.

## Container structure

**Never use bare `<pre class="mermaid">`.** It renders but has no zoom/pan controls — diagrams become tiny and unusable. Use the full `diagram-shell` pattern from `../templates/mermaid-flowchart.html`: the HTML structure (`.diagram-shell` > `.mermaid-wrap` > `.zoom-controls` + `.mermaid-viewport` > `.mermaid-canvas`), the CSS, and the ~200-line JS module for zoom/pan/fit. Copy it wholesale.

Center every diagram with `display: flex; justify-content: center;`. Every `.mermaid-wrap` gets the zoom controls for its medium: on pages and documents the five-button set from `css-patterns.md` "Zoom Controls", in decks the four-button set from `slide-patterns.md` "Diagram Slide". Both end at ⛶ / `openInNewTab()`.

## Theming

Always `theme: 'base'` with custom `themeVariables` so colors match the page palette. Override Mermaid's SVG classes with CSS for pixel-perfect control. Full theming guide in `libraries.md`.

Mermaid bakes its colors into the SVG at render time, so a CSS variable swap can't recolor it — the page's theme toggle must re-initialize and re-render on `themechange`. See "Theme Toggle" in `css-patterns.md`.

## Labels

Break long single-line labels and file paths, not just multi-line content: a line wider than its box gets clipped when the viewer's real font is wider than the render-time measurement.

"Writing Valid Mermaid" in `libraries.md` owns the syntax rules — `<br/>` vs `\n`, quoting special characters, node IDs. Read it before writing diagram source.

## CSS class collision

**Never define `.node` as a page-level CSS class.** Mermaid uses `.node` internally on SVG `<g>` elements with `transform: translate(x, y)` for positioning. Page-level `.node` styles (hover transforms, box-shadows) leak into diagrams and break layout. Use the namespaced `.ve-card` class for card components. The only safe way to style Mermaid's `.node` is scoped under `.mermaid` (e.g. `.mermaid .node rect`).
