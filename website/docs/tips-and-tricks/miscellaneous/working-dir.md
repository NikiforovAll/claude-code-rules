---
title: "Fix - Maintain working dir"
sidebar_position: 18
---

# If you find Claude Code struggle with working dir

Use `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`

You may have noticed that Claude gets really confused about its current directory after doing that.

The problem is that cd changes the current working directory permanently (for the rest of the session). So any steps after that will also use the new CWD. Which Claude does not expect.

Anyway they recently added a flag to change this:

```bash
export CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1
```
