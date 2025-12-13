---
title: "🔌 Plugins"
sidebar_position: 3
---

# Plugins

Claude Code Handbook provides complementary plugins to enhance your AI-assisted development workflow.

```bash
# Add the marketplace
/plugin marketplace add nikiforovall/claude-code-rules
```

## [<span className="badge badge--handbook">handbook</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook/README.md)

Core plugin with essential tools and best practices for Claude Code development.


```bash
/plugin install handbook
```

## [<span className="badge badge--handbook-extras">handbook-extras</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-extras/README.md)

Extended features and experimental tools for advanced use cases.

```bash
/plugin install handbook-extras
```

## [<span className="badge badge--handbook-dotnet">handbook-dotnet</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-dotnet/README.md)

.NET development tools and automatic CSharpier formatting for C# files.

```bash
/plugin install handbook-dotnet
```

## [<span className="badge badge--handbook-sounds">handbook-sounds</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-sounds/README.md)

Audio feedback for Claude Code events on Windows using PowerShell sounds.

```bash
/plugin install handbook-sounds
```

## [<span className="badge badge--handbook-git-worktree">handbook-git-worktree</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-git-worktree/README.md)

Git worktree management for working on multiple branches simultaneously.

```bash
/plugin install handbook-git-worktree
```

## [<span className="badge badge--handbook-structured-plan-mode">handbook-structured-plan-mode</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-structured-plan-mode/README.md)

Structured planning methodology for complex feature implementations through systematic task decomposition.

```bash
/plugin install handbook-structured-plan-mode
```

## [<span className="badge badge--handbook-agent-spec-kit">handbook-agent-spec-kit</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-agent-spec-kit/README.md)

Spec-driven development workflow system with structured phases: Requirements → Design → Tasks → Implementation.

**Components:**
- **Skill:** [`spec-driven`](/component-reference/skills/spec-driven) - Orchestrator that coordinates the entire workflow with approval gates
- **Agents:**
  - [`requirements-agent`](/component-reference/agents/requirements-agent) - Creates requirements documents with EARS acceptance criteria
  - [`tech-design-agent`](/component-reference/agents/tech-design-agent) - Creates comprehensive technical design documents
  - [`tasks-agent`](/component-reference/agents/tasks-agent) - Converts designs into actionable coding tasks
  - [`implementation-agent`](/component-reference/agents/implementation-agent) - Executes tasks with strict zero-improvisation policy

```bash
/plugin install handbook-agent-spec-kit
```

## [<span className="badge badge--handbook-context7">handbook-context7</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-context7/README.md)

Context7 MCP server for fetching latest library documentation from official sources.

```bash
/plugin install handbook-context7
```

## [<span className="badge badge--handbook-qa">handbook-qa</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-qa/README.md)

Browser automation and QA testing tools with Playwright MCP integration.

```bash
/plugin install handbook-qa
```

## [<span className="badge badge--handbook-nano-banana">handbook-nano-banana</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-nano-banana/README.md)

Python scripting and Gemini image generation using uv with inline script dependencies.

```bash
/plugin install handbook-nano-banana
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
/plugin install ./plugins/handbook

# Install extras plugin
/plugin install ./plugins/handbook-extras

# Install QA plugin
/plugin install ./plugins/handbook-qa

# Install .NET plugin
/plugin install ./plugins/handbook-dotnet

# Install Context7 plugin
/plugin install ./plugins/handbook-context7

# Install sounds plugin
/plugin install ./plugins/handbook-sounds

# Install git-worktree plugin
/plugin install ./plugins/handbook-git-worktree

# Install structured-plan-mode plugin
/plugin install ./plugins/handbook-structured-plan-mode

# Install agent-spec-kit plugin
/plugin install ./plugins/handbook-agent-spec-kit

# Install nano-banana plugin
/plugin install ./plugins/handbook-nano-banana
```

## Contributing

Want to contribute to cc-handbook-extras? Submit pull requests to the [GitHub repository](https://github.com/nikiforovall/claude-code-rules).

- Add new commands or agents
- Report issues
- Suggest improvements
