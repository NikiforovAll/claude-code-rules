# Example deck — reflect-solution skill design

Fully worked example showing how a real session (this one) maps to the seven sections. Use as inspiration for tone and density, not as a template.

---

## Slide 1 — Title (title-slide layout, no eyebrow)

> *A `/reflect-solution` skill* `for outcome-focused recaps.`
> ────────────────────────
> SOLUTION RECAP · ~/.claude/skills

## Slide 2 — Problem (two-column prose block)

EYEBROW: `01 · PROBLEM`

Title: *Two reflect skills,* `one missing lens.`

Body (two short paragraphs):
- `/reflect` answers "where did the agent go wrong" — useful for tuning, not for a recap. There's no tool to answer "what did this session actually deliver" without re-reading the transcript.
- We need an elevator pitch that a stakeholder can read in 60 seconds: problem, solution, artifacts, decisions, verification, gaps.

Footer: `SCOPE · skills` ··· *reflect family / planning*

## Slide 3 — Solution (bullets block, 4 substantial)

EYEBROW: `02 · SOLUTION`

Title: *A self-contained skill* `at ~/.claude/skills/reflect-solution/`.

Bullets (each leads with a bolded phrase):
- **Mirrors `/reflect` shape.** Forked context, current-session default, optional `<id-or-path>` argument.
- **Outcome-focused taxonomy.** Title, problem, solution, artifacts, decisions, verification, followups — journey detail dropped.
- **Owns its own style.** No delegation to `frontend-slides`; one fixed reflect aesthetic (Newsreader + JetBrains Mono on dark, rust accent).
- **Self-contained rendering.** `viewport-base.css` copied as the only shared asset; skill free to diverge.

Footer: `SHIPPED · 7 sections` ··· *reflect-solution / v1*

## Slide 4 — Artifacts (artifact grid block, 2x2)

EYEBROW: `03 · ARTIFACTS`

Title: *Three files, one* `viewport-base.css.`

Cards (2x2 grid, file path mono + 1-line purpose):

| `SKILL.md` | `scripts/analyze_session.py` |
| Workflow, taxonomy, full style spec | JSONL compressor, duplicated from /reflect |
| **ADDED** | **ADDED** |

| `assets/viewport-base.css` | `reference/example-deck.md` |
| Copied verbatim from frontend-slides | Worked example (this file) |
| **ADDED** | **ADDED** |

Footer: `4 FILES · ~/.claude/skills/reflect-solution` ··· *all-new*

## Slide 5 — Decisions (decision rows block)

EYEBROW: `04 · DECISIONS`

Title: *What we chose,* `what we left behind.`

Rows:

> **CHOSE** Self-contained skill that owns its style
> **REJECTED** Delegating to `frontend-slides` with overrides
> *Reason: too many escape hatches; user disliked preset fonts and pastel layouts*

> **CHOSE** Single fixed style (reflect aesthetic)
> **REJECTED** Per-session preset selection
> *Reason: continuity across the /reflect family beats variety*

> **CHOSE** Duplicate `analyze_session.py` from /reflect
> **REJECTED** Symlink
> *Reason: skills should evolve independently; drift is acceptable*

Footer: `3 DECISIONS · locked` ··· *reflect-solution / design*

## Slide 6 — Verification (code/output block)

EYEBROW: `05 · VERIFICATION`

Title: *Skill is registered* `but not yet runtime-tested.`

Code block (mono, --snippet bg):
```
$ ls ~/.claude/skills/reflect-solution/
SKILL.md
assets/
  viewport-base.css
reference/
  example-deck.md
scripts/
  analyze_session.py
```

Bullet line under: **Pending** — first real `/reflect-solution` invocation will exercise the rendering path end-to-end.

Footer: `MANUAL CHECK ONLY · no automated verification` ··· *reflect-solution / pending*

## Slide 7 — Followups (bullets block, terse)

EYEBROW: `06 · FOLLOWUPS`

Title: *Known gaps* `worth tracking.`

Bullets:
- **`--style=<preset>` arg parsing.** Add only when a second style is genuinely requested in practice — not before.
- **Density-split logic.** Validate against a long session (20+ artifacts, 10+ decisions). Current rules are theoretical.
- **Shared payload schema.** If a third `reflect-*` skill emerges, factor a common extraction interface; until then, each skill owns its own.

Footer: `3 OPEN · deferred` ··· *reflect-solution / v1.x*
