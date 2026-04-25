---
name: reflect
description: Analyze a Claude Code session for "wrong-turn" moments (corrections, retries, waste, reversals, dead-ends) and produce an interactive HTML dashboard with copy-able recommendations (CLAUDE.md rules, docs, scripts, hooks, memory entries, sub-skills, etc.) that would help future agents reach the goal faster. Defaults to reflecting on the current in-context session; optionally accepts a session ID or JSONL path. Use when the user invokes /reflect or asks to learn from this session.
context: fork
argument-hint: `<current_session> or <session-id-or-path>`
---

# /reflect — session reflection

Produce a single-file interactive HTML dashboard analyzing a Claude Code session for places the agent took a wrong turn, paired with concrete repo additions that would prevent the same wrong turn next time.

## When to use

- User invokes `/reflect` (no args) → analyze the **current session** from the in-context conversation. Do **not** re-read the session JSONL — work from the agent's own memory of what happened.
- User invokes `/reflect <session-id>` or `/reflect <path-to-jsonl>` → analyze a different session. Run `scripts/analyze_session.py <path>` directly (this skill runs in a forked context — `context: fork` — so the compressed transcript can enter your context safely). The script outputs a compact markdown transcript: system reminders stripped, tool calls/results collapsed to one-liners, compaction blocks expanded with embedded user quotes. Then **you** analyze that transcript to identify wrong-turn moments — the script does NOT classify incidents, it only compresses.

Session JSONLs live under: `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`

## What to detect (incidents)

Open-ended — but the common shapes are:

- **correction** — user pushed back on an approach (`"no"`, `"don't"`, `"stop"`, `"actually"`)
- **retry** — agent ran the same tool 2+ times with variations before it worked
- **waste** — many Reads/Greps/Globs before finding the right file
- **reversal** — agent edited then unwound (Edit → revert, Write → delete)
- **dead-end** — tool failed because of the environment (missing binary, wrong path, OS mismatch)
- **self-correction** — agent caught its own mistake mid-stream

Severity:
- **high** — explicit user correction, repeated correction, or substantial wasted turns
- **med** — single retry/reversal, modest waste
- **low** — minor dead-end, easily recovered

Confidence (0–100): how sure you are this is a real wrong turn worth surfacing, vs. signal noise. Be honest — low-confidence items are not bugs, they let the user filter out speculation.
- **90–100** — explicit user correction or unambiguous failure
- **70–89** — strong pattern (repeated retries, clear reversal) with minor interpretation
- **50–69** — plausible wrong turn, could also be normal exploration
- **<50** — speculative; surface only if the pattern is interesting

Render as `data-conf="<n>"` on each `.incident` plus a small badge. The dashboard slider hides incidents below the chosen threshold.

## What to recommend

Open-ended. Anything that would help a future agent reach the goal faster. Examples (not a fixed taxonomy — pick what fits the incident):

- **rule** → `CLAUDE.md` block (project or user)
- **doc** → `docs/ARCHITECTURE.md`, README pointer, architecture map
- **script** → `scripts/<name>.sh` wrapping a known-good command
- **hook** → `.claude/settings.json` `PreToolUse` / `PostToolUse` for hard blocks (e.g. block edits to a generated file)
- **memory** → user/feedback/project/reference entry under `~/.claude/.../memory/`
- **skill** → a new sub-skill in `~/.claude/skills/`
- **agent** → an agent definition in `.claude/agents/`
- **allowlist** → `permissions` in `.claude/settings.json`
- **env** → environment variable, MCP server, etc.

Each recommendation should map to one or more incidents (the dashboard renders these as `addresses #N` links).

## How to render

Synthesize a fresh single-file HTML dashboard each run, using `reference/example.html` as **inspiration** (not a template — override anything that doesn't fit the session). The reference file establishes:

- Two-pane layout: incidents left, recommendations right
- CSS tokens (`--bg`, `--panel`, `--fg`, `--muted`, `--accent`, etc.) — keep this scheme
- Type pairing: Newsreader italic for the wordmark, JetBrains Mono for everything technical, system sans for prose
- Click incident card to expand; click `addresses #N` link to scroll-and-highlight the matching incident
- Filter chips toggle severity and category

Output directory — do **not** write inside the skill folder. Resolve a temp dir from the environment, in this preference order:

1. `$TMPDIR` (Unix/macOS)
2. `$TMP` or `$TEMP` (Windows / Git Bash)
3. `/tmp` as fallback

Then create a `reflect/` subdir inside it (`mkdir -p`) and write the report as `<that-dir>/reflect/<slug>.html`. Slug rules — kebab-case, derived from session goal:
- 2–5 words, lowercase, hyphen-separated, ASCII only
- describe the *task*, not the session id (e.g. `auth-middleware-rewrite`)
- if the goal is unclear, fall back to `<YYYY-MM-DD>-<topic>.html`

Open it in the browser when done: `start "" <path>` (Git Bash on Windows).

## Files in this skill

- `reference/example.html` — canonical inspiration HTML. Read before generating.
- `scripts/analyze_session.py` — JSONL compressor. Strips system reminders, preserves real user messages, collapses tool calls/results to one-liners, expands compaction blocks. Output is markdown to stdout. Use only for explicit sessions — never on the current in-context session.

## Workflow

**Default (no args)** — reflect on current session:
1. From conversation memory, list wrong-turn moments (incidents) with severity + category + turn marker + a 1-line excerpt.
2. For each incident (or cluster), draft a recommendation: title, target (kind + path), snippet, list of incident IDs it addresses.
3. Read `reference/example.html` for the current aesthetic.
4. Write the dashboard to the temp dir resolved above (`<temp>/reflect/<slug>.html`) — fresh HTML, same look-and-feel as the reference, populated with the real incidents/recs.
5. Open it with `start "" <path>`.

**Explicit session** — `/reflect <id-or-path>`:
1. Resolve to a JSONL path (if just an id, look under `~/.claude/projects/<encoded-cwd>/<id>.jsonl`).
2. Run `scripts/analyze_session.py <path>`. Skill is forked (`context: fork`), so the compressed transcript (tens of KB even for multi-MB JSONLs) is safe in context. No subagent.
3. Identify wrong-turn incidents from the transcript yourself — the script does not classify. Focus on user/assistant exchange (what the user wanted vs. what the agent did), not raw tool patterns.
4. **Fallback to JSONL when transcript is lossy.** Transcript truncates tool args/results and long messages. When detail matters (exact rejected input, full error body, Edit diff, full user message), `Read` the JSONL directly with `offset`/`limit` scoped to the event by turn/tool. JSONL is source of truth; transcript is the index.
5. Draft recommendations and render (default steps 2–5).

## Notes

- Incidents are claims about what *happened*. Be honest — include the agent's own mistakes, not just user corrections.
- Recommendations should be specific and actionable (real paths, real snippet content). A vague "improve docs" rec is not useful.
