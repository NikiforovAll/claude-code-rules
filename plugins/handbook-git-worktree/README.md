# Git Worktree

Git worktree management for working on multiple branches simultaneously.

## Features

- Create worktrees from local, remote, or new branches
- List all active worktrees with navigation commands
- Delete and clean up worktrees
- Sibling directory pattern: `../<project>-<branch>`

## Installation

```bash
/plugin marketplace add nikiforovall/claude-code-rules
/plugin install handbook-git-worktree
```

## Usage

The skill activates automatically when you mention worktree tasks:

```
"Manage my worktrees"
"Create worktree from remote branch feature-x"
"List all worktrees"
"Delete worktree for branch hotfix-123"
```

**Example:**
```
You: "Create a worktree for the feature-auth branch"
Claude: Creates ../myproject-feature-auth and provides cd command
```
