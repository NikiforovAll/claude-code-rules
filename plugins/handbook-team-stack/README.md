# Team Stack

Agent team composition and ADR-based planning for Claude Code.

## Skills

### `/team-stack`

Analyzes a task, proposes an agent team, and creates it after confirmation.

**Flow:** describe task → analysis (silent) → team proposal → user confirms → team created

- Infers scope, parallelization potential, and risk from codebase context
- Proposes minimum viable team with roles, responsibilities, and isolation mode
- Structures every agent prompt with **Definition of Ready / Definition of Done**
- Leverages existing plans, ADRs, or task lists as input
- Teams persist for follow-up — no auto-shutdown

**Example roles:** implementer, reviewer, test-writer, investigator, architect, migrator

### `/adr-plan`

Decomposes a task into an Architecture Decision Record with ordered implementation steps.

**Flow:** describe task → codebase exploration → ADR with steps → user confirms

- Produces ADR with context, decision, alternatives table, and implementation steps
- Each step has files, dependencies, and concrete "done when" criteria
- Steps map naturally to work units for `/team-stack`
- Uses `npx adr` CLI for file management (auto-detects or initializes ADR directory)
- Skips ceremony for simple tasks

## Usage

The skills work independently or chained:

```
# Plan first, then staff
/adr-plan
/team-stack

# Or jump straight to team composition
/team-stack
```

## Install

```bash
claude plugin add /path/to/handbook-team-stack
```
