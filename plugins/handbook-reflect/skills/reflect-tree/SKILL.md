---
name: reflect-tree
description: Visualize a Claude Code session as a quest/skill tree — a navigable SVG graph where nodes are turns and edges show flow, with distinct visual encoding for normal flow, dead-ends, corrections, retries, reversals, and backtracking. Sibling to /reflect (which produces an incidents+recommendations dashboard); this one shows the journey itself. Defaults to the current in-context session; optionally accepts a session ID or JSONL path. Use when the user invokes /reflect-tree or asks to map a session as a tree/graph/journey.
context: fork
argument-hint: `<current_session> or <session-id-or-path>`
---

# /reflect-tree — session quest-tree

Produce a single-file interactive HTML quest-tree of a Claude Code session. The vertical spine is the linear sequence of turns; back-edges and off-spine nodes encode wrong turns (corrections, retries, reversals, dead-ends, backtracks) so the user can see the whole journey at a glance — including detours and where the agent had to redo work.

This is a **sibling** to `/reflect`. Same input contract, different output: `/reflect` is a two-pane incidents/recommendations dashboard; `/reflect-tree` is a graph.

## When to use

- User invokes `/reflect-tree` (no args) → analyze the **current session** from the in-context conversation. Do **not** re-read the session JSONL — work from the agent's own memory.
- User invokes `/reflect-tree <session-id>` or `/reflect-tree <path-to-jsonl>` → run `scripts/analyze_session.py <path>` directly (this skill runs in a forked context — `context: fork` — so the compressed transcript is safe to ingest). The script outputs a compact markdown transcript: system reminders stripped, tool calls/results collapsed to one-liners, compaction blocks expanded with embedded user quotes. Then **you** classify each turn — the script does NOT classify, it only compresses.

Session JSONLs live under: `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`

## Node classifications

Each turn becomes a node. Pick the strongest applicable label:

- **normal** — routine forward progress (user request or assistant tool call/result with no problem)
- **correction** — user pushed back on an approach (`"no"`, `"don't"`, `"stop"`, `"actually"`)
- **retry** — agent ran the same tool/intent 2+ times with variations before it worked
- **reversal** — agent edited then unwound (Edit → revert, Write → delete)
- **dead-end** — tool failed because of the environment (missing binary, wrong path, OS mismatch)
- **backtrack** — agent abandoned a path and resumed from an earlier state
- **self-correction** — agent caught its own mistake mid-stream

## Edge types

- **flow** (default) — solid thin line between consecutive turns
- **back-edge** — curved dashed line from a retry/reversal/correction node back to the ancestor turn it relates to (color matches the classification)
- **backtrack** — curved solid arrow showing where the agent jumped back to
- **wasted-segment** — thicker grey edge with a `T12–T18 · 7 turns` label when many turns of fruitless searching collapse into one capsule

Each non-normal node carries a `refs` array listing the ancestor turn IDs it relates to.

## Knowledge mining (per-node insight)

Every node must carry an `insight` block — the **single most important, reusable lesson** from that turn, framed so a future agent could drop it into a prompt or rule. This is the value of the tree: each node becomes copyable knowledge.

For each turn, extract:

- **highlight** (1 line, ≤120 chars) — the single most important fact/decision/lesson. The "if you only read one thing from this turn" sentence.
- **insight** (2–5 lines) — the *why* behind the highlight. What the agent learned, what was non-obvious, what a future agent should do differently or keep doing. Phrase it as durable advice, not a play-by-play.
- **prompt_snippet** (copyable text) — a self-contained chunk a user could paste into CLAUDE.md, a memory file, or a future prompt. Must read independently of the tree (no "see T5" references). Format depends on the classification:
  - **correction / dead-end** → a rule: `- Always X, because Y` or a `<rule>` block
  - **retry / waste** → a recipe: the canonical command/path/tool that worked
  - **reversal / backtrack** → a guard: "Don't edit X — edit Y instead" with the reason
  - **self-correction** → a heuristic: "Before doing X, check Y"
  - **normal** (only the load-bearing ones — request, key decision, final answer) → a fact: the goal statement, the chosen approach, the outcome

Skip `prompt_snippet` for filler `normal` turns (routine Reads/Greps with no insight). Better to have 6 strong insights than 50 weak ones.

The HTML drawer renders these per-node with a **Copy insight** button that copies `prompt_snippet` to the clipboard. A header-level **Copy all insights** button assembles every node's `prompt_snippet` into one markdown document grouped by classification.

## Visual language

| Class            | Shape            | Color (CSS token)        | Symbol |
|------------------|------------------|--------------------------|--------|
| normal user      | filled circle    | `--accent`               | —      |
| normal assistant | open circle      | `--fg`                   | —      |
| correction       | diamond          | `--err` border           | `!`    |
| retry            | double ring      | `--warn`                 | `↻`    |
| reversal         | hollow square    | `--warn` dashed          | `⇄`    |
| dead-end         | filled X         | `--err`                  | `✕`    |
| backtrack        | arrow node       | `--muted` dashed         | `↶`    |
| self-correction  | small diamond    | `--ok` border            | `✓!`   |

