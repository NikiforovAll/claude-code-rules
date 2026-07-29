---
name: dotnet-analyzers
description:   Run dotnet format to fix code style and analyzer diagnostics (IDE0005, CA*, SA*). Use when fixing unnecessary usings, code style violations, analyzer warnings, or verifying format compliance
argument-hint: "[diagnostic ID or 'verify' or 'list' or '--dashboard' or '--sarif']"
allowed-tools: Bash(dotnet format *), Bash(dotnet clean *), Bash(jq *), Bash(bash *generate-report*), Read, Grep, Glob
---

# .NET Analyzers & Code Format

Fix code style and analyzer diagnostics using `dotnet format`.

Arguments: $ARGUMENTS

## Key Concepts

- `dotnet format` does its own internal compilation — it does NOT depend on cached build output
- CA*/SA* rules (analyzers) run during build if `EnableNETAnalyzers` is true

## Command Reference

| Task | Command |
|------|---------|
| Fix specific style diagnostic | `dotnet format style --diagnostics IDE0005 --severity warn` |
| Fix specific analyzer diagnostic | `dotnet format analyzers --diagnostics CA1305 --severity warn` |
| Fix all style issues | `dotnet format style --severity warn` |
| Fix all analyzer issues | `dotnet format analyzers --severity warn` |
| Fix everything | `dotnet format --severity warn` |
| Verify only (CI) | `dotnet format --verify-no-changes --severity warn` |
| List violations without fixing | `dotnet format style --verify-no-changes --severity warn -v diag` |
| Scope to folder | `dotnet format style --diagnostics IDE0005 --include src/MyProject/` |

## Common Diagnostics

### Style (IDE*) — use `dotnet format style`

| ID | Description |
|----|-------------|
| IDE0005 | Unnecessary using directive |
| IDE0055 | Fix formatting |
| IDE0090 | Simplify `new` expression |
| IDE0161 | File-scoped namespace |
| IDE0251 | Make member readonly |

### Analyzers (CA*) — use `dotnet format analyzers`

| ID | Description |
|----|-------------|
| CA1305 | Specify IFormatProvider |
| CA1822 | Mark members as static |
| CA1859 | Use concrete types for performance |
| CA2000 | Dispose objects before losing scope |

## Workflow

IMPORTANT: Always start in verify/list mode. NEVER auto-fix without explicit user confirmation.

### Step 1: List violations (default)

Always start by showing what would change — never fix automatically.
Use `--report "$TEMP/dotnet-format"` to get structured JSON, then process with `jq`.

```bash
# List all style violations as JSON report
dotnet format style --verify-no-changes --severity warn --report "$TEMP/dotnet-format" <PROJECT_OR_SOLUTION> 2>/dev/null

# List specific diagnostic
dotnet format style --verify-no-changes --diagnostics IDE0005 --severity warn --report "$TEMP/dotnet-format" <PROJECT_OR_SOLUTION> 2>/dev/null

# List analyzer violations
dotnet format analyzers --verify-no-changes --severity warn --report "$TEMP/dotnet-format" <PROJECT_OR_SOLUTION> 2>/dev/null
```

Process the JSON report with `jq`:

```bash
# Summary: count violations per diagnostic ID
jq '[.[].FileChanges[].DiagnosticId] | group_by(.) | map({id: .[0], count: length}) | sort_by(-.count)' "$TEMP/dotnet-format/format-report.json"

# List affected files
jq '[.[].FilePath] | unique | .[]' "$TEMP/dotnet-format/format-report.json"

# Show details for a specific diagnostic
jq '[.[] | {file: .FilePath, changes: [.FileChanges[] | select(.DiagnosticId == "IDE0005")]} | select(.changes | length > 0)]' "$TEMP/dotnet-format/format-report.json"
```

### Step 2: Report findings to user

Summarize the violations found using the JSON report and ask the user if they want to apply fixes.

### Step 3: Apply fixes (only after user confirms)

```bash
dotnet format style --diagnostics IDE0005 --severity warn
```

Or for analyzer rules:

```bash
dotnet format analyzers --diagnostics CA1305 --severity warn
```

### Step 4: Verify build still passes

```bash
dotnet build -p:WarningLevel=0 /clp:ErrorsOnly
```

