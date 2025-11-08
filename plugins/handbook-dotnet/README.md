# Handbook .NET

.NET development tools including automatic CSharpier formatting for C# files.

## Features

- Automatic CSharpier formatting for `.cs` files after Claude edits them
- Performance optimized with `--skip-validation`
- Non-blocking warnings
- Uses `.csharpierrc` config if present

## Prerequisites

Install CSharpier:

```bash
dotnet tool install -g csharpier
```

## Installation

```bash
/plugin marketplace add nikiforovall/claude-code-rules
/plugin install handbook-dotnet
```

## Configuration

**Disable formatting:**
```bash
export CC_HANDBOOK_DOTNET_DISABLE_HOOKS=true
```

**Custom config:**
Place `.csharpierrc` or `.csharpierrc.json` in your project root.