X-position: normal = center spine; correction/reversal nudged left; retry/dead-end nudged right. This keeps the spine readable while making detours visually distinct.

A legend is rendered inline in the header.

### Collapsed-run capsule

When grouping consecutive `normal` turns into a capsule, render the **entire label inside the rounded rect** — turn-range, count, and topic together. Do not place the turn-range outside the box; it looks broken when the rect background only covers part of the label.

Pattern (SVG):

```html
<g class="capsule" transform="translate(300 380)">
  <rect x="-150" y="-13" width="300" height="26"/>
  <text x="0" y="0">
    <tspan class="turn-range">T120–T139</tspan> · 11 turns · refactor + INFRA_GUIDE.md
  </text>
</g>
```

The rect width must accommodate the full text. Center the `<text>` (anchor middle, dominant-baseline middle) so it sits inside the rect. Use `rx`/`ry` ≥ 8 for the pill shape. Style the turn-range inline with `<tspan class="turn-range">` so it stays bold/foreground while the rest of the label is muted.

## How to render

Synthesize a fresh single-file HTML each run, using `reference/example.html` as **inspiration** (override anything that doesn't fit the actual session). The reference establishes:

- Pure SVG + vanilla JS (no external libs). Sessions are <200 turns; force-directed layouts are overkill.
- CSS tokens (`--bg`, `--panel`, `--fg`, `--muted`, `--accent`, `--err`, `--warn`, `--ok`, …) — keep this scheme.
- Type pairing: Newsreader italic for the wordmark, JetBrains Mono for everything technical, system sans for prose.
- Header with goal banner, session metadata, theme toggle, filter chips (one per classification).
- SVG canvas (vertical spine) with pan + zoom (`viewBox`-based: wheel zoom on cursor; drag to pan; `0` resets; `+`/`-` zoom).
- Click node → right-side drawer with full text/excerpt, tool calls, args, results.
- Hover node → tooltip with turn id + 1-line summary; highlight all incident edges.
- Filter chips dim non-matching nodes/edges to ~15% opacity.
- Click a back-edge or a `refs` chip in the drawer → center+pulse the referenced ancestor.
- Auto-collapse runs of consecutive `normal` turns into a single capsule labeled `T12–T18 · 7 turns` (click to expand inline).

Output directory — do **not** write inside the skill folder. Resolve a temp dir from the environment, in this preference order:

1. `$TMPDIR` (Unix/macOS)
2. `$TMP` or `$TEMP` (Windows / Git Bash)
3. `/tmp` as fallback

Then create a `reflect-tree/` subdir inside it (`mkdir -p`) and write the report as `<that-dir>/reflect-tree/<slug>.html`. Slug rules — kebab-case, derived from session goal:

- 2–5 words, lowercase, hyphen-separated, ASCII only
- describe the *task*, not the session id (e.g. `auth-middleware-rewrite`)
- if the goal is unclear, fall back to `<YYYY-MM-DD>-<topic>.html`

Open it in the browser when done: `start "" <path>` (Git Bash on Windows).

## Files in this skill

- `reference/example.html` — canonical inspiration HTML showing the tree layout, all node classifications, all edge types, theme toggle, filters, drawer, pan/zoom. Read before generating.
- `scripts/analyze_session.py` — JSONL compressor (independent copy of reflect's; no symlink). Strips system reminders, preserves real user messages, collapses tool calls/results to one-liners, expands compaction blocks. Output is markdown to stdout. Use only for explicit sessions — never on the current in-context session.

## Workflow

**Default (no args)** — reflect on current session:
1. From conversation memory, walk the turns in order. For each, decide the classification (default `normal`); for non-normal turns, fill in `refs` (which earlier turn(s) this re-attempts/undoes/contradicts).
2. Group consecutive `normal` turns into capsules where they would clutter the spine.
3. Read `reference/example.html` for the current aesthetic / SVG layout patterns.
4. Write the tree to the temp dir (`<temp>/reflect-tree/<slug>.html`) — fresh HTML, same look-and-feel as the reference, populated with real turns/edges.
5. Open it with `start "" <path>`.

**Explicit session** — `/reflect-tree <id-or-path>`:
1. Resolve to a JSONL path (if just an id, look under `~/.claude/projects/<encoded-cwd>/<id>.jsonl`).
2. Run `scripts/analyze_session.py <path>`. Skill is forked (`context: fork`), so the compressed transcript is safe in context. No subagent.
3. Walk the transcript and classify each turn yourself — the script does not classify. Focus on user/assistant exchange (what the user wanted vs. what the agent did), not raw tool patterns.
4. **Fallback to JSONL when transcript is lossy.** Transcript truncates tool args/results and long messages. When detail matters (exact rejected input, full error body, Edit diff), `Read` the JSONL directly with `offset`/`limit` scoped to the event. JSONL is source of truth; transcript is the index.
5. Render and open (default steps 2–5).

## Notes

- The tree is a claim about what *happened*. Be honest — include the agent's own mistakes, not just user corrections.
- A linear, all-normal spine is a valid output. Do not invent detours to make the tree look more interesting.
- Sibling: `/reflect` complements this view by producing actionable recommendations. The two can be run on the same session.
