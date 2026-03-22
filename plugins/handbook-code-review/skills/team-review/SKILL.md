---
name: team-review
description: Review changed code for reuse, quality, and efficiency using a team of persistent named reviewers. This skill should be used when the user says "team review", "review with team", or wants parallel code review with persistent team members for follow-up questions. Similar to /subagent-review but reviewers persist after review.
allowed-tools: Agent, Bash(git diff *), Bash(git log *), Bash(git status *), Read, Grep, Glob, TaskCreate, TaskUpdate, TaskList, TeamCreate, TeamDelete, SendMessage
---

# Team Review: Code Review with Persistent Team Members

Review all changed files for reuse, quality, and efficiency using a **team of named reviewers** that persist for follow-up questions.

## Phase 1: Identify Changes

Run `git diff` (or `git diff HEAD` if there are staged changes) to see what changed. If there are no git changes, review the most recently modified files that the user mentioned or that you edited earlier in this conversation.

Store the full diff text — you will pass it to each reviewer.

## Phase 2: Create Review Team and Spawn Reviewers

Create a team (or reuse an existing one) and spawn **three named team members** concurrently using the Agent tool. Each member gets the full diff as context.

Use `run_in_background: true` for all three so they run in parallel. Give each a descriptive `name` parameter.

### Member 1: reuse-reviewer

**Prompt:** You are a code reuse reviewer. Here is the diff to review:

```
<paste full diff>
```

For each change:
1. Search for existing utilities and helpers that could replace newly written code. Look for similar patterns elsewhere in the codebase.
2. Flag any new function that duplicates existing functionality. Suggest the existing function to use instead.
3. Flag any inline logic that could use an existing utility — hand-rolled string manipulation, manual path handling, custom environment checks, ad-hoc type guards.

Report findings as a bulleted list. If the code is clean, say so.

### Member 2: quality-reviewer

**Prompt:** You are a code quality reviewer. Here is the diff to review:

```
<paste full diff>
```

Review for:
1. **Redundant state**: state that duplicates existing state, cached values that could be derived
2. **Parameter sprawl**: adding new parameters instead of generalizing
3. **Copy-paste with slight variation**: near-duplicate code blocks
4. **Leaky abstractions**: exposing internal details that should be encapsulated
5. **Stringly-typed code**: using raw strings where constants or enums exist
6. **Unnecessary nesting**: wrapper elements that add no value
7. **Unnecessary comments**: comments explaining WHAT — delete; keep only non-obvious WHY

Report findings as a bulleted list. If the code is clean, say so.

### Member 3: efficiency-reviewer

**Prompt:** You are an efficiency reviewer. Here is the diff to review:

```
<paste full diff>
```

Review for:
1. **Unnecessary work**: redundant computations, repeated file reads, duplicate API calls, N+1 patterns
2. **Missed concurrency**: independent operations run sequentially when they could be parallel
3. **Hot-path bloat**: blocking work added to startup or per-request hot paths
4. **Recurring no-op updates**: state updates that fire unconditionally — add change-detection guards
5. **Unnecessary existence checks**: pre-checking before operating (TOCTOU anti-pattern)
6. **Memory**: unbounded data structures, missing cleanup, event listener leaks
7. **Overly broad operations**: reading entire files when only a portion is needed

Report findings as a bulleted list. If the code is clean, say so.

## Phase 3: Collect and Act on Findings

Wait for all three reviewers to complete. Aggregate their findings and fix each issue directly. If a finding is a false positive or not worth addressing, note it and move on.

When done, briefly summarize what was fixed (or confirm the code was already clean).

## Important

- Do **NOT** shut down the team after review — reviewers persist for follow-up questions
- Each reviewer should use `Bash(git diff)`, `Read`, `Grep`, `Glob` to explore the codebase
- Pass the `team_name` parameter when spawning agents so they join the same team
- Create tasks for each reviewer to track progress
