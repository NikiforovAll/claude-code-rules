---
title: "Use git worktree"
sidebar_position: 12
---

# Use `git worktree` for parallel development

You can use `git worktree` to create multiple working directories for the same repository. This is useful for parallel development, e.g., working on multiple features or bug fixes simultaneously without needing to switch branches in a single working directory.


```bash
git worktree add ../feature-branch feature-branch
```