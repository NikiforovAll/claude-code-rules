---
name: team-stack
description: Analyze a task, propose an agent team composition with roles and responsibilities, and create the team after user confirmation. Use when the user says "team stack", "create a team", "set up agents for this", or describes a complex task that would benefit from multiple agents working together.
allowed-tools: Agent, AskUserQuestion, Bash(git diff *), Bash(git log *), Bash(git status *), Read, Grep, Glob, TaskCreate, TaskUpdate, TaskList, TeamCreate, TeamDelete, SendMessage
---

# Team Stack: Analyze, Propose, and Create Agent Teams

You help the user set up the right agent team for their task. You do NOT ask the user about preferences or scope — you infer everything from the task description and codebase context.

## Phase 1: Analyze the Task

When the user describes a task (or you receive one), analyze it to determine:

1. **Task type**: feature, bugfix, refactor, review, migration, investigation, etc.
2. **Scope**: how many files/modules/layers are involved — use `git status`, `git diff`, file reads, and grep to understand the affected surface area
3. **Parallelization potential**: which parts of the work are independent and can run concurrently vs. which have dependencies
4. **Risk level**: does it touch critical paths, shared state, or public APIs
5. **Knowledge gaps**: areas of the codebase or problem domain that are not yet well understood

### Use Existing Context

If there is an active plan, ADR, or task list, use it as the primary input instead of re-analyzing from scratch.

### Explore the Codebase

Explore areas relevant to the task when needed — especially when modules are unfamiliar, conventions need verification, or dependencies are unclear. Explore independent areas concurrently.

Do this analysis silently. Do NOT present it to the user as a separate step.

## Phase 2: Propose Team Stack

Based on your analysis, propose a team. Present it to the user as a clear table:

```
## Proposed Team: <team-name>

| Role | Name | Responsibility | Isolation |
|------|------|---------------|-----------|
| ... | ... | ... | worktree / shared |

**Why this composition:** <1-2 sentences explaining the rationale>

```

### Team Composition Guidelines

Pick the **minimum viable team**. Do not over-staff.

**Solo agent (no team needed):**
- Simple, single-file changes
- Quick fixes with obvious solutions
- Suggest using a subagent instead and exit

**2 agents:**
- Task has two clearly independent workstreams (e.g., frontend + backend, implementation + tests)

**3 agents:**
- Task benefits from a builder/reviewer split (e.g., 2 builders + 1 reviewer)
- Cross-layer work (e.g., API + service + tests)

**4+ agents:**
- Large migrations, multi-module refactors, or parallel investigation of competing hypotheses
- Each additional agent must have a clearly distinct responsibility

### Role Types to Draw From

Choose roles that fit the task. These are examples, not a fixed menu:

- **implementer** — writes the code for a specific module/layer
- **reviewer** — cross-reviews artifacts produced by other agents
- **test-writer** — writes/updates tests for the changes
- **investigator** — researches codebase, finds patterns, reports findings
- **architect** — designs the approach, reviews for consistency across agents' work
- **migrator** — handles mechanical transformations across many files

### Isolation Decision

- Use `worktree` when agents edit overlapping files or the same module
- Use `shared` (no isolation) when agents work on completely separate file sets

## Phase 3: Confirm with User

Present the proposal using `AskUserQuestion`. The user may:
- **Approve** → proceed to Phase 4
- **Adjust** → modify roles, add/remove agents, change responsibilities → re-present
- **Cancel** → stop

## Phase 4: Create the Team

After confirmation:

1. Create the team with `TeamCreate`
2. Create tasks for each agent using `TaskCreate`
3. Spawn each agent using the `Agent` tool with:
   - A prompt structured with **DoR** and **DoD** sections (see below)
   - The `name` parameter matching the role name from the table
   - The `team_name` parameter so they join the same team
   - `isolation: "worktree"` if specified in the proposal
   - `run_in_background: true` for agents that can work in parallel
4. Briefly confirm to the user that the team is running

### Agent Prompt Structure: DoR / DoD

Every agent prompt MUST follow this structure:

```
## Definition of Ready (what you receive)

- <concrete input 1: e.g., "Diff of changed files: ...", "File to review: src/auth/login.ts", "Architecture decision: use repository pattern">
- <concrete input 2>
- ...

## Your Task

<what this agent must do — clear, scoped, actionable>

## Definition of Done (what you must deliver)

- <concrete output 1: e.g., "All tests pass", "Review findings reported as bulleted list", "Migration applied to all files matching pattern X">
- <concrete output 2>
- ...

When done, verify each DoD item before reporting completion.
```

**DoR** — what the agent starts with. Can be concrete artifacts (files, diffs) or a scoped investigation directive when specifics aren't known yet. Both are valid.

**DoD** — unambiguous completion criteria.

## Important Rules

- **Minimum viable team** — fewer agents doing more is better than many agents doing little
- **DoR/DoD in every prompt** — no agent starts without clear inputs and expected outputs
- **Do NOT shut down the team** — agents persist for follow-up. Ask the user before any shutdown.
- **Dynamic scaling** — if during execution you notice a subtask that could be parallelized, suggest spawning an additional agent to the user.
