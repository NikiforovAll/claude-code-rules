# CLAUDE.md

This file provides guidance to Claude Code when working with the Claude Code Handbook monorepo.

## Repository Overview

This is a Claude Code plugin monorepo containing multiple distributable plugins and a marketplace. It provides practical techniques, tools, and extensions to enhance AI-assisted development workflows.

## Repo Structure

```
claude-code-rules/                    # Root monorepo
│
├── plugins/                          # Plugin directory
│   ├── cc-handbook/                  # Core plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json          # Name: "cc-handbook"
│   │   ├── commands/                 # 5 slash commands
│   │   ├── agents/                   # 2 specialized agents
│   │   ├── hooks/
│   │   ├── .mcp.json                 # 4 MCP servers
│   │   ├── BEST-PRACTICES.md
│   │   ├── TIPS-AND-TRICKS.md
│   │   └── README.md
│   │
│   └── cc-handbook-extras/           # Extras plugin (empty shell)
│       ├── .claude-plugin/
│       │   └── plugin.json          # Name: "cc-handbook-extras"
│       ├── commands/                 # Ready for contributions
│       ├── agents/
│       ├── hooks/
│       └── README.md
│
├── marketplace/                      # Marketplace configuration
│   └── marketplace.json              # Catalogs both plugins
│
├── website/                          # Docusaurus documentation site
│   ├── docs/                         # Source documentation
│   └── docusaurus.config.js          # Site configuration
│
├── BEST-PRACTICES.md                 # Shared documentation
├── TIPS-AND-TRICKS.md
├── CHANGELOG.md
└── README.md
```

## Website

**Location:** `website/`

Docusaurus-based documentation site deployed at [nikiforovall.blog/claude-code-rules](https://nikiforovall.blog/claude-code-rules)

- Source docs in `website/docs/`
- Configuration in `website/docusaurus.config.js`
- Build and deploy via standard Docusaurus commands

## IMPORTANT

**Do not modify:** `TIPS-AND-TRICKS.md` and `BEST-PRACTICES.md` (obsolete, website is source of truth)
