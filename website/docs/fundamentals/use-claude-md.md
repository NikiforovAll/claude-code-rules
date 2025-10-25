---
title: "Use CLAUDE.md"
sidebar_position: 2
---

# Use CLAUDE.md

CLAUDE.md is Claude Code's persistent memory system that stores instructions and preferences across sessions. It enables teams and individuals to maintain consistent coding standards, workflows, and project context without repeating them in every conversation.

## What is CLAUDE.md?

CLAUDE.md files act as persistent memory for Claude Code, automatically loaded at the start of each session. They can contain:

- **Coding standards**: Formatting rules, naming conventions, architecture patterns
- **Project context**: Technology stack, key decisions, system architecture
- **Team conventions**: Git workflows, testing approaches, review processes
- **Personal preferences**: Your preferred coding style, frequently used commands

These instructions are always available to Claude Code without cluttering your conversation context.

## Memory Hierarchy

Claude Code loads CLAUDE.md files from multiple locations, with later tiers overriding earlier ones:

- **Enterprise Policy**
  - Organization-wide security policies and company standards
  - Use for: Mandatory rules that apply to all developers and projects

- **Project Memory** (`./CLAUDE.md` or `./.claude/CLAUDE.md`)
  - Team-shared project conventions, typically committed to version control
  - Use for: Tech stack, architecture patterns, team coding standards

- **User Memory** (`~/.claude/CLAUDE.md`)
  - Personal preferences that apply across all your projects
  - Use for: Your coding style, preferred workflows, communication preferences


## How Memory Resolution Works

Claude Code resolves memory files progressively with a smart discovery system:

### Progressive Directory Resolution

Starting from your current working directory (cwd), Claude Code:

1. **Recurses upward**: Reads CLAUDE.md files from cwd up to (but not including) the root directory `/`
2. **Discovers subtrees**: When you access subdirectories, loads their CLAUDE.md files on-demand

### Example: Monorepo Structure

```
/workspace/
├── CLAUDE.md                    # Workspace-level conventions
├── frontend/
│   ├── CLAUDE.md               # Frontend-specific rules
│   └── packages/
│       ├── ui/
│       │   └── CLAUDE.md      # UI package conventions
│       └── utils/
│           └── CLAUDE.md      # Utils package conventions
└── backend/
    └── CLAUDE.md              # Backend-specific rules
```

**When working in `/workspace/frontend/packages/ui/`**:

Claude Code loads (in order):
1. `/workspace/CLAUDE.md` (workspace conventions)
2. `/workspace/frontend/CLAUDE.md` (frontend conventions)
3. `/workspace/frontend/packages/ui/CLAUDE.md` (UI-specific conventions)
4. `~/.claude/CLAUDE.md` (your personal preferences)

Each file can add or override instructions from previous files in the chain.

## Managing Your Memory Files

### Quick Addition with `#`

Start your input with `#` to add instructions to a memory file:

```
# Remember to use async/await instead of .then() chains
```

Claude Code will prompt you to select which CLAUDE.md file to update.

### Direct Editing with `/memory`

Use the `/memory` command to:
- View all loaded memory files
- Open memory files in your editor
- See the complete memory hierarchy

```bash
/memory
```

This displays the import chain and lets you edit files directly.

## Best Practices

### 1. Be Specific

```markdown
# ❌ Vague
- Write good code
- Follow best practices

# ✅ Specific
- Use 2-space indentation for TypeScript
- Max function length: 50 lines
- Prefer composition over inheritance
```

### 2. Structure with Markdown

Use headings, lists, and code blocks for scannable content:

```markdown
# Testing Standards

## Unit Tests
- Test one thing at a time
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

## Integration Tests
- Test critical user paths
- Use test database, not production
- Clean up after each test
```

### 3. Keep It Current

Review and update CLAUDE.md files as your project evolves:
- Remove outdated conventions
- Add new patterns discovered
- Update architectural decisions

### 4. Layer Appropriately

- **Enterprise**: Security policies, company standards (rarely change)
- **Project**: Team conventions, architecture (change occasionally)
- **User**: Personal preferences (change as you learn)

## Using Imports

For complex projects, you can break down CLAUDE.md into smaller, focused files using imports.

### Import Syntax

Reference files using `@path/to/file`:

```markdown
# CLAUDE.md (main file)

# Architecture
@docs/architecture.md

# Coding Standards
@docs/typescript-conventions.md
@docs/react-patterns.md
```

### Benefits of Imports

1. **Modular Organization**: Keep each file focused on a single topic
2. **Reuse Across Projects**: Share common conventions via imports

- **Recursive imports**: Imported files can import others (max 5 levels deep)
- **Code block safety**: Imports inside code blocks are ignored

## Related Topics

- [Manage Context](./manage-context) - Learn how CLAUDE.md reduces context window usage by storing persistent instructions
- [Understanding Building Blocks](./understanding-building-blocks) - Learn about all Claude Code customization features

## References

- [Official Memory Documentation](https://docs.claude.com/en/docs/claude-code/memory)
