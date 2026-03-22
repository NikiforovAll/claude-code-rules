---
name: handbook-discover
description: This skill should be used when users want to discover, browse, or audit cc-handbook marketplace plugins. Shows all available plugins with installation status, versions, and component breakdown (skills, agents, commands, MCP/LSP servers, hooks). Trigger phrases include "discover plugins", "list handbook plugins", "what plugins are available", "browse marketplace".
---

# Handbook Plugin Discovery

Run the discovery script to inventory all plugins in a Claude Code marketplace.

## Usage

```bash
python ${CLAUDE_SKILL_DIR}/scripts/discover.py                    # default: cc-handbook
python ${CLAUDE_SKILL_DIR}/scripts/discover.py --detailed         # show component names
python ${CLAUDE_SKILL_DIR}/scripts/discover.py --json             # machine-readable
python ${CLAUDE_SKILL_DIR}/scripts/discover.py --filter dotnet    # filter by keyword
python ${CLAUDE_SKILL_DIR}/scripts/discover.py --uninstalled      # only uninstalled
python ${CLAUDE_SKILL_DIR}/scripts/discover.py -m <marketplace>   # other marketplace
python ${CLAUDE_SKILL_DIR}/scripts/discover.py -r <path>          # explicit repo path
```

## Interpreting Results

- `[+]` — installed and enabled
- `[o]` — installed but disabled
- `[ ]` — not installed
- Component counts: `S`=skills `A`=agents `C`=commands `M`=mcp `L`=lsp `H`=hooks

## Follow-up Actions

For uninstalled plugins, suggest:
```bash
claude plugin install <plugin-name>@cc-handbook
```
