# External Libraries (CDN)

Optional CDN libraries for cases where pure CSS/HTML isn't enough. Only include what the diagram actually needs — most diagrams need zero external JS.

## Mermaid.js — Diagramming Engine

Use for flowcharts, sequence diagrams, ER diagrams, state machines, mind maps, class diagrams, and any diagram where automatic node positioning and edge routing saves effort. Mermaid handles layout — you handle theming.

Do NOT use for dashboards — CSS Grid card layouts with Chart.js look better for those. Data tables use `<table>` elements.

**CDN (UMD build — use this, not the ESM `.mjs` build):**
```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"
        onerror="document.querySelectorAll('.zoom-label').forEach(function (l) { l.textContent = 'Error: Mermaid failed to load (offline or CDN blocked)'; })"></script>
<script>
  mermaid.initialize({ startOnLoad: true, /* ... */ });
</script>
```

The UMD build exposes a `mermaid` global and its `onerror` hook makes CDN failures visible. A static ESM `import` that fails (offline, blocked CDN) kills the entire module script silently — the page hangs on "Loading..." with no error and no way to diagnose it.

**ELK layout — do not use.** `layout: 'elk'` (the separate `@mermaid-js/layout-elk` package) mis-measures HTML labels in some environments and produces a giant canvas with tiny scattered nodes — observed: the same 16-node flowchart rendered at viewBox 7557×21070 with ELK vs 825×1342 with dagre. The default dagre layout renders correctly everywhere. If you believe a diagram truly needs ELK, verify the output visually in a real browser AND headless before delivering.

### Deep Theming

Always use `theme: 'base'` — it's the only theme where all `themeVariables` are fully customizable. The built-in themes (`default`, `dark`, `forest`, `neutral`) ignore most variable overrides.

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  // Read the live theme from the attribute the toggle sets — never matchMedia,
  // which can't see the user's override.
  const isDarkTheme = () => document.documentElement.getAttribute('data-theme') === 'dark';
  const isDark = isDarkTheme();
  mermaid.initialize({
    startOnLoad: true,
    theme: 'base',
    look: 'classic',
    themeVariables: {
      // Background and surfaces — teal/slate palette (not violet/indigo!)
      primaryColor: isDark ? '#134e4a' : '#ccfbf1',
      primaryBorderColor: isDark ? '#14b8a6' : '#0d9488',
      primaryTextColor: isDark ? '#f0fdfa' : '#134e4a',
      secondaryColor: isDark ? '#1e293b' : '#f0fdf4',
      secondaryBorderColor: isDark ? '#059669' : '#16a34a',
      secondaryTextColor: isDark ? '#f1f5f9' : '#1e293b',
      tertiaryColor: isDark ? '#27201a' : '#fef3c7',
      tertiaryBorderColor: isDark ? '#d97706' : '#f59e0b',
      tertiaryTextColor: isDark ? '#fef3c7' : '#27201a',
      // Lines and edges
      lineColor: isDark ? '#64748b' : '#94a3b8',
      // Text
      fontSize: '16px',
      fontFamily: 'var(--font-body)',
      // Notes and labels
      noteBkgColor: isDark ? '#1e293b' : '#fefce8',
      noteTextColor: isDark ? '#f1f5f9' : '#1e293b',
      noteBorderColor: isDark ? '#fbbf24' : '#d97706',
    }
  });
</script>
```

**FORBIDDEN in Mermaid themeVariables:** `#8b5cf6`, `#7c3aed`, `#a78bfa` (indigo/violet), `#d946ef` (fuchsia). Use teal, slate, amber, emerald, or colors from your page's palette.

### CSS Overrides on Mermaid SVG

Mermaid renders SVG. Override its classes for pixel-perfect control that `themeVariables` can't reach:

