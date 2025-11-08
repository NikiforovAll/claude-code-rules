---
name: git-worktree
description: This skill should be used when the user wants to manage Git worktrees - creating worktrees from local or remote branches, listing active worktrees with details, deleting worktrees, or switching between worktrees. Ideal for working on multiple branches simultaneously without stashing changes.
---

# Git Worktree Management

## Overview

This skill provides comprehensive Git worktree management capabilities, enabling work on multiple branches simultaneously in isolated directories. Worktrees eliminate the need for stashing when switching contexts and are ideal for parallel development, quick bug fixes, and code reviews.

## When to Use This Skill

Use this skill when the user wants to:
- Create a new worktree from a local branch, remote branch, or new branch
- List all active worktrees with detailed information
- Delete and clean up worktrees
- Get navigation commands to switch between worktrees
- Set up parallel development environments

## How It Works

### Configuration

**Location Strategy**: Sibling directory pattern
- Worktrees are created outside the main repository: `../<project>-<branch>`
- Example: Main repo at `~/dev/myproject`, worktree at `~/dev/myproject-feature-x`
- Benefits: Clean separation, no nested repos, IDE-friendly

**Naming Convention**: `<project>-<branch>`
- Project name extracted using: `basename "$(git rev-parse --show-toplevel)"`
- Example: `myproject-feature-auth`, `myapp-bugfix-login`

### Interface

**Hybrid Mode**: Accepts arguments when provided, prompts when missing

**Usage patterns**:
```
# Interactive menu
User: "Manage my worktrees"
User: "Create a worktree"

# Direct with arguments
User: "Create worktree from remote branch feature-x"
User: "List all worktrees"
User: "Delete worktree for branch hotfix-123"
```

## Core Operations

### 1. List Worktrees

**Purpose**: Show all active worktrees with detailed information

**What to display**:
- Index number for easy reference
- Worktree path
- Branch name
- HEAD commit hash (short)
- Commit message (first line)
- Indicator for current worktree

**Implementation**:
```bash
# Get project name
project=$(basename "$(git rev-parse --show-toplevel)")

# List worktrees with details
git worktree list -v
```

**Output format**:
```
Git Worktrees for myproject:

1. /Users/dev/myproject (main)
   abc1234 Initial commit
   [CURRENT]

2. /Users/dev/myproject-feature-x (feature-x)
   def5678 Add authentication logic

3. /Users/dev/myproject-hotfix (hotfix-123)
   789abcd Fix login bug
```

### 2. Create Worktree from Remote Branch

**Purpose**: Fetch and create a worktree from a remote branch

**Steps**:
1. Validate we're in a git repository
2. Get project name: `project=$(basename "$(git rev-parse --show-toplevel)")`
3. Extract branch name from remote reference (e.g., `origin/feature-x` → `feature-x`)
4. Check if worktree already exists (warn and skip if it does)
5. Fetch remote branch: `git fetch origin <branch-name>`
6. Verify remote branch exists (check exit code)
7. Determine worktree path: `../<project>-<branch-name>`
8. Create worktree: `git worktree add ../<project>-<branch-name> origin/<branch-name>`
9. Show success message with path and navigation command

**Error handling**:
- Not in git repo: Show clear error message
- Worktree already exists: "Worktree for branch 'X' already exists at Y. Use 'list' to see all worktrees."
- Remote branch doesn't exist: "Remote branch 'origin/X' not found. Available branches: [list]"

**Success output**:
```
✓ Created worktree for remote branch 'feature-x'

Location: /Users/dev/myproject-feature-x
Branch: feature-x (tracking origin/feature-x)

To switch to this worktree:
  cd ../myproject-feature-x

To start working:
  cd ../myproject-feature-x && code .
```

### 3. Create Worktree from Local Branch

**Purpose**: Create a worktree from an existing local branch

**Steps**:
1. Validate we're in a git repository
2. Get project name
3. Verify local branch exists: `git rev-parse --verify <branch-name>`
4. Check if worktree already exists
5. Create worktree: `git worktree add ../<project>-<branch-name> <branch-name>`
6. Show success message with navigation

**Error handling**:
- Local branch doesn't exist: "Local branch 'X' not found. Available branches: [list local branches]"
- Worktree already exists: Same as remote case

### 4. Create Worktree with New Branch

**Purpose**: Create a worktree with a brand new branch

**Parameters needed**:
- New branch name
- Base branch (optional, default: current branch)

**Steps**:
1. Validate we're in a git repository
2. Get project name
3. Get base branch (use current if not specified)
4. Check if worktree directory already exists
5. Create worktree with new branch: `git worktree add -b <new-branch> ../<project>-<new-branch> <base-branch>`
6. Show success message

**Success output**:
```
✓ Created new worktree with branch 'experiment-auth'

Location: /Users/dev/myproject-experiment-auth
Branch: experiment-auth (based on main)

To switch to this worktree:
  cd ../myproject-experiment-auth
```

### 5. Delete Worktree

**Purpose**: Remove a worktree and show prune command

**Steps**:
1. If no branch specified, list all worktrees for selection
2. Verify worktree exists for specified branch
3. Remove worktree: `git worktree remove <path>` or manually `rm -rf <path>`
4. Show manual prune command (don't auto-execute per user preference)

**Output**:
```
✓ Removed worktree at /Users/dev/myproject-feature-x

To clean up metadata, run:
  git worktree prune
```

### 6. Prune Worktrees

**Purpose**: Clean up worktree metadata

**Steps**:
1. Run: `git worktree prune`
2. Show what was cleaned

**Output**:
```
✓ Pruned stale worktree metadata

Run 'git worktree list' to see remaining worktrees.
```

### 7. Switch Helper

**Purpose**: Show easy navigation to worktrees

**Implementation**:
1. List all worktrees (numbered)
2. Provide copy-ready cd commands

**Output**:
```
Available worktrees:

1. main (current)
   cd /Users/dev/myproject

2. feature-x
   cd /Users/dev/myproject-feature-x

3. hotfix-123
   cd /Users/dev/myproject-hotfix
```

## Interactive Flow

When invoked without arguments:

1. Show menu:
   ```
   Git Worktree Management

   1. List all worktrees
   2. Create from remote branch
   3. Create from local branch
   4. Create new branch
   5. Delete worktree
   6. Prune metadata
   7. Switch between worktrees
   ```

2. Prompt for selection
3. For create operations, prompt for required info (branch name, base branch, etc.)
4. Execute operation
5. Show results with clear next steps

## Direct Command Parsing

When arguments are provided, parse intent:
- "list" → List operation
- "create remote <branch>" → Create from remote
- "create local <branch>" → Create from local
- "create new <branch> [from <base>]" → Create new branch
- "delete <branch>" → Delete worktree
- "prune" → Prune metadata
- "switch" → Switch helper

## Error Handling Checklist

Before any operation:
- ✓ Verify in git repository: `git rev-parse --git-dir`
- ✓ Get project name successfully
- ✓ Validate branch exists (for remote/local operations)
- ✓ Check worktree doesn't already exist (for create operations)
- ✓ Provide actionable error messages with suggestions
