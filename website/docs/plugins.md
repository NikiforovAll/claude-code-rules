---
title: "🔌 Plugins"
sidebar_position: 3
---

# Plugins

Claude Code Handbook provides complementary plugins to enhance your AI-assisted development workflow.

```bash
# Add the marketplace
claude plugin marketplace add nikiforovall/claude-code-rules
```

## [<span className="badge badge--handbook-discover">handbook-discover</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-discover/README.md)

Discover and audit all plugins in a Claude Code marketplace. Shows installation status, versions, and component breakdown (skills, agents, commands, MCP/LSP servers, hooks).

```bash
claude plugin install handbook-discover@cc-handbook
```

:::tip
Once installed, use `/handbook-discover` or ask Claude to "discover plugins" to get a live inventory of all marketplace plugins — including ones you haven't installed yet.
:::

## [<span className="badge badge--handbook">handbook</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook/README.md)

Core plugin with essential tools and best practices for Claude Code development.


```bash
claude plugin install handbook@cc-handbook
```

## [<span className="badge badge--handbook-extras">handbook-extras</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-extras/README.md)

Extended features and experimental tools for advanced use cases.

```bash
claude plugin install handbook-extras@cc-handbook
```

## [<span className="badge badge--handbook-dotnet">handbook-dotnet</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-dotnet/README.md)

.NET development tools and automatic CSharpier formatting for C# files.

```bash
claude plugin install handbook-dotnet@cc-handbook
```

## [<span className="badge badge--handbook-microsoft-docs">handbook-microsoft-docs</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-microsoft-docs/README.md)

Microsoft Learn MCP server for searching and fetching official Microsoft and Azure documentation.

```bash
claude plugin install handbook-microsoft-docs@cc-handbook
```

## [<span className="badge badge--handbook-sounds">handbook-sounds</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-sounds/README.md)

Audio feedback for Claude Code events on Windows using PowerShell sounds.

```bash
claude plugin install handbook-sounds@cc-handbook
```

## [<span className="badge badge--handbook-git-worktree">handbook-git-worktree</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-git-worktree/README.md)

Git worktree management for working on multiple branches simultaneously.

```bash
claude plugin install handbook-git-worktree@cc-handbook
```

## [<span className="badge badge--handbook-structured-plan-mode">handbook-structured-plan-mode</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-structured-plan-mode/README.md)

Structured planning methodology for complex feature implementations through systematic task decomposition.

```bash
claude plugin install handbook-structured-plan-mode@cc-handbook
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
claude plugin install handbook-agent-spec-kit@cc-handbook
```

## [<span className="badge badge--handbook-context7">handbook-context7</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-context7/README.md)

Context7 MCP server for fetching latest library documentation from official sources.

```bash
claude plugin install handbook-context7@cc-handbook
```

## [<span className="badge badge--handbook-qa">handbook-qa</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-qa/README.md)

Browser automation and QA testing tools with Playwright MCP integration.

```bash
claude plugin install handbook-qa@cc-handbook
```

## [<span className="badge badge--handbook-nano-banana">handbook-nano-banana</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-nano-banana/README.md)

Python scripting and Gemini image generation using uv with inline script dependencies.

```bash
claude plugin install handbook-nano-banana@cc-handbook
```

## [<span className="badge badge--handbook-glab">handbook-glab</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-glab/README.md)

GitLab CLI (glab) expertise for managing merge requests, issues, CI/CD pipelines, and repositories.

```bash
claude plugin install handbook-glab@cc-handbook
```

## [<span className="badge badge--handbook-csharp-lsp">handbook-csharp-lsp</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-csharp-lsp/README.md)

C# Language Server Protocol support using csharp-ls for code intelligence features.

```bash
claude plugin install handbook-csharp-lsp@cc-handbook
```

## [<span className="badge badge--handbook-elasticsearch">handbook-elasticsearch</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-elasticsearch/README.md)

Elasticsearch and Kibana REST API expertise for querying, indexing, managing indices, cluster health, aggregations, ES|QL, and dashboard deployment.

```bash
claude plugin install handbook-elasticsearch@cc-handbook
```

## [<span className="badge badge--handbook-code-review">handbook-code-review</span>](https://github.com/nikiforovall/claude-code-rules/blob/main/plugins/handbook-code-review/README.md)

Code review plugin with two review strategies: disposable subagents for one-shot reviews and persistent team members for iterative reviews.

**Components:**
- **Skill:** `subagent-review` - One-shot review using three parallel disposable subagents (reuse, quality, efficiency)
- **Skill:** `team-review` - Review using three persistent named team members for follow-up questions

```bash
claude plugin install handbook-code-review@cc-handbook
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
claude plugin install ./plugins/handbook

# Install extras plugin
claude plugin install ./plugins/handbook-extras

# Install QA plugin
claude plugin install ./plugins/handbook-qa

# Install .NET plugin
claude plugin install ./plugins/handbook-dotnet

# Install Microsoft Docs plugin
claude plugin install ./plugins/handbook-microsoft-docs

# Install Context7 plugin
claude plugin install ./plugins/handbook-context7

# Install sounds plugin
claude plugin install ./plugins/handbook-sounds

# Install git-worktree plugin
claude plugin install ./plugins/handbook-git-worktree

# Install structured-plan-mode plugin
claude plugin install ./plugins/handbook-structured-plan-mode

# Install agent-spec-kit plugin
claude plugin install ./plugins/handbook-agent-spec-kit

# Install nano-banana plugin
claude plugin install ./plugins/handbook-nano-banana

# Install glab plugin
claude plugin install ./plugins/handbook-glab

# Install elasticsearch plugin
claude plugin install ./plugins/handbook-elasticsearch

# Install code-review plugin
claude plugin install ./plugins/handbook-code-review

# Install csharp-lsp plugin
claude plugin install ./plugins/handbook-csharp-lsp

# Install discover plugin
claude plugin install ./plugins/handbook-discover
```

## Contributing

Want to contribute to cc-handbook-extras? Submit pull requests to the [GitHub repository](https://github.com/nikiforovall/claude-code-rules).

- Add new commands or agents
- Report issues
- Suggest improvements