```css
/* Container — see css-patterns.md "Zoom Controls" for the full zoom pattern */
.mermaid-wrap {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  overflow: auto;
}

/* CRITICAL: Force node/edge text to follow the page's color scheme.
   Without this, themeVariables.primaryTextColor works for DEFAULT nodes,
   but any classDef that sets color: will hardcode a single value that
   breaks in the opposite color scheme. Fix: never set color: in classDef,
   and always include these CSS overrides. */
.mermaid .nodeLabel { color: var(--text) !important; }
.mermaid .edgeLabel { color: var(--text-dim) !important; background-color: var(--bg) !important; }
.mermaid .edgeLabel rect { fill: var(--bg) !important; }

/* Node shapes */
.mermaid .node rect,
.mermaid .node circle,
.mermaid .node polygon {
  stroke-width: 1.5px;
}

/* Edge paths */
.mermaid .edge-pattern-solid {
  stroke-width: 1.5px;
}

/* Edge labels — smaller than node labels for visual hierarchy */
.mermaid .edgeLabel {
  font-family: var(--font-mono) !important;
  font-size: 13px !important;
}

/* Node labels — 16px default; drop to 14px for complex diagrams (20+ nodes) */
.mermaid .nodeLabel {
  font-family: var(--font-body) !important;
  font-size: 16px !important;
}

/* Sequence diagram actors */
.mermaid .actor {
  stroke-width: 1.5px;
}

/* Sequence diagram messages */
.mermaid .messageText {
  font-family: var(--font-mono) !important;
  font-size: 12px !important;
}

/* ER diagram entities */
.mermaid .er.entityBox {
  stroke-width: 1.5px;
}

/* Mind map nodes */
.mermaid .mindmap-node rect {
  stroke-width: 1.5px;
}
```

### classDef and style Gotchas

`classDef` values and per-node `style` directives are static text inside `<pre>` — they can't use CSS variables or JS ternaries. Two rules:

1. **Never set `color:` in classDef or per-node `style` directives.** It hardcodes a text color that breaks in the opposite color scheme. This applies to both `classDef highlight fill:...,color:#2c2a25` and `style I fill:...,color:#2c2a25`. Let the CSS overrides above handle text color via `var(--text)`.

2. **Use semi-transparent fills (8-digit hex) for node backgrounds.** They layer over whatever Mermaid's base theme background is, producing a tint that works in both light and dark modes. Use `20`–`44` alpha for subtle, `55`–`77` for prominent:

```
classDef highlight fill:#b5761433,stroke:#b57614,stroke-width:2px
classDef muted fill:#7c6f6411,stroke:#7c6f6444,stroke-width:1px
```

### Node Label Special Characters

Mermaid uses certain characters for shape syntax. Node labels containing these characters cause syntax errors unless quoted.

**Shape characters to watch:**
- `[/text/]` — parallelogram
- `[\text\]` — trapezoid (alt)
- `[/text\]` — trapezoid
- `[\text/]` — trapezoid (alt)
- `[(text)]` — cylindrical
- `[[text]]` — subroutine
- `((text))` — circle
- `{{text}}` — hexagon

