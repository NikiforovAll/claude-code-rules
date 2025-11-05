# Claude Code Handbook QA Plugin

Browser automation and QA testing tools for Claude Code Handbook.

This plugin provides Playwright MCP integration for browser automation, end-to-end testing, and quality assurance workflows.

## Features

### MCP Servers

- **Playwright** - Browser automation with Chromium, Firefox, and WebKit support
  - Navigate and interact with web pages
  - Take screenshots and capture accessibility snapshots
  - Fill forms and validate UI behavior
  - Monitor network requests and console logs

## Plugin Structure

```
cc-handbook-qa/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest
└── .mcp.json             # Playwright MCP configuration
```

## Installation

```bash
claude plugins install https://github.com/nikiforovall/claude-code-rules/tree/main/plugins/cc-handbook-qa
```

## Usage

Once installed, Playwright browser automation tools are available through MCP:

- `browser_navigate` - Navigate to URLs
- `browser_snapshot` - Capture accessibility snapshots
- `browser_click` - Interact with page elements
- `browser_fill_form` - Fill out web forms
- And many more...

See the [Playwright MCP documentation](https://nikiforovall.blog/claude-code-rules/component-reference/mcp-servers/playwright) for complete usage details.

## License

MIT
