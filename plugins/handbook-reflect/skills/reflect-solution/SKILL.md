---
name: reflect-solution
description: Summarize WHAT WAS SHIPPED in a Claude Code session as a self-contained HTML slide deck — the elevator pitch (problem, solution, decisions, artifacts, verification, gaps), not a play-by-play of tool calls or debugging detours. Defaults to the current in-context session; optionally accepts a session ID or JSONL path. Renders directly in the reflect aesthetic — no delegation. Use when the user invokes /reflect-solution or asks for a recap deck of what changed.
context: fork
argument-hint: `<current_session> or <session-id-or-path>`
---

# /reflect-solution — solution recap deck

Produce a single-file HTML slide deck summarizing the **outcome** of a Claude Code session: what shipped, why, and how it was verified. Audience: someone who wants the elevator pitch, not the journey.

Sibling to `/reflect`. Where `/reflect` looks at *wrong turns*, this skill looks at *what was delivered*. Tool-call churn, retries, dead-ends, and reversals are excluded unless they shaped a final decision.

**Self-contained.** This skill ships its own working starter (`assets/template.html`) — fonts, CSS tokens, all six content blocks, IntersectionObserver, keyboard nav, theme toggle. The agent's job is to *fill the template with extracted content*, not to rebuild the scaffolding from scratch.

## When to use

- User invokes `/reflect-solution` (no args) → recap the **current session** from the in-context conversation. Do **not** re-read the session JSONL — work from the agent's own memory of what was built.
- User invokes `/reflect-solution <session-id>` or `/reflect-solution <path-to-jsonl>` → recap a different session. Run `scripts/analyze_session.py <path>` directly (this skill runs forked — `context: fork` — so the compressed transcript can enter your context safely). The script outputs a compact markdown transcript; **you** then extract the solution.

Session JSONLs live under: `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`

## What to extract (menu, not template)

Outcome-focused. Drop the journey. An item belongs in the deck only if it would matter in a PR description.

**The deck structure should fit the session — not the other way around.** Pick from the menu below; skip what's irrelevant; add what isn't listed if the session calls for it. A 3-slide deck is fine. So is 8. Don't pad to hit a count, don't force a section just because it's in the list.

Common sections (use what fits):

- **Title** — one-line elevator pitch of the shipped solution. Always include.
- **Problem / Goal** — what the user brought. Skip if obvious from title.
- **Solution shipped** — components, modules, behaviors. The *what*, not the steps.
- **Artifacts** — concrete files created/modified. Skip if there's only one file or the file list is trivial.
- **Key decisions & tradeoffs** — locked-in choices + rejected alternatives. Skip if the session was straightforward (no real branch points).
- **Verification / evidence** — tests, builds, manual checks. If absent, say so — never invent.
- **Followups / known gaps** — TODOs, deferred work. Skip if there are none.

Other sections that may earn a slide if the session reveals them: stakeholders, deadlines, related tickets/PRs, performance numbers, before/after diff, architecture sketch, a punchline pull-quote.

**Always omit**: session metadata footer (id, date, turn count). The deck is about the solution, not the session.

## Voice and language

The audience is technical (engineers, reviewers). Write like a commit message or a postmortem, not a launch announcement.

- **Direct and factual.** State what is, what changed, what was decided. No hedging, no hype.
- **No marketing language.** Banned: "elegant", "powerful", "seamless", "robust", "leverages", "unlocks", "delivers", "best-in-class", "modern", "clean", "beautiful", "stunning", "delightful". Also banned: rhetorical hooks ("Imagine if…", "What if…"), exclamation points, emoji.
- **No slogans or punchlines.** Every line carries information. Skip the pull-quote slide unless the quote is a real artifact (a user message, a commit subject, a doc heading) — not something invented for flair.
- **No empty connectives.** Drop "In order to", "It is important to note that", "We are excited to". Get to the noun.
- **Concrete over abstract.** "Replaced regex parser with PEG grammar in `parser/expr.ts` — handles nested parens" beats "Improved parsing capabilities".
- **Numbers when you have them.** "12 tests, 94% coverage", "reduced p99 from 240ms to 90ms", "3 files modified, 1 added". Don't invent numbers.
- **Code identifiers in mono.** Function names, file paths, flags, env vars → `<code>`. Prose stays prose.

## Problem statement

This is the most important slide. A reader who only sees this slide should understand what was wrong before the session started. Treat it like the "Background" section of a bug ticket.

- **One paragraph, 2–4 sentences.** Or 3–5 short bullets. Not both.
- **Factual.** State the prior state of the system, the observed defect or gap, and the constraint that forced the work. No motivation language ("we wanted to…"), no story arc.
- **Concrete.** Name the file, the function, the error message, the failing case. If there was a ticket or incident, reference it.
- **No solution preview.** The problem slide describes the problem only. What was done belongs on the next slide.
- **Easy to digest.** Short sentences. One idea per sentence. If you need a comma-spliced run-on to fit, split it.