## HTML Dashboard Report (`--dashboard`)

Only generate when user explicitly passes `--dashboard`. Do NOT suggest or run this unprompted.

`--sarif` selects SARIF mode: the script runs its own `dotnet build -t:Rebuild` and harvests `_analyzer-diag.sarif` files. It is NOT a request to run `dotnet build` separately — passing the flag through to `generate-report.sh` is the entire job. Without `--sarif`, the script uses the faster `dotnet format` path. SARIF mode respects editorconfig severity (filters `level=note`/`none` and source-suppressed entries). See [Mode comparison](#mode-comparison) for when to pick which.

Generate an interactive HTML dashboard from live `dotnet format` output. No AI involved — purely deterministic.

### Usage

Default mode uses `dotnet format` (fast, fixable diagnostics only):

```bash
# From repo root (defaults to current dir, outputs analyzer-dashboard.html)
bash ~/.claude/skills/dotnet-analyzers/scripts/generate-report.sh

# Explicit solution/project path and output
bash ~/.claude/skills/dotnet-analyzers/scripts/generate-report.sh ./MyProject.sln analyzer-dashboard-generated.html
```

SARIF mode runs `dotnet build -t:Rebuild` and harvests Roslyn ErrorLog SARIF (slower, comprehensive):

```bash
# Run ONLY when user explicitly asks for full coverage / "report everything"
bash ~/.claude/skills/dotnet-analyzers/scripts/generate-report.sh --sarif presales.slnx analyzer-dashboard-sarif.html
```

Flag parsing: `--sarif` and `--dashboard` may appear in any order; `--dashboard` is a no-op (dashboard is always emitted) but accepted so user invocations like `--dashboard --sarif` work as expected. Positional args are `[project] [output.html]`.

When the user asks for **both** dashboards, generate them with distinct output names:

```bash
bash ~/.claude/skills/dotnet-analyzers/scripts/generate-report.sh presales.slnx analyzer-dashboard.html
bash ~/.claude/skills/dotnet-analyzers/scripts/generate-report.sh --sarif presales.slnx analyzer-dashboard-sarif.html
```

### Mode comparison

| Aspect | default (`dotnet format`) | `--sarif` (Roslyn ErrorLog) |
|--------|----------------------------|------------------------------|
| Speed | Fast (~10s) | Slow (full rebuild, ~1–2 min) |
| Coverage | Fixable analyzers only (CA*, S*, IDE*, IDISP*) | All Roslyn diagnostics: CS* + CA* + S* + IDE* + IDISP* + ASP* + MUD* + xUnit* etc. |
| CS* compiler warnings (CS8602, CS0618, …) | ❌ skipped | ✅ included |
| Editorconfig severity respected | ✅ | ✅ (filters SARIF `level=note`/`none` and `suppressions[]`) |
| NU* (NuGet vulnerabilities) | ❌ | ❌ (restore phase, not in SARIF) |
| MSB* (MSBuild engine) | ❌ | ❌ (build engine, not in SARIF) |
| Side effects | None | Forces full rebuild; writes per-project `_analyzer-diag.sarif` |

### When to use which

- **Default (no flag)** — quick triage of fixable issues; iterating on `dotnet format` fixes.
- **`--sarif`** — only when user explicitly asks for "everything", "full picture", "real warning count", or notices the default dashboard is undercounting compared to `dotnet build`. Never run unprompted: it triggers a full rebuild.

### What it does

Default mode:
1. Runs `dotnet format style --verify-no-changes --severity warn --report <tmpdir>`
2. Runs `dotnet format analyzers --verify-no-changes --severity warn --report <tmpdir>`
3. Transforms `format-report.json` via `jq` into violation summaries and file-level details
4. Injects data into `scripts/template.html`, writes output HTML

`--sarif` mode:
1. Cleans prior `_analyzer-diag.sarif` files
2. Runs `dotnet build <project> -t:Rebuild -p:ErrorLog=_analyzer-diag.sarif%2cversion=2.1`
3. Globs all per-project SARIF, drops source-suppressed and `level∉{warning,error}` results, dedupes by `(ruleId, uri, line, col)` (collapses multi-target duplicates)
4. Routes IDE* into the style bucket, everything else into analyzer bucket, injects into `template.html`

