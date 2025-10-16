---
title: "Fix - Maintain working dir"
sidebar_position: 18
---

# Maintain Working Directory

## Problem

By default, when `cd` is used in a bash command, it changes the current working directory permanently for the rest of the session. This can cause Claude Code to lose track of the project root directory, leading to confusion in subsequent commands and file operations.

## Solution

Enable the `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` flag to automatically reset the working directory to the project root after each bash command:

```bash
export CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1
```

This ensures that Claude Code always maintains its working directory at the project root, regardless of any `cd` commands executed during the session.
