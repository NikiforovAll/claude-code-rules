---
title: "Connect to IDE"
sidebar_position: 15
---

# Connect to IDE

You can connect to VSCode or JetBrains IDEs to get context for files and diagnostics.

For external terminals, use the `/ide` command to connect Claude Code to your VS Code instance. To configure, run claude, enter `/config`, and set the diff tool to auto for automatic IDE detection.

## Features:

* Selection context sharing (current selection/tab is automatically shared with Claude Code)
* Diff viewing in the IDE instead of terminal, 
* File reference shortcuts (Cmd+Option+K on Mac or Alt+Ctrl+K on Windows/Linux to insert file references like @File#L1-99)
* Automatic diagnostic sharing (lint and syntax errors).

> 💡 You can nudge Claude Code to get the diagnostics from a file by saying something like: "Check all diagnostics for Program.cs with warning level and fix them"

See the [Visual Studio Code Integration](https://docs.claude.com/en/docs/claude-code/vs-code)
