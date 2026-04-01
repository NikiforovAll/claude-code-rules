# Handbook Code Review

Code review plugin with a standalone reviewer agent and two skill strategies.

## Agent

- **code-reviewer** — Systematic code review against a base branch. Analyzes diffs directly for critical issues, code quality, and maintainability.

## Skills

- **subagent-review** — One-shot review using three parallel disposable subagents (reuse, quality, efficiency). Use for quick reviews.
- **team-review** — Review using three persistent named team members. Use when you want to ask follow-up questions to specific reviewers.