**If your node label starts with `/`, `\`, `(`, or `{`, wrap it in quotes:**

```
%% WRONG — syntax error (/ starts parallelogram shape)
CMD[/gallery command] --> SRV[server]

%% RIGHT — quotes escape the special character
CMD["/gallery command"] --> SRV[server]
```

**Edge labels with special characters also need quotes:**

```
%% WRONG — quotes inside edge label
UI -->|"Use as Reference"| RET

%% RIGHT — use single quotes or escape
UI -->|'Use as Reference'| RET
UI -->|Use as Reference| RET
```

Avoid opaque light fills like `fill:#fefce8` — they render as bright boxes in dark mode.

### stateDiagram-v2 Label Limitations

State diagram transition labels have a strict parser. Avoid:
- `<br/>` — only works in flowcharts; causes a parse error in state diagrams
- Parentheses in labels — `cancel()` can confuse the parser
- Multiple colons — the first `:` is the label delimiter; extra colons in the label text may break parsing

If you need multi-line labels or special characters, use a `flowchart` instead of `stateDiagram-v2`. Flowcharts support quoted labels (`|"label with: special chars"|`) and `<br/>` for line breaks.

### Writing Valid Mermaid

Most Mermaid failures come from a few recurring issues. Follow these rules to avoid invalid diagrams:

**For multi-line flowchart node labels, use `<br/>` (not `\n`).** Mermaid flowcharts interpret `<br/>` as a line break, but escaped `\n` in labels often renders as literal text:

```
%% WRONG — renders literal "\n" in node text
A["Copilot Backend\n/api + /api/voicebot"] --> B["Redis"]

%% RIGHT — renders on two lines
A["Copilot Backend<br/>/api + /api/voicebot"] --> B["Redis"]
```

**Quote labels with special characters.** Parentheses, colons, commas, brackets, and ampersands break the parser when unquoted. Wrap any label containing special characters in double quotes:

```
A["handleRequest(ctx)"] --> B["DB: query users"]
A[handleRequest] --> B[query users]
```

**Keep IDs simple.** Node IDs should be alphanumeric with no spaces or punctuation. Put the readable name in the label, not the ID:

```
userSvc["User Service"] --> authSvc["Auth Service"]
```

**Max 10-12 nodes per diagram** — beyond that you get a **blow-up** (see `mermaid-rules.md`). Use `subgraph` blocks to group related nodes when under the limit:

```
subgraph Auth
  login --> validate --> token
end
subgraph API
  gateway --> router --> handler
end
Auth --> API
```

**Arrow styles for semantic meaning:**

| Arrow | Meaning | Use for |
|-------|---------|---------|
| `-->` | Solid | Primary flow |
| `-.->` | Dotted | Optional, async, or fallback paths |
| `==>` | Thick | Critical or highlighted path |
| `--x` | Cross | Rejected or blocked |
| `-->\|label\|` | Labeled | Decision branches, data descriptions |

**Escape pipes in labels.** If a label contains a literal `|`, use `#124;` (HTML entity) or rephrase to avoid it — pipes delimit edge labels in flowcharts.

**Sequence diagram messages must be plain text.** Unlike flowchart labels, sequence diagram messages (the text after `:`) cannot be quoted or escaped. Curly braces `{}`, square brackets `[]`, angle brackets `<>`, and `&` will silently break the parser and the entire diagram renders as raw text. Write human-readable descriptions, not code:

```
%% WRONG — parser chokes on braces, brackets, ampersand
A->>B: web_search({ queries: [...] })
B->>B: User removes query 2, keeps 1 & 3
B->>S: POST /submit { selected: [0, 2] }

%% RIGHT — plain English, no special characters
A->>B: Call web_search with queries
B->>B: User removes query 2, keeps 1 and 3
B->>S: POST /submit with selected indices
```

**Don't mix diagram syntax.** Each diagram type has its own syntax. `-->` works in flowcharts but not in sequence diagrams (`->>` instead). `:::className` works in flowcharts but not in ER diagrams. When in doubt, check the examples below for correct syntax per type.

### Layout Direction: TD vs LR

`flowchart LR` (left-to-right) spreads horizontally. With many nodes, Mermaid scales everything down to fit the width, making text unreadable. `flowchart TD` (top-down) is almost always better.

**When to use each:**

| Direction | Use when | Avoid when |
|-----------|----------|------------|
| `TD` (top-down) | Complex diagrams, 5+ nodes, hierarchies, architecture | Simple A→B→C linear flows |
| `LR` (left-to-right) | Simple linear flows, 3-4 nodes, pipelines | Complex graphs, many branches |

**Rule of thumb:** If the diagram has more than one row of nodes or any branching, use `TD`. The extra vertical space makes labels readable.

```
%% WRONG — LR with many nodes produces wide, short, unreadable diagram
flowchart LR
  A --> B --> C --> D --> E
  A --> F --> G --> H
  
%% RIGHT — TD uses vertical space, labels stay readable
flowchart TD
  A --> B --> C --> D --> E
  A --> F --> G --> H
```

### Diagram Type Examples

**Flowchart with decisions:**
```html
<pre class="mermaid">
graph TD
  A[Request] --> B{Authenticated?}
  B -->|Yes| C[Load Dashboard]
  B -->|No| D[Login Page]
  D --> E[Submit Credentials]
  E --> B
  C --> F{Role?}
  F -->|Admin| G[Admin Panel]
  F -->|User| H[User Dashboard]
</pre>
```

**Sequence diagram:**
```html
<pre class="mermaid">
sequenceDiagram
  participant C as Client
  participant G as Gateway
  participant S as Service
  participant D as Database
  C->>G: POST /api/data
  G->>G: Validate JWT
  G->>S: Forward request
  S->>D: Query
  D-->>S: Results
  S-->>G: Response
  G-->>C: 200 OK
</pre>
```

**ER diagram:**
```html
<pre class="mermaid">
erDiagram
  USERS ||--o{ ORDERS : places
  ORDERS ||--|{ LINE_ITEMS : contains
  LINE_ITEMS }o--|| PRODUCTS : references
  USERS { string email PK }
  ORDERS { int id PK }
  LINE_ITEMS { int quantity }
  PRODUCTS { string name }
</pre>
```

**State diagram:**
```html
<pre class="mermaid">
stateDiagram-v2
  [*] --> Draft
  Draft --> Review : submit
  Review --> Approved : approve
  Review --> Draft : request_changes
  Approved --> Published : publish
  Published --> Archived : archive
  Archived --> [*]
</pre>
```

**Mind map:**
```html
<pre class="mermaid">
mindmap
  root((Project))
    Frontend
      React
      Next.js
      Tailwind
    Backend
      Node.js
      PostgreSQL
      Redis
    Infrastructure
      AWS
      Docker
      Terraform
</pre>
```

**Class diagram:**
```html
<pre class="mermaid">
classDiagram
  class User {
    +string email
    +string name
    +login()
    +logout()
  }
  class Order {
    +int id
    +decimal total
    +submit()
  }
  class Product {
    +string name
    +decimal price
  }
  User "1" --> "*" Order : places
  Order "*" --> "*" Product : contains
</pre>
```

**C4 architecture (flowchart-as-C4):**
```html
<pre class="mermaid">
graph TD
  user("👤 User<br/><small>Browser client</small>")
  subgraph boundary["Web Platform"]
    app["Web App<br/><small>Node.js</small>"]
    db[("Database<br/><small>PostgreSQL</small>")]
  end
  email["📧 Email Service"]:::ext
  payment["💳 Payment Gateway"]:::ext
  user -->|"HTTPS"| app
  app -->|"SQL"| db
  app -->|"SMTP"| email
  app -->|"API"| payment
  classDef ext fill:none,stroke-dasharray:5 5
</pre>
```

Do NOT use native `C4Context` / `C4Container` syntax — it hardcodes sharp corners, its own font, and inline colors that ignore `themeVariables`. Use `graph TD` + `subgraph` for C4 boundaries instead; it inherits all theme settings automatically.

### Which Mermaid Diagram Type?

Quick-reference for choosing the right Mermaid syntax:

| You want to show... | Use | Syntax keyword |
|---|---|---|
| Process flow, decisions, pipelines | Flowchart | `graph TD` / `graph LR` |
| Request/response, API calls, temporal interactions | Sequence diagram | `sequenceDiagram` |
| Database tables and relationships | ER diagram | `erDiagram` |
| OOP classes, domain models with methods | Class diagram | `classDiagram` |
| System architecture at multiple zoom levels | C4 diagram | `graph TD` + `subgraph` (not native `C4Context`) |
| State transitions, lifecycles | State diagram | `stateDiagram-v2` |
| Hierarchical breakdowns, brainstorms | Mind map | `mindmap` |

### Dark Mode Handling

Mermaid bakes its colors into the SVG at render time, so a CSS variable swap can't recolor an existing diagram — it must be re-rendered. Put the config in a function, read the theme from the `data-theme` attribute (never `matchMedia`, which can't see the user's toggle choice), and re-render on the `themechange` event the toggle dispatches:

```javascript
const isDarkTheme = () => document.documentElement.getAttribute('data-theme') === 'dark';

function mermaidConfig() {
  const isDark = isDarkTheme();
  return { startOnLoad: false, theme: 'base', look: 'classic', themeVariables: { /* isDark ? ... : ... */ } };
}

mermaid.initialize(mermaidConfig());

addEventListener('themechange', () => {
  mermaid.initialize(mermaidConfig());
  render();   // re-render from the preserved .diagram-source, per mermaid-flowchart.html
});
```

Anything else that reads the theme at load time — `openInNewTab()`'s export background, Chart.js colors — must be recomputed the same way, at use time or on `themechange`. CSS overrides on the container (`.mermaid-wrap`) follow the attribute automatically since they use custom properties.

## Chart.js — Data Visualizations

Use for bar charts, line charts, pie/doughnut charts, radar charts, and other data-driven visualizations in dashboard-type diagrams. Overkill for static numbers — use pure SVG/CSS for simple progress bars and sparklines. Check "Is it even a chart?" in the skill's §2 before reaching for this section at all.

### Mark Specs

Chart.js defaults are tuned to look busy in a demo, not correct on a designed page. Override them:

| Mark | Spec | Why |
|---|---|---|
| Bar thickness | `maxBarThickness: 24` | A bar wider than its label reads as a block of color, not a measured quantity |
| Line width | `borderWidth: 2` | 1px disappears on a tinted surface; 3px+ makes the ink louder than the trend |
| Mark borders | `borderWidth: 0` on bars, points, arcs | A stroke around a filled mark is ink that isn't data. Separate adjacent marks with a 2px gap of surface color instead |
| Point radius | `pointRadius: 0`, `pointHoverRadius: 4` | Dots on a dense line are noise; keep them for the hover target only |
| Grid | one axis only, solid hairline in `--border` | Dashed grid lines compete with dashed data lines. Grid on the value axis, none on the category axis |
| Axis borders | `border: { display: false }` | The grid already implies the frame |

Fill opacity belongs at the palette level, not per-dataset: a series color at full strength with a `~15%` companion for area fills keeps the line legible over its own fill.

### Tooltips and Hit Targets

**Tooltips enhance, never gate.** Anything a reader *needs* — the value of the tallest bar, the label of the outlier, the total — is on the page as a direct label, an axis tick, or a KPI card. A tooltip carries the second-order detail: exact figures, timestamps, an extra dimension. A number reachable only by hover is unreachable on touch, in print, and by keyboard.

**Interactive targets are at least 24px** in their smallest dimension — chart hover regions, legend toggles, zoom controls, theme toggle. Under that, the control works with a mouse and fails with a thumb. Chart.js: widen the grab area with `interaction: { mode: 'index', intersect: false }` rather than by enlarging the marks.

**Build the legend in HTML, not Chart.js.** Its built-in legend draws ~12px swatches and makes each one a click-to-hide toggle — a sub-24px target on a control that silently deletes a series when a thumb lands on it. Set `plugins: { legend: { display: false } }` and put the key in markup beside the canvas, where it inherits the page's type, wraps at narrow widths, and survives print and screen readers:

```html
<div class="legend">
  <span><i style="background:var(--c1)"></i>references/</span>
  <span><i style="background:var(--c2)"></i>templates/</span>
</div>
```
```css
.legend { display: flex; flex-wrap: wrap; gap: 6px 18px; margin-top: 14px; font-size: 12.5px; color: var(--text-dim); }
.legend span { display: inline-flex; align-items: center; gap: 7px; }
.legend i { width: 11px; height: 11px; border-radius: 3px; flex: 0 0 auto; }
```

A single-series chart needs no legend at all — the caption names what the bars are.

### Direct Labels

"Tooltips never gate" is unenforceable without a way to draw the values, and Chart.js ships no built-in for it. Register one plugin and every value lands on the page:

```js
const valueLabels = {
  id: 'valueLabels',
  afterDatasetsDraw(chart, _args, opts) {
    const { ctx } = chart;
    // Horizontal bars get the label past the bar end; vertical bars get it above.
    const horizontal = chart.options.indexAxis === 'y';
    ctx.save();
    ctx.font = '600 11px ' + opts.font;
    ctx.fillStyle = opts.color;
    ctx.textAlign = horizontal ? 'left' : 'center';
    ctx.textBaseline = horizontal ? 'middle' : 'bottom';
    chart.data.datasets.forEach((ds, di) => {
      chart.getDatasetMeta(di).data.forEach((mark, i) => {
        const v = ds.data[i];
        if (v == null) return;
        const text = opts.fmt ? opts.fmt(v) : String(v);
        ctx.fillText(text, horizontal ? mark.x + 8 : mark.x, horizontal ? mark.y : mark.y - 6);
      });
    });
    ctx.restore();
  }
};
Chart.register(valueLabels);
```

Per chart, pass its options and reserve room — a label drawn past the chart area is clipped at the canvas edge. `padding.right` for horizontal bars, `padding.top` for vertical:

```js
options: {
  layout: { padding: { right: 56 } },   // room for the widest label
  plugins: {
    valueLabels: { color: inkColor, font: fontFamily, fmt: v => v.toLocaleString() },
  }
}
```

Registering globally runs it on *every* chart, including ones where labels would collide — a scatter of 13 points, a dense line. Opt those out with `plugins: { valueLabels: false }` and let the table twin carry the numbers.

Prefer horizontal bars when the category names are long: each label gets a full text line instead of a column's width, and the values read down a clean edge.

### Webfont Measurement

Chart.js measures tick labels at construction time with whatever font is resolved *then*. Build before the webfont lands and the axis is sized for the fallback metrics, so the widest category label is drawn clipped at the canvas edge — a defect that never appears in the console and only shows up in a screenshot.

Build once, then again when the font is ready:

```js
build();
if (document.fonts && document.fonts.ready) document.fonts.ready.then(build);
addEventListener('themechange', build);   // same function; see the theme note above
```

`build()` must `destroy()` its previous instances or they stack up on the same canvas. When one label still dominates the axis, claim the width outright and shorten it on small viewports rather than letting it clip:

```js
y: {
  ticks: {
    ...tickStyle,
    callback(v) {                      // ellipsis reads as a decision; a clip reads as a bug
      const s = this.getLabelForValue(v);
      return this.chart.width > 560 || s.length <= 15 ? s : s.slice(0, 14) + '…';
    }
  },
  afterFit: s => { if (s.chart.width > 560) s.width = Math.max(s.width, 176); }
}
```

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>

<canvas id="myChart" width="600" height="300"></canvas>

<script>
  // Attribute, not matchMedia — the toggle's choice must win.
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const textColor = isDark ? '#8b949e' : '#6b7280';
  const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';
  const fontFamily = getComputedStyle(document.documentElement)
    .getPropertyValue('--font-body').trim() || 'system-ui, sans-serif';

  new Chart(document.getElementById('myChart'), {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
      datasets: [{
        label: 'Feedback Items',
        data: [45, 62, 78, 91, 120],
        backgroundColor: isDark ? 'rgba(129, 140, 248, 0.6)' : 'rgba(79, 70, 229, 0.6)',
        borderWidth: 0,
        borderRadius: 4,
        maxBarThickness: 24,
      }]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      layout: { padding: { top: 18 } },   // room for the value labels
      plugins: {
        // One series, so no key is needed; a multi-series chart gets an HTML
        // legend instead — see "Tooltips and Hit Targets".
        legend: { display: false },
        valueLabels: { color: textColor, font: fontFamily },
      },
      scales: {
        // Grid on the value axis only — see Mark Specs.
        x: { ticks: { color: textColor, font: { family: fontFamily } }, grid: { display: false }, border: { display: false } },
        y: { ticks: { color: textColor, font: { family: fontFamily } }, grid: { color: gridColor }, border: { display: false } },
      }
    }
  });
</script>
```

Wrap the canvas in a styled container:
```css
.chart-container {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  position: relative;
}

.chart-container canvas {
  max-height: 300px;
}
```

## anime.js — Orchestrated Animations

Use when a diagram has 10+ elements and you want a choreographed entrance sequence (staggered reveals, path drawing, count-up numbers). For simpler diagrams, CSS `animation-delay` staggering is sufficient.

```html
<script src="https://cdn.jsdelivr.net/npm/animejs@3.2.2/lib/anime.min.js"></script>

<script>
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!prefersReduced) {
    anime({
      targets: '.ve-card',
      opacity: [0, 1],
      translateY: [20, 0],
      delay: anime.stagger(80, { start: 200 }),
      easing: 'easeOutCubic',
      duration: 500,
    });

    anime({
      targets: '.connector path',
      strokeDashoffset: [anime.setDashoffset, 0],
      easing: 'easeInOutCubic',
      duration: 800,
      delay: anime.stagger(150, { start: 600 }),
    });

    document.querySelectorAll('[data-count]').forEach(el => {
      anime({
        targets: { val: 0 },
        val: parseInt(el.dataset.count),
        round: 1,
        duration: 1200,
        delay: 400,
        easing: 'easeOutExpo',
        update: (anim) => { el.textContent = anim.animations[0].currentValue; }
      });
    });
  }
