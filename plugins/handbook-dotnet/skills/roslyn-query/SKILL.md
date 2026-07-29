---
name: roslyn-query
description: Query .NET/C# codebases using Roslyn AST analysis via dotnet run file. Use for tracing data flow, auditing API usage, finding pattern violations, or ad-hoc codebase queries.
argument-hint: "[analysis description or query type]"
---

# Roslyn Query

Query .NET/C# codebases using Roslyn AST analysis scripts executed via `dotnet run file.cs`.

Before generating scripts, load the `handbook-dotnet:dotnet-run-file` skill for execution conventions and directive syntax.

## When to Use

- Trace data flow from sources to sinks (taint analysis)
- Audit all assignments to specific properties
- Find all callers of a method
- Find all implementations of an interface
- Detect pattern violations (empty catches, missing sanitizers, etc.)
- Architecture validation (layer violations)
- Ad-hoc codebase structural queries

## Analysis Tiers

### Tier 1: Syntax-Only (fast, no compilation)

Uses `CSharpSyntaxTree.ParseText()` — parses files individually, no solution loading.

Best for:
- Property assignment audits (`x.Content = ...`)
- Empty catch block detection
- Naming convention checks
- Cyclomatic complexity
- Magic number/string detection
- Method size metrics
- Pattern matching on code structure

### Tier 2: Semantic (needs project/solution)

Uses `MSBuildWorkspace` — loads project, resolves types, enables cross-file analysis.

Best for:
- Find all callers of a method (`SymbolFinder.FindCallersAsync`)
- Find interface implementations (`SymbolFinder.FindImplementationsAsync`)
- Find method overrides (`SymbolFinder.FindOverridesAsync`)
- Type dependency graphs
- Full data flow analysis (`SemanticModel.AnalyzeDataFlow`)

## Instructions

### Step 1: Determine analysis type

Based on the user's request, choose the appropriate template from `references/templates.md`. If no template fits, compose a custom script using the patterns documented there.

### Step 2: Generate the script

Create a `.cs` file in a `scripts/` directory (or temp location) using `dotnet run file.cs` format with `#:package` directives.

For syntax-only analysis:
```csharp
#:package Microsoft.CodeAnalysis.CSharp@4.*
```

For semantic analysis, additionally:
```csharp
#:package Microsoft.CodeAnalysis.CSharp.Workspaces@4.*
#:package Microsoft.CodeAnalysis.Workspaces.MSBuild@4.*
#:package Microsoft.Build.Locator@1.*
#:property DisableMSBuildAssemblyCopyCheck=true
```

> **Note:** `DisableMSBuildAssemblyCopyCheck=true` suppresses the MSBL001 build error that requires `ExcludeAssets="runtime"` on MSBuild packages — an attribute `#:package` directives can't express. Safe for throwaway analysis scripts.
>
> **`.slnx` not supported:** Roslyn 4.x `MSBuildWorkspace` only supports `.sln`, not `.slnx`. Use `OpenProjectAsync` with a `.csproj` instead — transitive project references are loaded automatically.

### Step 3: Script conventions

- Accept target directory/path via `args[0]`, default to `Directory.GetCurrentDirectory()`
- Use `Path.GetRelativePath()` for output paths
- Print structured output: file:line, description, context
- Use color: green for safe, yellow for warnings, red for violations
- Exit code 0 = clean, 1 = findings

### Step 4: Execute

```bash
dotnet run scripts/my-analysis.cs -- <target-path>
```

### Step 5: Interpret results

Analyze the output. For taint analysis, categorize findings:
- **Safe** — trusted source (code-generated, AI output, literal null)
- **Already sanitized** — sanitizer call deeper in call chain (syntax-only false positive)
- **Needs investigation** — external input, user-authored content
- **Violation** — clear miss that should be fixed

## Key Roslyn APIs Quick Reference

Load `references/roslyn-api.md` for detailed API reference with code examples.

## Templates

Load `references/templates.md` for ready-to-use analysis script templates.
