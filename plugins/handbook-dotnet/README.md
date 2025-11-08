# Claude Code .NET Plugin

Automatic CSharpier formatting for C# files modified by Claude Code.

## Features

- **Automatic Formatting**: Automatically formats `.cs` files after Claude creates or edits them
- **Performance Optimized**: Uses `--skip-validation` for faster formatting
- **Compilation-Tolerant**: Uses `--compilation-errors-as-warnings` to format incomplete code
- **Non-Blocking**: Warnings are shown but don't interrupt Claude's workflow
- **Seamless Integration**: Works alongside existing hooks and tools

## Prerequisites

**CSharpier must be installed on your system.**

Install CSharpier globally:

```bash
dotnet tool install -g csharpier
```

Or locally in your project:

```bash
dotnet tool install csharpier
```

Verify installation:

```bash
dotnet csharpier --version
```

## Installation

Via marketplace (recommended):

```bash
/plugin marketplace add nikiforovall/claude-code-rules
/plugin install handbook-dotnet
```

Or directly from source:

```bash
/plugin install https://github.com/nikiforovall/claude-code-rules/tree/main/plugins/handbook-dotnet
```

## How It Works

This plugin uses a **PostToolUse hook** that triggers after Claude uses the `Write` or `Edit` tools:

1. **Detects C# files**: Only processes files with `.cs` extension
2. **Runs CSharpier**: Formats the file using `dotnet csharpier format`
3. **Reports status**: Shows warnings if formatting fails, but doesn't block Claude

### Hook Configuration

The hook is configured in `hooks/hooks.json`:

```json
{
  "description": "Automatic CSharpier formatting for C# files",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"${CLAUDE_PLUGIN_ROOT}/hooks/format-csharp.sh\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Configuration

### Custom CSharpier Config

If you have a `.csharpierrc` or `.csharpierrc.json` file in your project, CSharpier will automatically use it.

### Environment Variables

**CC_HANDBOOK_DOTNET_DISABLE_HOOKS**

Disable the automatic CSharpier formatting hook.

```bash
# Disable globally in your shell
export CC_HANDBOOK_DOTNET_DISABLE_HOOKS=true

# Or disable for a single Claude Code session
CC_HANDBOOK_DOTNET_DISABLE_HOOKS=true claude
```

This is useful when:
- You want to temporarily disable formatting
- You're working with generated code that shouldn't be formatted
- You're debugging formatting issues

## Contributing

Found a bug or have a suggestion? Please open an issue at:
https://github.com/nikiforovall/claude-code-rules/issues

## License

MIT License - see [LICENSE](../../LICENSE) for details
