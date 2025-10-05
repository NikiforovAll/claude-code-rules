---
title: "Know Available Tools"
sidebar_position: 2
---

# Know Available Tools


It is important to know the available tools at your disposal when working with Claude Code. This is also useful when you want to configure permissions for specific tools.

See [docs/claude-code/settings#tools-available-to-claude](https://docs.claude.com/en/docs/claude-code/settings#tools-available-to-claude)

---

## Command `/tools`

Claude Code in a way is self-aware of its capabilities. You can ask it to list available tools. See `/tools` command.

```markdown
---
description: List Claude Code Tools
---

List available Claude Code tools for various development tasks. 

List tools as-is. Write two sections with Built-in tools and Custom tools. 

For each tool, provide a brief description of its purpose.

## Output Format

<output>
# Built-in Tools
- Tool Name: Description of the tool's purpose.

# Custom Tools
- Tool Name($TOOL_TYPE|COMMAND|AGENT|MCP): Description of the tool's purpose.
</output>

### Constraints

* For COMMAND tools, check `.claude/commands`.
* For AGENT tools, check `.claude/agents`.
* For MCP tools, check Claude Code available MCP server installed using built-in command. MCP tools goes to Custom Tools section.
```