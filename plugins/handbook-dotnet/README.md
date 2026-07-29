# Handbook .NET

.NET development tools including automatic CSharpier formatting for C# files and dotnet run file support.

## Features

- Automatic CSharpier formatting for `.cs` files after Claude edits them
- Performance optimized with `--skip-validation`
- Non-blocking warnings
- Uses `.csharpierrc` config if present
- **dotnet-run-file skill**: Run C# files directly without projects (.NET 10+)
- **coverage-report skill**: Generate code coverage reports scoped to branch changes
- **dotnet-inspect skill**: Query .NET APIs across NuGet packages, platform libraries, and local assemblies
- **dotnet-analyzers skill**: Fix code style and analyzer diagnostics with `dotnet format`, plus an HTML dashboard
- **roslyn-query skill**: Query C# codebases structurally via Roslyn AST analysis

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

### dotnet-inspect

Query .NET library APIs — the same commands work across NuGet packages, platform libraries, and local `.dll`/`.nupkg` files.

**Quick examples:**

```bash
# Scan a type's members
dnx dotnet-inspect -y -- member JsonSerializer --package System.Text.Json --oneline

# Triage what changed between two versions
dnx dotnet-inspect -y -- diff --package System.CommandLine@2.0.0-beta4.22272.1..2.0.3 --oneline

# Find extension methods for a type
dnx dotnet-inspect -y -- extensions IServiceCollection --extensions
```

Generic types need quotes and a type parameter: `'Option<T>'`. Use the built-in `-n N` / `-s Section` limits instead of piping through `head`.

### dotnet-analyzers

Fix code style and analyzer diagnostics (IDE\*, CA\*, SA\*) with `dotnet format`. Always reports first — never fixes without confirmation.

**Quick examples:**

```bash
# List violations without fixing
dotnet format style --verify-no-changes --severity warn -v diag

# Fix a specific diagnostic
dotnet format style --diagnostics IDE0005 --severity warn

# CI gate
dotnet format --verify-no-changes --severity warn
```

Pass `--dashboard` for an interactive HTML report, or `--dashboard --sarif` for comprehensive SARIF-based coverage that respects `.editorconfig` severity.

### roslyn-query

Query C# codebases structurally using Roslyn AST analysis, run as throwaway scripts via `dotnet run file.cs`. Answers questions grep can't: who calls this method, what implements this interface, where does untrusted data flow.

Two tiers — syntax-only (fast, no compilation) for assignment audits and pattern checks, semantic (`MSBuildWorkspace`) for callers, implementations, and data flow.

```bash
dotnet run scripts/my-analysis.cs -- <target-path>
```

See `skills/roslyn-query/references/` for the API reference and script templates.
