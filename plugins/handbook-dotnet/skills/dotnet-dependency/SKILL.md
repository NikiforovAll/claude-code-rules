---
name: dotnet-dependency
description: This skill should be used when investigating .NET project dependencies, understanding why packages are included, listing references, or auditing for outdated/vulnerable packages.
allowed-tools: Bash(dotnet nuget why:*), Bash(dotnet list:*), Bash(dotnet outdated:*), Read, Grep, Glob
---

# .NET Dependencies

Investigate and manage .NET project dependencies using built-in dotnet CLI commands.

## When to Use This Skill

Invoke when the user needs to:

- Understand why a specific NuGet package is included
- List all project dependencies (NuGet packages or project references)
- Find outdated or vulnerable packages
- Trace transitive dependencies

## Quick Reference

| Command                                     | Purpose                               |
| ------------------------------------------- | ------------------------------------- |
| `dotnet nuget why <package>`                | Show dependency graph for a package   |
| `dotnet list package`                       | List NuGet packages                   |
| `dotnet list package --include-transitive`  | Include transitive dependencies       |
| `dotnet list reference --project <project>` | List project-to-project references    |
| `dotnet list package --outdated`            | Find packages with newer versions     |
| `dotnet list package --vulnerable`          | Find packages with security issues    |
| `dotnet outdated`                           | (Third-party) Check outdated packages |
| `dotnet outdated -u`                        | (Third-party) Auto-update packages    |

## Investigate Package Dependencies

To understand why a package is included in your project:

```bash
# Why is this package included?
dotnet nuget why Newtonsoft.Json

# For a specific project
dotnet nuget why path/to/Project.csproj Newtonsoft.Json

# For a specific framework
dotnet nuget why Newtonsoft.Json --framework net8.0
```

Output shows the complete dependency chain from your project to the package.

## List NuGet Packages

```bash
# Direct dependencies only
dotnet list package

# Include transitive (indirect) dependencies
dotnet list package --include-transitive

# For a specific project
dotnet list package --project path/to/Project.csproj

# JSON output for scripting
dotnet list package --format json
```

## List Project References

```bash
# List project-to-project references
dotnet list reference --project path/to/Project.csproj
```

### Transitive Project References

No built-in command shows transitive project dependencies. To find if Project A depends on Project B transitively:

1. **Recursive approach**: Run `dotnet list reference` on each referenced project
2. **Parse .csproj files**: Search for `<ProjectReference>` elements recursively:

```bash
# Find all ProjectReference elements
grep -r "ProjectReference" --include="*.csproj" .
```

## Update Dependencies

### Using dotnet outdated (Third-party)

If installed (`dotnet tool install -g dotnet-outdated-tool`):

```bash
# Check for outdated packages
dotnet outdated

# Auto-update to latest versions
dotnet outdated -u

# Update only specific packages
dotnet outdated -u -inc PackageName
```

### Using built-in commands

```bash
# Check for outdated packages
dotnet list package --outdated

# Include prerelease versions
dotnet list package --outdated --include-prerelease
```

## Progressive Disclosure

For security auditing (vulnerable, deprecated, outdated packages), load **references/security-audit.md**.

## References

- [dotnet nuget why](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-nuget-why)
- [dotnet list reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-reference-list)
- [dotnet list package](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-list-package)
