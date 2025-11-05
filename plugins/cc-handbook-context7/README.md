# Claude Code Handbook Context7 Plugin

Fetch latest library documentation directly from official sources for Claude Code Handbook.

This plugin provides the Context7 MCP server to prevent outdated API usage and hallucinated functions by accessing real-time library documentation.

## Features

### MCP Servers

- **Context7** - Real-time library documentation access
  - Fetch latest API documentation from official sources
  - Support for popular libraries and frameworks
  - Prevent outdated API references
  - Reduce hallucinations with authoritative documentation

## Plugin Structure

```
cc-handbook-context7/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest
└── .mcp.json             # Context7 MCP configuration
```

## Installation

```bash
claude plugins install https://github.com/nikiforovall/claude-code-rules/tree/main/plugins/cc-handbook-context7
```

Or via marketplace:

```bash
/plugin marketplace add nikiforovall/claude-code-rules
/plugin install cc-handbook-context7
```

## Usage

Once installed, Context7 is automatically available through MCP. Simply mention the library name in your prompts:

```
"Use context7 to help me with React hooks"
"Fetch the latest TypeScript documentation for generics"
"Show me the current Next.js API for server components"
```

See the [Context7 MCP documentation](https://nikiforovall.blog/claude-code-rules/component-reference/mcp-servers/context7) for complete usage details.

## Migration Note

If you previously used Context7 through the `cc-handbook` plugin, you now need to install this dedicated plugin. Context7 has been moved to its own plugin for better modularity.

## License

MIT
