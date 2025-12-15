# Handbook Microsoft Docs

Microsoft Learn MCP server for searching and fetching official Microsoft and Azure documentation.

## Features

- Search official Microsoft Learn documentation
- Fetch complete documentation pages
- Access Microsoft and Azure code samples
- Integrated with Claude Code for seamless documentation lookup

## Installation

```bash
/plugin marketplace add nikiforovall/claude-code-rules
/plugin install handbook-microsoft-docs
```

## Usage

Once installed, you'll have access to the Microsoft Docs MCP server which provides three main tools:

### 1. Search Documentation
Get quick overviews of Microsoft and Azure topics with concise content chunks.

### 2. Code Sample Search
Find official code examples and practical implementations for Microsoft/Azure products.

### 3. Fetch Full Pages
Retrieve complete documentation pages for detailed tutorials, troubleshooting, and guides.

## Available Resources

The MCP server provides structured access to:
- Microsoft Learn articles
- Azure documentation
- .NET framework docs
- C# language reference
- Visual Studio guides
- Azure service documentation

## Configuration

The plugin uses the Microsoft Learn API endpoint: `https://learn.microsoft.com/api/mcp`

## Requirements

- Claude Code with MCP support
- Internet connection for accessing Microsoft Learn
