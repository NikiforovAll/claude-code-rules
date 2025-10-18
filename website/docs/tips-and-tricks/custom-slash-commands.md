---
title: "Create Custom Slash Commands"
sidebar_position: 7
---

# Create Custom Slash Commands

You can create [custom slash commands](https://docs.claude.com/en/docs/claude-code/slash-commands) to streamline your workflow in Claude Code. It makes sense to create reusable commands for tasks you perform frequently.

Let's explore anatomy of a slash command and how to create your own.

All you need to do is to create a file in the `~/.claude/commands/` directory. The filename will be the command name.

## Write your commands

💡 When you craft a prompt you can ask Claude to generate a draft and improve it incrementally.

**Example:**

```txt
Generate a pros&cons prompt

hint: use this guide - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
```

For more comprehensive approach for prompt generation see [Prompt Generator - Meta Prompting](/component-reference/commands/prompt-generator).


## Example: `/explain`


The command definition starts with markdown frontmatter that defines the command arguments and description. This part is optional, but recommended for better user experience. This impact the way the command is presented in the UI.

Next, we can use user input available as `$1`, `$2`, etc (or `$ARGUMENTS` for all arguments) to add additional context to the prompt.

Finally, we define the prompt that will be sent to Claude. You can use any valid markdown syntax here, including code blocks, lists, and headings.

```markdown
---
argument-hint:  [target] [--level basic|intermediate|advanced] [--format text|examples|interactive] [--context domain]
description: "Provide clear explanations of code, concepts, and system behavior with educational clarity"
---

Target: $1, Level : $2, Format : $3, Context : $4

## Behavioral Flow
1. **Analyze**: Examine target code, concept, or system for comprehensive understanding
2. **Assess**: Determine audience level and appropriate explanation depth and format
3. **Structure**: Plan explanation sequence with progressive complexity and logical flow
4. **Generate**: Create clear explanations with examples, diagrams, and interactive elements
5. **Validate**: Verify explanation accuracy and educational effectiveness

Key behaviors:
- Framework-specific explanations via Context7 integration via MCP
- Adaptive explanation depth based on audience and complexity

## Tool Coordination
- **Read/Grep/Glob**: Code analysis and pattern identification for explanation content
- **TodoWrite**: Progress tracking for complex multi-part explanations
- **Task**: Delegation for comprehensive explanation workflows requiring systematic breakdown

## Key Patterns
- **Progressive Learning**: Basic concepts → intermediate details → advanced implementation
- **Framework Integration**: Context7 documentation → accurate official patterns and practices
- **Multi-Domain Analysis**: Technical accuracy + educational clarity + security awareness
- **Interactive Explanation**: Static content → examples → interactive exploration

## Examples

### Basic Code Explanation

<example>
# Clear explanation with practical examples for beginners
# Educator persona provides learning-optimized structure
</example>

### Framework Concept Explanation

<example>
/explain react-hooks --level intermediate --context react
# Structured explanation with progressive complexity
</example>

### System Architecture Explanation

<example>
/explain microservices-system --level advanced --format interactive
# Architect persona explains system design and patterns
# Interactive exploration with Sequential analysis breakdown
</example>

### Security Concept Explanation

<example>
/explain jwt-authentication --context security --level basic
# Security persona explains authentication concepts and best practices
# Framework-agnostic security principles with practical examples
</example>

## Boundaries

**Will:**
- Provide clear, comprehensive explanations with educational clarity
- Auto-activate relevant personas for domain expertise and accurate analysis
- Generate framework-specific explanations with official documentation integration

**Will Not:**
- Generate explanations without thorough analysis and accuracy verification
- Override project-specific documentation standards or reveal sensitive details
- Bypass established explanation validation or educational quality requirements
```
