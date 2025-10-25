---
title: "Install ripgrep for faster search"
sidebar_position: 14
---

# Install `ripgrep` for faster search

## Grep Tool

Claude Code has a built-in **Grep tool** powered by `ripgrep` for searching code:

- **Fast regex search**: Full regex pattern support
- **Smart filtering**: Filter by file type (`type: "js"`) or glob patterns (`glob: "*.ts"`)
- **Multiple output modes**:
  - `content` - shows matching lines with context
  - `files_with_matches` - shows only file paths
  - `count` - shows match counts
- **Respects .gitignore**: Automatically excludes ignored files
- **Context lines**: Supports `-A`, `-B`, `-C` flags for surrounding context

## Performance Tip

Installing ripgrep on your system makes the Grep tool significantly faster (5-10x), especially in large codebases. Claude Code will automatically use it if available.

```bash
# Verify ripgrep is installed
rg --version
```

Without ripgrep installed, searches may fall back to slower methods.

Interesting discussion can be found at [Quick & easy tip to make claude code find stuff faster (it really works)](https://www.reddit.com/r/ClaudeCode/comments/1o4vy1a/quick_easy_tip_to_make_claude_code_find_stuff/)