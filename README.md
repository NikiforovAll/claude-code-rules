# 📖 [Claude Code Handbook](https://nikiforovall.blog/claude-code-rules/)

A collection of [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) recommendations and practices.

Learn practical techniques to enhance your AI-assisted development workflow with Claude Code.

![](./assets/handbook-demo.png)

## Plugins

This repository contains next plugins:

- **`handbook`** - Core plugin with best practices, commands, agents, and MCP integrations
- **`handbook-extras`** - Experimental and extended features plugin
- **`handbook-qa`** - Browser automation and QA testing tools with Playwright integration
- **`handbook-dotnet`** - .NET-specific development skillset
- **`handbook-context7`** - Context7 MCP server for fetching latest library documentation
- **`handbook-sounds`** - Audio feedback for Claude Code events on Windows

Plus a marketplace for centralized plugin discovery and installation.

## Quick Start

Use Claude Code's `/plugin` command for the quickest installation:

```bash
# Add the marketplace (one-time setup)
/plugin marketplace add nikiforovall/claude-code-rules

# Install core plugin
/plugin install handbook

# Install extras plugin
/plugin install handbook-extras

# Install QA plugin
/plugin install handbook-qa

# Install dotnet plugin
/plugin install handbook-dotnet

# Install context7 plugin
/plugin install handbook-context7

# Install sounds plugin
/plugin install handbook-sounds
```
