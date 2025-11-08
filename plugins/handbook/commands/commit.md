---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: "[--no-verify]"
description: Create a git commit
---

# Commit

Create well-formatted commits with conventional commit messages and emojis.

## Features:
- Runs pre-commit checks by default (lint, build, generate docs)
- Automatically stages files if none are staged
- Uses conventional commit format with descriptive emojis
- Suggests splitting commits for different concerns

## Usage:
- `/commit` - Standard commit with pre-commit checks
- `/commit --no-verify` - Skip pre-commit checks if $ARGUMENTS contains `--no-verify` flag

## Commit Types:
- ✨ feat: New features
- 🐛 fix: Bug fixes
- 📝 docs: Documentation changes
- ♻️ refactor: Code restructuring without changing functionality
- 🎨 style: Code formatting, missing semicolons, etc.
- ⚡️ perf: Performance improvements
- ✅ test: Adding or correcting tests
- 🧑‍💻 chore: Tooling, configuration, maintenance
- 🚧 wip: Work in progress
- 🔥 remove: Removing code or files
- 🚑 hotfix: Critical fixes
- 🔒 security: Security improvements

## Process:
1. Check for staged changes (!`git status`)
2. If no staged changes, review and stage appropriate files
3. Run pre-commit checks (unless --no-verify)
4. Analyze changes to determine commit type
5. Generate descriptive commit message
6. Include scope if applicable: `type(scope): description`
7. Add body for complex changes explaining why
8. NOTE: Exclude Claude co-authorship footer from commits
9. Execute commit

## Best Practices:
- Keep commits atomic and focused
- Write in imperative mood ("Add feature" not "Added feature")
- Explain why, not just what
- Reference issues/PRs when relevant
- Split unrelated changes into separate commits