</script>
```

When using anime.js, set initial opacity to 0 in CSS so elements don't flash before the animation:
```css
.ve-card { opacity: 0; }

@media (prefers-reduced-motion: reduce) {
  .ve-card { opacity: 1 !important; }
}
```

## Google Fonts — Typography

Always load with `display=swap` for fast rendering. Pick a distinctive pairing — body + mono at minimum, optionally a display font for the title.

Forbidden `--font-body` values are listed under Typography in the skill's Anti-Patterns.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
```

Define as CSS variables for easy reference:
```css
:root {
  --font-body: 'Outfit', system-ui, sans-serif;
  --font-mono: 'Space Mono', 'SF Mono', Consolas, monospace;
}
```

**Font pairings** (rotate — never use the same pairing twice in a row):

| Rec | Body / Headings | Mono / Labels | Feel | Use for |
|---|---|---|---|---|
| ✓ | DM Sans | Fira Code | Friendly, developer | Blueprint, technical docs |
| ✓ | Crimson Pro | Noto Sans Mono | Editorial, refined — set headlines at 600 | The `editorial` direction, plan reviews, decision logs |
| ✓ | IBM Plex Sans | IBM Plex Mono | Reliable, readable | Architecture diagrams |
| ✓ | Bricolage Grotesque | Fragment Mono | Bold, characterful | Data tables, dashboards |
| ✓ | Plus Jakarta Sans | Azeret Mono | Rounded, approachable | Status reports, audits |
| | Outfit | Space Mono | Clean geometric, modern | Flowcharts, pipelines |
| | Sora | IBM Plex Mono | Technical, precise | ER diagrams, schemas |
| | Instrument Serif | JetBrains Mono | Display serif, high contrast | Pull quotes, covers, mastheads, slides — **not body text on a scrollable page** |
| | Fraunces | Source Code Pro | Warm, distinctive | Project recaps |
| | Geist | Geist Mono | Vercel-inspired, sharp | Modern API docs |
| | Red Hat Display | Red Hat Mono | Cohesive family | System overviews |
| | Libre Franklin | Inconsolata | Classic, reliable | Data-dense tables |
| | Playfair Display | Roboto Mono | Elegant contrast | Executive summaries |