Good: *The deck template hard-coded a 7-section taxonomy. Sessions with no decisions or no followups produced empty slides. Agents had no guidance on when to drop a section.*

Bad: *We wanted to make the deck more flexible and adaptable so that it could elegantly handle a wider variety of sessions and deliver a more polished experience.*

## Honesty rules

- Be specific. "Added auth handling" is useless; "Added `validateBearerToken()` in `src/auth/middleware.ts`, called from `app.use()`" is a recap.
- Don't invent verification. If no tests were run, the Verification slide says "No automated verification this session — manual smoke check only" or similar.
- Don't pad. A 4-slide deck is fine if the session was small.
- Don't editorialize. Skip adjectives that don't carry information ("nicely", "cleanly", "properly"). If the change was correct, the diff shows it.

## Output

Resolve a temp dir from the environment, in this preference order:

1. `$TMPDIR` (Unix/macOS)
2. `$TMP` or `$TEMP` (Windows / Git Bash)
3. `/tmp` as fallback

Create `<temp>/reflect-solution/` (`mkdir -p`). Write the deck as `<temp>/reflect-solution/<slug>.html`.

**Slug rules** — kebab-case, derived from the *solution* (not the session id):
- 2–5 words, lowercase, hyphen-separated, ASCII only
- describe what was shipped (e.g. `auth-middleware-rewrite`, `reflect-solution-skill-design`)
- if the solution is unclear, fall back to `<YYYY-MM-DD>-<topic>`

Open with `start "" <path>` (Git Bash on Windows).

---

# How to render — fill the template, don't rebuild

The starter at `assets/template.html` is a working deck: light theme by default (with a dark toggle persisted in localStorage), full slide shell, all six content blocks pre-styled, keyboard nav (↑/↓/Space/PageUp/PageDown/Home/End/j/k), touch swipe, IntersectionObserver reveals, nav rail, and `prefers-reduced-motion` respect.

## Workflow

1. **Read** `assets/template.html` and `assets/viewport-base.css`.
2. **Copy** the template to your temp output path as the deck's starting point.
3. **Inline** the full contents of `assets/viewport-base.css` into the `<style>` block where the abridged base styles live (the comment marks the spot). Don't link to it — the deck must be a single self-contained HTML file.
4. **Replace** the `{{...}}` placeholders with extracted content.
5. **Duplicate / remove** body-slide `<section>` elements as needed for your taxonomy. Keep one slide per taxonomy section by default; split if a section overflows density limits (see below). Update the nav rail `<a>` list to match.
6. **Pick the right content block** per slide (see catalog) — don't default to bullets.
7. **Validate** density and font/style rules before saving.

## Light theme is the default

`<html data-theme="light">`. Do NOT change this. The dark theme exists as a user-toggleable option (button bottom-right, key persists in localStorage). Both themes are wired; just leave them alone.

## Content block catalog (copy from template, fill in)

| Block | Class | When |
|---|---|---|
| **Bullets** | `<ul class="bullets">` | 4–6 substantial parallel items. Each `<li>` leads with `<b>…</b> —` then a sentence. Mono em-dash marker auto-rendered. |
| **Artifact grid** | `<div class="artifacts">` w/ `.artifact` cards | Files created/modified. 2-col grid. Each card: `.tag.added/.modified/.removed`, `.path` (mono), `.purpose` (sans). Banned: bulleted list of file paths. |
| **Decision rows** | `<div class="decisions">` w/ `.decision` rows | Locked-in choices + rejected alternatives. Two columns ("Chose" / "Rejected") with reason underneath. |
| **Code/output** | `<pre class="codeblock">` | Real command + output (8–10 lines max). `.ln` spans for line numbers. |
| **Pull-quote** | `<div class="pullquote">` | One italic Newsreader sentence + mono attribution. For Title subtitle or a punchline slide. |
| **Two-column prose** | `<div class="cols2">` | Dense paragraphs. Use for Problem when there's a story to tell. |

## Slide shell (every body slide)

```html
<section class="slide" id="sN">
  <div class="eyebrow reveal"><span class="num">0N</span> SECTION</div>
  <h2 class="title reveal"><em>Italic part</em> <span class="roman">roman tail.</span></h2>
  <div class="hairline reveal"></div>
  <div class="body">
    <!-- one of the content blocks above -->
  </div>
  <div class="hairline reveal"></div>
  <div class="footer reveal">
    <span>EYEBROW · CONTEXT</span>
    <span class="right">project / status</span>
  </div>
</section>
```

The eyebrow + numbered title hairline anchors the top, the bottom hairline + footer rail anchors the bottom. Both are mandatory — they prevent the "floating bullets in a void" failure mode.

