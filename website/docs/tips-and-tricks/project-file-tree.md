---
title: "Include Project File Tree in CLAUDE.md"
sidebar_position: 14
---

# Include Project File Tree in CLAUDE.md

Including your project's file tree in your `CLAUDE.md` file helps Claude Code navigate files faster and understand your codebase structure at a glance.

## Why This Helps

- **Faster Navigation**: Claude can quickly understand your project structure without searching
- **Better Context**: Reduces the back-and-forth needed to clarify file locations
- **Improved Code Suggestions**: Claude provides more accurate, context-aware suggestions
- **Large Codebase Support**: Essential for projects with 100+ files where Claude might get lost

## How to Generate File Tree

### Basic Command

```bash
tree .
```

### Exclude Specific Folders

Use the `-I` argument to exclude folders like `node_modules`, `dist`, `.git`, etc.:

```bash
tree . -I "node_modules|dist|.git|build|coverage"
```

## Example CLAUDE.md Structure

````markdown
# Project Overview

Brief description of your project.

## File Structure

```
your-project/
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   └── About.tsx
│   └── utils/
│       └── helpers.ts
├── tests/
│   └── components/
├── package.json
└── README.md
```

## Key Components

- `src/components/` - Reusable UI components
- `src/pages/` - Application pages
- `src/utils/` - Helper functions and utilities
````

## Best Practices

1. **Keep It Updated**: Update the tree when you add/remove significant files or folders
2. **Be Selective**: Use exclusion patterns to avoid cluttering with temporary or generated files  
3. **Add Context**: Include brief descriptions of what each major directory contains
4. **Consider Size**: For very large projects (12,000+ files), consider showing only top-level structure or key directories

## Token Considerations

For large projects, be mindful of token usage. You can:
- Show only directory structure without individual files
- Focus on the most important parts of your codebase
- Use abbreviated trees for different sections

> 💡 **Pro tip**: Even an outdated tree is better than no tree at all. Claude can still use it as a general guide to your project structure.

## Source

This tip comes from the Reddit community discussion: [Quick tip for Claude Code: include your project's file tree in CLAUDE.md](https://www.reddit.com/r/ClaudeAI/comments/1o6rtb7/quick_tip_for_claude_code_include_your_projects/)