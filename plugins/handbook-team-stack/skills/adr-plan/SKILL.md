---
name: adr-plan
description: Analyze a task and produce an Architecture Decision Record with implementation steps.
allowed-tools: Agent, AskUserQuestion, Bash(npx adr *), Bash(git diff *), Bash(git log *), Bash(git status *), Bash(ls *), Bash(cat *), Read, Grep, Glob
---

# ADR Plan: Task Analysis → Architecture Decision Record

Analyze a task, explore the codebase, and produce an ADR with concrete implementation steps.

## Phase 1: Analyze

1. Read the task description, active plan, or task list
2. Explore affected areas of the codebase — do it concurrently for independent modules
3. Map blast radius — search for consumers of functions/types/routes being changed
4. Identify alternatives worth considering (at least 2)

Do this silently.

## Phase 2: Detect ADR Setup

Check if the project has an ADR directory:

```
ls docs/adr/ || ls adr/ || ls doc/adr/
```

- **Found** → use existing directory, detect next number from existing files
- **Not found** → run `npx adr init en`, then proceed

## Phase 3: Produce ADR Content

Write the ADR using `npx adr new "<title>"`, then edit the generated file with the following structure:

```markdown
# ADR-NNNN: [Title]

## Status
Proposed

## Context
[What problem are we solving? What constraints exist?]

## Decision
[What we chose and why]

## Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| ... | ... | ... |

## Implementation Steps

### Step 1: [Description]
- **Files:** [files to create/modify]
- **Depends on:** [previous step or "none"]
- **Done when:** [concrete acceptance criteria]

### Step 2: [Description]
...

## Consequences
- [Positive and negative outcomes, tradeoffs accepted]
```

### Guidelines

- **Steps are ordered by dependency** — each step lists what it depends on
- **Steps are parallelizable when independent** — note which steps can run concurrently
- **Each step has concrete "done when" criteria** — no vague outcomes
- **Alternatives table is honest** — include the option you chose and why others lost
- Keep it short. 1-2 pages max. No padding.

## Phase 4: Present to User

Show the ADR content and the file path. The user may:
- **Approve** → ADR stays as-is
- **Adjust** → edit and re-present
- **Cancel** → delete the file

## Important

- The ADR is a planning artifact, not documentation for posterity
- Steps should map naturally to work units (a team member could own one or more steps)
- If the task is too simple for an ADR (single file, obvious fix), say so and skip
- Do not write implementation code — this is planning only
