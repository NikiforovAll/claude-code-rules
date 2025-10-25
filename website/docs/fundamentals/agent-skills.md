---
title: "Use Custom Agent Skills"
sidebar_position: 5
---

# Use Custom Agent Skills

Agent Skills are modular capabilities that extend Claude's functionality through organized folders containing instructions, scripts, and resources. They enable teams to package expertise into discoverable, reusable components.

## Overview

Agent Skills differ from slash commands in a fundamental way:

- **Slash Commands**: User-invoked - you explicitly call them (e.g., `/commit`)
- **Agent Skills**: Model-invoked - Claude autonomously triggers them based on request context and the Skill's description

## Key Benefits

- **Extend Capabilities**: Add specific workflows and expertise to Claude
- **Team Collaboration**: Share Skills across teams via git
- **Reduce Repetition**: Eliminate repetitive prompting for common tasks
- **Composability**: Combine multiple Skills for complex workflows
- **Discoverability**: Claude automatically finds and uses relevant Skills

## Skill Types

### Personal Skills

**Location**: `~/.claude/skills/`

Available across all your projects. Ideal for:
- Individual workflows
- Experimental capabilities
- Personal productivity tools

### Project Skills

**Location**: `.claude/skills/` (within project)

Shared with teams via git. Best for:
- Team workflows
- Project-specific expertise
- Standardized processes

### Plugin Skills

Bundled with Claude Code plugins and automatically available upon installation.

## Creating a Skill

Each Skill requires a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: Your Skill Name
description: Brief description of what this Skill does and when to use it
---

# Skill Instructions

Your detailed instructions go here...
```

### Critical: The Description Field

The `description` field is **critical for discovery**. It determines when Claude will activate your Skill.

**Good descriptions include:**
- What the Skill does
- When to use it
- Specific triggers or use cases

**Examples:**

✅ **Good**: "Extract text and tables from PDF files when the user asks to read or analyze PDF content"

❌ **Bad**: "Helps with documents"

✅ **Good**: "Generate TypeScript types from JSON schemas, activated when user wants to create types from JSON or OpenAPI specs"

❌ **Bad**: "Works with types"

## Supporting Files

Skills can include optional files alongside `SKILL.md`:

```
.claude/skills/my-skill/
├── SKILL.md           # Required: Skill definition
├── reference.md       # Optional: Reference documentation
├── examples/          # Optional: Example files
├── scripts/           # Optional: Helper scripts
│   └── process.sh
└── templates/         # Optional: Template files
    └── template.md
```

Claude loads these files progressively, managing context efficiently.

## Tool Access Restriction

Use the `allowed-tools` frontmatter to limit Claude's capabilities within a Skill:

```yaml
---
name: Read-Only Analyzer
description: Analyze code structure without making changes
allowed-tools: Read, Grep, Glob, Bash(ls:*)
---
```

This restricts Claude to specified tools without requiring permission requests—useful for:
- Read-only workflows
- Security-sensitive operations
- Preventing accidental modifications

## Example: PDF Text Extractor Skill

```yaml
---
name: PDF Text Extractor
description: Extract text and tables from PDF files when user asks to read or analyze PDF content
allowed-tools: Read, Bash(pdftotext:*)
---

# PDF Text Extraction Skill

When the user provides a PDF file or asks to analyze PDF content:

1. Use `pdftotext` to extract text content
2. Format the output for readability
3. If tables are present, attempt to preserve structure
4. Provide a summary of the extracted content

## Prerequisites

Ensure `pdftotext` is installed on the system.

## Usage Examples

- "Extract text from report.pdf"
- "What does this PDF say?"
- "Analyze the tables in data.pdf"
```

## Best Practices

### Keep Skills Focused

✅ **Good**: One Skill per capability
- PDF text extraction
- Database migration helper

❌ **Bad**: Broad, multi-purpose Skills
- Document helper (too vague)
- Developer tools (too broad)

### Write Specific Descriptions

Include concrete triggers and use cases in your description:

```yaml
# Good
description: Generate conventional git commit messages with emojis when user asks to commit changes

# Better
description: Create conventional git commits (feat, fix, docs) with descriptive emojis. Activated when user says "commit", "create commit", or "commit these changes"
```

## Reference

For more information, see the official documentation:
- [Introducing Agent Skills](https://www.anthropic.com/news/skills)
- [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [anthropics/skills](https://github.com/anthropics/skills)
- [Claude Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)
- ⭐ [Skill authoring best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)