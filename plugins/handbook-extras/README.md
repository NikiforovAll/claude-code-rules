# Claude Code Handbook Extras Plugin

Extended features and experimental tools for Claude Code Handbook.

This is a companion plugin to `handbook` providing additional, experimental, or domain-specific features.

## Current Status

This plugin is in its initial release and ready for community contributions.

## Contributing

To add new features to this extras plugin:

1. Create a new command or agent in the appropriate directory (`commands/`, `agents/`, etc.)
2. Update the plugin version in `.claude-plugin/plugin.json`
3. Test the plugin locally: `claude plugins install .`
4. Submit a pull request with your changes

## Plugin Structure

```
handbook-extras/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest
├── commands/             # Custom slash commands
├── agents/               # Specialized agents
├── hooks/                # Event handlers
└── .mcp.json (optional) # MCP server configurations
```

## Installation

Via marketplace (recommended):

```bash
/plugin marketplace add nikiforovall/claude-code-rules
/plugin install handbook-extras
```

Or directly from source:

```bash
/plugin install https://github.com/nikiforovall/claude-code-rules/tree/main/plugins/handbook-extras
```

## License

MIT
