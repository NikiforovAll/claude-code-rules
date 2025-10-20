---
title: "🔌 Plugins"
sidebar_position: 3
---

# Plugins

Claude Code Handbook provides two complementary plugins to enhance your AI-assisted development workflow.

## <span className="badge badge--primary">cc-handbook</span>

Core plugin with essential tools and best practices for Claude Code development.

## <span className="badge badge--secondary">cc-handbook-extras</span>

Extended features and experimental tools for advanced use cases.

**Features:**
- Ready for community contributions
- Experimental functionality playground
- Compatible with cc-handbook

---

## Understanding Building Blocks

Plugins help you to bundle related customizations, commands, and agents into reusable packages. This modular approach allows you to easily share and install sets of tools tailored for specific workflows or problem domains.

Learn more: [Understanding Building Blocks](/tips-and-tricks/understanding-building-blocks)

---

## Installation

### Quick Install via CLI

Use Claude Code's `/plugin` command for the quickest installation:

```bash
# Add the marketplace (one-time setup)
/plugin marketplace add nikiforovall/claude-code-rules

# Install core plugin
/plugin install cc-handbook

# Install extras plugin
/plugin install cc-handbook-extras
```

### Direct Installation from Source

To install directly from the GitHub repository:

```bash
# Clone the repository
git clone https://github.com/nikiforovall/claude-code-rules.git
cd claude-code-rules

# Install core plugin
/plugin install ./plugins/cc-handbook

# Install extras plugin
/plugin install ./plugins/cc-handbook-extras
```

## Contributing

Want to contribute to cc-handbook-extras? Submit pull requests to the [GitHub repository](https://github.com/nikiforovall/claude-code-rules).

- Add new commands or agents
- Report issues
- Suggest improvements