The **Rec** rows are recommended for most use cases. Vary across consecutive diagrams.

The mark rides the row rather than its position, so reordering this table cannot silently change what is recommended — an earlier "the first 5 pairings" claim did exactly that when a row was inserted above it. SKILL.md's "Good pairings (use these)" list mirrors these five, so adding or removing a mark means editing the skill too. A display face like Instrument Serif or Playfair Display is never marked, because the mark means "safe as a body stack at reading size" and they aren't — they hold up on a masthead or a slide, and go limp below roughly 16px. Listed is not the same as recommended.

### Typography by Content Voice

For prose-heavy pages (documentation, articles, essays), match typography to the content's voice:

| Voice | Fonts | Best For |
|-------|-------|----------|
| **Literary / Thoughtful** | Literata, Lora, Newsreader, Merriweather | Essays, personal posts, long-form articles |
| **Technical / Precise** | IBM Plex Sans + Mono, Geist + Geist Mono, Source family | Documentation, READMEs, API references |
| **Bold / Contemporary** | Bricolage Grotesque, Space Grotesk, DM Sans | Product pages, feature announcements |
| **Minimal / Focused** | Source Serif 4 + Source Sans 3, Karla + Inconsolata | Tutorials, how-tos, focused reading |

**Literata** deserves special mention — it has optical sizing designed specifically for screen reading. Google's answer to Georgia, but modernized.
