---
title: "🔌 Plugins"
sidebar_position: 3
---

# Plugins

Claude Code Handbook provides two complementary plugins to enhance your AI-assisted development workflow.

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

## <span className="badge badge--success">cc-handbook-dotnet</span>

.NET development tools and automatic CSharpier formatting for C# files.

```bash
/plugin install cc-handbook-dotnet
```

---

## Understanding Building Blocks

Plugins help you to bundle related customizations, commands, and agents into reusable packages. This modular approach allows you to easily share and install sets of tools tailored for specific workflows or problem domains.

Learn more: [Understanding Building Blocks](/tips-and-tricks/understanding-building-blocks)

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

# Install .NET plugin
/plugin install ./plugins/cc-handbook-dotnet
```

## Contributing

Want to contribute to cc-handbook-extras? Submit pull requests to the [GitHub repository](https://github.com/nikiforovall/claude-code-rules).

- Add new commands or agents
- Report issues
- Suggest improvements
