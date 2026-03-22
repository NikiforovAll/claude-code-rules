# CLAUDE.md

This file provides guidance to Claude Code when working with the Claude Code Handbook monorepo.

## Repository Overview

This is a Claude Code plugin monorepo containing multiple distributable plugins and a marketplace. It provides practical techniques, tools, and extensions to enhance AI-assisted development workflows.

## Repo Structure

```
claude-code-rules/                    # Root monorepo
├── plugins/                          # All plugins (run discover script for full inventory)
│   └── <plugin-name>/
│       ├── .claude-plugin/plugin.json  # Manifest (name, version, description)
│       ├── skills/                     # Skills (SKILL.md per skill)
│       ├── agents/                     # Agent definitions (.md)
│       ├── commands/                   # Slash commands (.md)
│       ├── hooks/hooks.json            # Event hooks
│       ├── .mcp.json                   # MCP servers
│       └── .lsp.json                   # LSP servers
├── .claude-plugin/
│   └── marketplace.json              # Catalogs all plugins (marketplace: "cc-handbook")
├── website/                          # Docusaurus documentation site
├── BEST-PRACTICES.md
├── TIPS-AND-TRICKS.md
├── CHANGELOG.md
└── README.md
```

To list all plugins with components and install status:
```bash
python plugins/handbook-discover/skills/handbook-discover/scripts/discover.py --detailed
```

## Website

This repository includes a Docusaurus-based documentation site located in the `website/` folder. The site serves as the primary source of truth for the Claude Code Handbook content.

## IMPORTANT
**Do not modify:** `TIPS-AND-TRICKS.md` and `BEST-PRACTICES.md` (obsolete, website is source of truth)