## Title slide

Distinct layout (no eyebrow, no body):

```html
<section class="slide title-slide" id="s0">
  <div class="pitch reveal"><em>Italic pitch</em> <span class="roman">roman tail.</span></div>
  <div class="meta reveal">SOLUTION RECAP <span class="sep">·</span> PROJECT-OR-CONTEXT</div>
</section>
```

## Density (avoid empty slides)

The biggest failure mode is sparse slides — 3 short bullets in the upper third, the rest of the viewport empty. Counter it:

- **Use the full viewport.** Body content fills the middle 60–70vh between the title hairline and the footer rail. If you have less, switch to a richer content block (artifact grid, decision rows, code block) before adding padding.
- **Substantial bullets only.** 4–6 bullets, each a full sentence with a bolded lead. If you only have 2 short bullets, merge with adjacent content or switch block types.
- **Footer rail is mandatory.** Eyebrow + context on the left, project/status in italic on the right.
- **Banned**: floating bullets in the top third with >40% empty viewport below.

## Typography rules

The template hard-codes these — don't override:

- **Hero / slide titles** → Newsreader italic, weight 500. Mix italic + roman in one title (`<em>…</em> <span class="roman">…</span>`).
- **Body prose & bullets** → system sans, `clamp(0.95rem, 1.25vw, 1.1rem)`.
- **Eyebrows / footer rail / mono labels** → JetBrains Mono uppercase, `letter-spacing: 0.14–0.18em`.
- **Inline code** → `<code>literal</code>` — the template enforces `display: inline` so it does NOT break across lines. Never wrap a code span in a flex-column container.
- **Forbidden fonts**: Bodoni Moda, DM Sans, Plus Jakarta Sans, Space Grotesk, Archivo Black, Outfit, Fraunces, Cormorant, Inter, Roboto, Arial.

## Animation guidance

See `assets/animation-patterns.md` for the slim crib sheet (entrance variants, what NOT to do, common breakage). The default `.reveal` class with stagger is already wired in `template.html`.

## CSS gotcha

Do not negate CSS functions directly. `right: -clamp(...)` is silently ignored. Use `right: calc(-1 * clamp(...))`.

---

# Files in this skill

- `SKILL.md` — this file: taxonomy, render workflow.
- `assets/template.html` — **working starter deck**. Light by default, dark toggle, all six content blocks pre-styled, keyboard nav + IntersectionObserver wired. Copy-and-fill, don't rebuild.
- `assets/viewport-base.css` — copied verbatim from `frontend-slides`. Inline its full contents in the `<style>` block of the generated deck.
- `assets/animation-patterns.md` — slim animation reference (variants, don'ts, troubleshooting).
- `scripts/analyze_session.py` — JSONL compressor (duplicated from the `reflect` skill, independent). Strips system reminders, preserves real user messages, collapses tool calls/results to one-liners. Output is markdown to stdout. Use only for explicit sessions — never on the current in-context session.
- `reference/example-deck.md` — fully worked example showing how a real session maps to the seven sections (treat as inspiration for tone and density, not a template).

# Workflow

**Default (no args)** — recap current session:
1. From conversation memory, walk the taxonomy: title, problem, solution, artifacts, decisions, verification, followups. Drop everything that's journey-not-outcome.
2. For each section, pick a content block. If a section has thin content, switch block types or merge.
3. Resolve temp dir, derive slug.
4. Read `assets/template.html` and `assets/viewport-base.css`.
5. Copy the template to `<temp>/reflect-solution/<slug>.html`. Inline `viewport-base.css` into the `<style>` block. Replace placeholders. Add/remove body slides. Update nav rail.
6. Open with `start "" <path>`.

**Explicit session** — `/reflect-solution <id-or-path>`:
1. Resolve to a JSONL path (if just an id, look under `~/.claude/projects/<encoded-cwd>/<id>.jsonl`).
2. Run `scripts/analyze_session.py <path>`. Skill is forked, so the compressed transcript is safe in context.
3. Extract the taxonomy from the transcript yourself.
4. **Fallback to JSONL when transcript is lossy.** Transcript truncates tool args/results and long messages. When detail matters (full file lists, full diff, full user goal statement), `Read` the JSONL directly with `offset`/`limit` scoped to the relevant turn.
5. Steps 2–6 from the default workflow.

# Notes

- The deck is the elevator pitch, not the changelog. If you find yourself listing every Edit, you're recapping the journey, not the solution — collapse to artifacts.
- If verification was absent, say so. A missing-evidence slide is more useful than a fabricated one.
- Decisions slide should include *what was rejected and why*, not just what was chosen.
- The skill is free to evolve its style independently of `frontend-slides`. Re-copy `viewport-base.css` if you want to pick up upstream improvements.
