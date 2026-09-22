# Mermaid Rules

Read before generating any page containing a Mermaid diagram. This file owns the container, the config, and the constraint list — the one place they live. Theming values and diagram syntax are in `libraries.md`; the theme toggle itself is in `css-patterns.md`.

## Reach for HTML instead

Mermaid earns its place when edges need automatic routing. Build the figure from HTML and CSS when the shape is fixed and you can place it yourself — layered stacks, matrices, timelines, legends, annotated sequences, anything that is really a grid.

Two measurements decide it, both taken on the rendered diagram:

- **Taller than 2:1** — a column-width figure scales it to fit, and the labels go with it. Restructure it, split it, or build it in HTML.
- **More than 12 nodes** — readability collapses regardless of font size. Use the hybrid pattern (see "Architecture" in `diagram-types.md`).

An HTML figure is measured by the browser that paints it, so it cannot blow up or drift. That reliability is the reason to prefer it whenever the topology does not need a layout engine.

## The blow-up

**A blow-up is a diagram that renders unreadably small.** Mermaid lays out in its own coordinate space; anything that inflates that space shrinks the content inside it.

- **`layout: 'elk'`** — mis-measures labels in some environments and scatters tiny nodes across a giant canvas. Use the default dagre layout.
- **Mixed subgraph `direction`** — keep one direction for the whole graph. A per-subgraph override (`direction LR` inside a `flowchart TD`) gives each subgraph its own coordinate space, and depending on the viewer's font metrics the outer nodes land thousands of px apart. It renders fine in some browsers and blows up in others, so local testing will not catch it.
- **`LR` on a complex graph** — spreads horizontally until labels are unreadable. Prefer `flowchart TD`; keep `LR` for linear flows of 3–4 nodes.
- **Extreme aspect ratio** — a long chain or a wide fan-out fits small by definition. See "Reach for HTML instead".

## Drift

**Drift is Mermaid measuring a label at one size and the browser painting it at another.** The layout is computed from the measurement, so the painted content lands outside the `viewBox` Mermaid derived: the figure clips on one side and shows dead space on the other, and node boxes cut their own text off. It reproduces only on the reader's machine, because it depends on which fonts resolved and when.

Three sources, all closed by the recipe below:

- **A CSS font rule on `.nodeLabel` or `.edgeLabel`** — it applies after measurement. Set label fonts in `themeVariables`, the one place measurement and paint both read.
- **`htmlLabels: true`** — wraps every label in a `foreignObject` whose size browsers report inconsistently. `htmlLabels: false` measures SVG text with `getBBox`, which cannot disagree with itself.
- **Webfonts arriving after render** — `document.fonts.ready` resolves before a face the page has not yet painted is fetched, so Mermaid measures the fallback metric. Load the exact faces first.

## Container structure

The diagram renders at its natural size and scales down to the column width, keeping its aspect ratio. Fitting width **and** height into a box is what made diagrams unreadable; fit width only and let the height run.

```html
<figure class="diagram">
<pre class="mermaid">
graph TD
  A["First line&lt;br/&gt;second line"] --&gt;|"Edge.Label"| B["Outcome"]
</pre>
  <figcaption class="diagram__caption">What the reader should take from it</figcaption>
</figure>
```

Write `&lt;br/&gt;` and `--&gt;`, not `<br/>` and `-->`. The HTML parser turns a literal `<br/>` inside the `<pre>` into an element, and `textContent` then drops it and runs the two label lines together.

```css
.diagram { background: var(--surface); border: 1px solid var(--border);
           border-radius: 12px; padding: 30px 22px; overflow-x: auto; }
.diagram .mermaid { display: flex; justify-content: safe center; min-height: 40px; }
.diagram .mermaid svg { max-width: 100%; height: auto; display: block; }
.mermaid .node rect, .mermaid .node polygon { stroke-width: 1.5px !important; }
```

Style the shapes, and leave the label fonts to `themeVariables` — see "Drift".

## The config

```js
mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  flowchart: { useMaxWidth: false, htmlLabels: false, wrappingWidth: 320 },
  sequence: { useMaxWidth: false },
  htmlLabels: false,
  markdownAutoWrap: false,
  themeVariables: { fontFamily: "'IBM Plex Sans', system-ui, sans-serif", fontSize: '17px', /* palette */ }
});
```

Render through these steps, in order:

```js
async function fontsSettled() {
  if (!document.fonts) return;
  const faces = ["17px 'IBM Plex Sans'", "600 17px 'IBM Plex Sans'"];
  try { await Promise.all(faces.map(f => document.fonts.load(f))); await document.fonts.ready; }
  catch (e) { /* proceed with fallback metrics */ }
}

async function renderDiagrams() {
  await fontsSettled();
  await mermaid.run({ querySelector: '.mermaid' });
  document.querySelectorAll('.diagram svg').forEach(svg => {
    let box; try { box = svg.getBBox(); } catch (e) { return; }
    if (!box || !box.width) return;
    const pad = 8, w = box.width + pad * 2, h = box.height + pad * 2;
    svg.setAttribute('viewBox', (box.x - pad) + ' ' + (box.y - pad) + ' ' + w + ' ' + h);
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svg.removeAttribute('width'); svg.removeAttribute('height');
    svg.style.width = '100%'; svg.style.height = 'auto'; svg.style.aspectRatio = w + ' / ' + h;
  });
}
```

The `getBBox` pass re-derives the `viewBox` from what was actually painted, so content cannot fall outside it even if a label still drifts. Keep each diagram's source in `dataset.source` before the first run, so a re-render has something to re-read.

Reaching a diagram larger than the column is the browser's job: the page scrolls, and the reader zooms. Pages carry no zoom, pan or fit engine of their own.

## Theming

Always `theme: 'base'` with custom `themeVariables` so colors match the page palette.

Mermaid bakes its colors into the SVG at render time, so a CSS variable swap cannot recolor it — the page's theme toggle must re-initialize and re-render on `themechange`. See "Theme Toggle" in `css-patterns.md`.

## Labels

Break long labels yourself with `&lt;br/&gt;`, including file paths and dotted event names: `markdownAutoWrap: false` leaves every break under your control, and auto-wrap splits `Documents.Document.Uploaded` mid-word. Break at a natural boundary such as a dot.

"Writing Valid Mermaid" in `libraries.md` owns the syntax rules — quoting special characters, node IDs.

## CSS class collision

**Keep `.node` scoped under `.mermaid`.** Mermaid uses `.node` internally on SVG `<g>` elements with `transform: translate(x, y)` for positioning, so a page-level `.node` rule (hover transforms, box-shadows) leaks in and breaks the layout. Name card components `.ve-card`, and write diagram rules as `.mermaid .node rect`.
