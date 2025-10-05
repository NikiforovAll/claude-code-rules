---
title: "Skip Permissions Mode"
sidebar_position: 1
---

You can use `--dangerously-skip-permissions` to run Claude Code without being prompted for permissions. 

⚠️ This is useful in case you want to move quickly, but please be cautious as this may introduce you to risks if Claude Code makes unintended changes to your codebase or  MCP requests.

Use this flag to skip permission prompts when you trust Claude Code with your codebase.

```bash
claude --dangerously-skip-permissions
```

💡 Setup alias:

```bash
alias ccsp="claude --dangerously-skip-permissions"
```