---
title: "Use Plugins"
sidebar_position: 9
---

# Use Plugins

Claude Code plugins are custom collections of extension points that can be installed with a single command. They allow you to bundle and share development workflows, tools, and best practices.

> 💡 Plugins work across both terminal and VS Code environments, making them a portable way to customize your Claude Code experience.


## What are Plugins?

Plugins can include five main types of customizations:

1. **Slash commands** - Custom shortcuts for frequently-used operations
2. **Subagents** - Purpose-built agents for specialized development tasks
3. **Skills** - Model-invoked capabilities that Claude autonomously triggers based on context
4. **MCP servers** - Connections to tools and data sources through the Model Context Protocol
5. **Hooks** - Customizations to Claude Code's behavior at key workflow points

## Installing Plugins

Use the `/plugin` command to install a plugin:

```
/plugin install <plugin-name-or-url>
```

Plugins can be toggled on and off as needed, helping reduce system prompt complexity when not in use.

## Benefits

- **Share development setups** - Distribute your workflows across projects
- **Standardize team practices** - Ensure consistent approaches across your team
- **Quick tool integration** - Connect tools and data sources easily
- **Enforce standards** - Maintain engineering best practices automatically
- **Bundle customizations** - Group related configurations together

## Examples

The Claude Code team maintains official plugin examples that you can learn from or use directly:

[github.com/anthropics/claude-code/tree/main/plugins](https://github.com/anthropics/claude-code/tree/main/plugins)

These examples demonstrate best practices and common patterns for building your own plugins.

## Learn More

For detailed information about creating and using plugins, see the [official announcement](https://www.anthropic.com/news/claude-code-plugins).

## Related Topics

- [Use Agent Skills](/tips-and-tricks/agent-skills) - Learn about model-invoked Skills that extend Claude's capabilities
