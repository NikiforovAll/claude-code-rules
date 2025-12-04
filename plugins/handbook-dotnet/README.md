# Handbook .NET

.NET development tools including automatic CSharpier formatting for C# files and dotnet run file support.

## Features

- Automatic CSharpier formatting for `.cs` files after Claude edits them
- Performance optimized with `--skip-validation`
- Non-blocking warnings
- Uses `.csharpierrc` config if present
- **dotnet-run-file skill**: Run C# files directly without projects (.NET 10+)

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

## Skills

### dotnet-run-file

Run C# code directly without creating project files using .NET 10's `dotnet run file.cs` feature.

**Invoke the skill:**
```
Use the dotnet-run-file skill to help me run this C# code
```

**Quick examples:**

```bash
# Run a .cs file
dotnet run app.cs

# One-liner via stdin (Claude Code friendly)
echo 'Console.WriteLine("Hello");' | dotnet run -

# Multi-line with heredoc
dotnet run - << 'EOF'
var now = DateTime.Now;
Console.WriteLine($"Time: {now}");
EOF

# With NuGet package
dotnet run - << 'EOF'
#:package Humanizer@*
using Humanizer;
Console.WriteLine(TimeSpan.FromMinutes(90).Humanize());
EOF
```

**Directives:**
- `#:package Humanizer@*` - Add NuGet packages (version required)
- `#:sdk Microsoft.NET.Sdk.Web` - Set SDK (for web apps)
- `#:property LangVersion preview` - MSBuild properties


See `skills/dotnet-run-file/references/` for detailed guides.
