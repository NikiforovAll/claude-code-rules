# Handbook Visual Explainer

Generate beautiful, self-contained HTML pages that visually explain systems, code changes, plans, and data.

Every page is a single file with no build step and no external assets beyond web fonts and CDN libraries: a theme toggle, a considered palette and font pairing, and Mermaid diagrams with zoom and pan where the topology matters.

## Skills

- **visual-explainer** - Generate HTML diagrams, tables, slide decks, and architecture overviews. Fires on its own when tabular data would otherwise land in the terminal as an ASCII table.

## Commands

All seven are user-invoked only — type them, they never fire on their own.

| Command | What it does |
|---------|-------------|
| `/handbook-visual-explainer:web-diagram` | Standalone HTML diagram for any topic |
| `/handbook-visual-explainer:visual-plan` | Implementation plan for a feature — state machines, code snippets, edge cases |
| `/handbook-visual-explainer:slides` | Magazine-quality slide deck as a self-contained page |
| `/handbook-visual-explainer:diff-review` | Before/after architecture comparison with code review analysis |
| `/handbook-visual-explainer:plan-review` | Current codebase state vs. a proposed implementation plan |
| `/handbook-visual-explainer:project-recap` | Current state, recent decisions, and cognitive debt hotspots |
| `/handbook-visual-explainer:fact-check` | Verify a document against the codebase and correct it in place |

## Choosing a look

`--picker` opens a catalog of every style at real hex values, so you can see the palette and font pairing before committing:

```
/handbook-visual-explainer:visual-explainer --picker
```

Or pass the choice directly — `--style nord`, `--theme light`, `--palette terracotta+sage`, `--font instrument-serif+jetbrains-mono`. The skill's own documentation lists every flag.

## Installation

```bash
/plugin marketplace add nikiforovall/claude-code-rules
/plugin install handbook-visual-explainer
```

## Documentation

See the [Component Reference](https://nikiforovall.blog/claude-code-rules/component-reference) for detailed usage of each command.

## Attribution

Based on [visual-explainer](https://github.com/nicobailon/visual-explainer) by nicobailon, MIT licensed.
