---
title: "🔌 Plugins"
sidebar_position: 3
---

# Plugins

Claude Code Handbook provides five complementary plugins to enhance your AI-assisted development workflow.

```bash
# Add the marketplace
/plugin marketplace add nikiforovall/claude-code-rules
```

## <span className="badge badge--primary">cc-handbook</span>

Core plugin with essential tools and best practices for Claude Code development.


```bash
/plugin install cc-handbook
```

## <span className="badge badge--secondary">cc-handbook-extras</span>

Extended features and experimental tools for advanced use cases.

```bash
/plugin install cc-handbook-extras
```

## <span className="badge badge--info">cc-handbook-qa</span>

Browser automation and QA testing tools with Playwright MCP integration.

```bash
/plugin install cc-handbook-qa
```

## <span className="badge badge--success">cc-handbook-dotnet</span>

.NET development tools and automatic CSharpier formatting for C# files.

```bash
/plugin install cc-handbook-dotnet
```

## <span className="badge badge--warning">cc-handbook-context7</span>

Context7 MCP server for fetching latest library documentation from official sources.

```bash
/plugin install cc-handbook-context7
```

---

## Understanding Building Blocks

Plugins help you to bundle related customizations, commands, and agents into reusable packages. This modular approach allows you to easily share and install sets of tools tailored for specific workflows or problem domains.

Learn more: [Understanding Building Blocks](/fundamentals/understanding-building-blocks)

---

## Release History

See the [Changelog](/changelog) for detailed release notes and version history.

---

## Direct Installation from Source

To install directly from the GitHub repository:

```bash
# Clone the repository
git clone https://github.com/nikiforovall/claude-code-rules.git
cd claude-code-rules

# Install core plugin
/plugin install ./plugins/cc-handbook

# Install extras plugin
/plugin install ./plugins/cc-handbook-extras

# Install QA plugin
/plugin install ./plugins/cc-handbook-qa

# Install .NET plugin
/plugin install ./plugins/cc-handbook-dotnet

# Install Context7 plugin
/plugin install ./plugins/cc-handbook-context7
```

## Contributing

Want to contribute to cc-handbook-extras? Submit pull requests to the [GitHub repository](https://github.com/nikiforovall/claude-code-rules).

- Add new commands or agents
- Report issues
- Suggest improvements
