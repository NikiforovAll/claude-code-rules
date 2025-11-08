# CLAUDE.md

This file provides guidance to Claude Code when working with the Claude Code Handbook monorepo.

## Repository Overview

This is a Claude Code plugin monorepo containing multiple distributable plugins and a marketplace. It provides practical techniques, tools, and extensions to enhance AI-assisted development workflows.

## Repo Structure

```
claude-code-rules/                    # Root monorepo
│
├── plugins/                          # Plugin directory
│   ├── handbook/                     # Core plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json          # Name: "handbook"
│   │   ├── commands/                 # 5 slash commands
│   │   ├── agents/                   # 2 specialized agents
│   │   ├── hooks/
│   │   ├── BEST-PRACTICES.md
│   │   ├── TIPS-AND-TRICKS.md
│   │   └── README.md
│   │
│   ├── handbook-extras/              # Extras plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json          # Name: "handbook-extras"
│   │   ├── commands/                 # Ready for contributions
│   │   ├── agents/
│   │   ├── hooks/
│   │   └── README.md
│   │
│   ├── handbook-qa/                  # QA and browser automation plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json          # Name: "handbook-qa"
│   │   ├── .mcp.json                 # Playwright MCP server
│   │   └── README.md
│   │
│   ├── handbook-dotnet/              # .NET development plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json          # Name: "handbook-dotnet"
│   │   ├── .mcp.json                 # Microsoft Docs MCP server
│   │   ├── hooks/
│   │   └── README.md
│   │
│   ├── handbook-context7/            # Context7 documentation plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json          # Name: "handbook-context7"
│   │   ├── .mcp.json                 # Context7 MCP server
│   │   └── README.md
│   │
│   └── handbook-sounds/              # Audio feedback plugin
│       ├── .claude-plugin/
│       │   └── plugin.json          # Name: "handbook-sounds"
│       ├── hooks/
│       └── README.md
│
├── .claude-plugin/                   # Marketplace configuration
│   └── marketplace.json              # Catalogs all plugins (Marketplace name: "cc-handbook")
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

This repository includes a Docusaurus-based documentation site located in the `website/` folder. The site serves as the primary source of truth for the Claude Code Handbook content.

## IMPORTANT
**Do not modify:** `TIPS-AND-TRICKS.md` and `BEST-PRACTICES.md` (obsolete, website is source of truth)
