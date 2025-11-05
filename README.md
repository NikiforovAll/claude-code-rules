# 📖 [Claude Code Handbook](https://nikiforovall.blog/claude-code-rules/)

A collection of [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) recommendations and practices.

Learn practical techniques to enhance your AI-assisted development workflow with Claude Code.

![](./assets/handbook-demo.png)

## Plugins

This repository contains four plugins:

- **`cc-handbook`** - Core plugin with best practices, commands, agents, and MCP integrations
- **`cc-handbook-extras`** - Experimental and extended features plugin
- **`cc-handbook-qa`** - Browser automation and QA testing tools with Playwright integration
- **`cc-handbook-dotnet`** - .NET-specific development skillset

Plus a marketplace for centralized plugin discovery and installation.

## Quick Start

Use Claude Code's `/plugin` command for the quickest installation:

```bash
# Add the marketplace (one-time setup)
/plugin marketplace add nikiforovall/claude-code-rules

# Install core plugin
/plugin install cc-handbook

# Install extras plugin
/plugin install cc-handbook-extras

# Install QA plugin
/plugin install cc-handbook-qa

# Install dotnet plugin
/plugin install cc-handbook-dotnet
```
