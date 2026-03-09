# Interactive HTML Diagrammer

Generate interactive HTML diagrams from .NET assemblies using ILSpy's built-in Mermaid-based diagrammer.

## Prerequisites

The diagrammer requires all assembly dependencies to be resolvable. Use published output with `-r` to provide them.

## Workflow

### 1. Publish the project to collect all dependencies

```bash
dotnet publish path/to/Project.csproj -o /tmp/ilspy-publish -p:WarningLevel=0 /clp:ErrorsOnly --verbosity minimal
```

### 2. Generate the diagrammer

```bash
ilspycmd /tmp/ilspy-publish/MyAssembly.dll \
  --generate-diagrammer \
  -o /tmp/ilspy-diagrams \
  -r /tmp/ilspy-publish/
```

### 3. Open in browser

```bash
# Windows
start /tmp/ilspy-diagrams/index.html

# macOS
open /tmp/ilspy-diagrams/index.html

# Linux
xdg-open /tmp/ilspy-diagrams/index.html
```

## Filtering types

Use regex patterns to include or exclude types:

```bash
# Only types in a specific namespace
ilspycmd MyAssembly.dll --generate-diagrammer -o ./diagrams \
  -r /tmp/ilspy-publish/ \
  --generate-diagrammer-include "MyNamespace\\..+"

# Exclude specific sub-namespace
ilspycmd MyAssembly.dll --generate-diagrammer -o ./diagrams \
  -r /tmp/ilspy-publish/ \
  --generate-diagrammer-include "MyNamespace\\..+" \
  --generate-diagrammer-exclude "MyNamespace\\.Internal\\..+"

# Debug your filters — report excluded types
ilspycmd MyAssembly.dll --generate-diagrammer -o ./diagrams \
  -r /tmp/ilspy-publish/ \
  --generate-diagrammer-report-excluded
```

## Adding XML documentation

If the assembly has XML docs, annotate diagrams with them:

```bash
ilspycmd MyAssembly.dll --generate-diagrammer -o ./diagrams \
  -r /tmp/ilspy-publish/ \
  --generate-diagrammer-docs /tmp/ilspy-publish/MyAssembly.xml
```

## Important

- Always use `-r <publish-dir>` — the diagrammer fails if it cannot resolve transitive dependencies
- Published output (`dotnet publish`) guarantees all deps are present in one folder
- Build output (`bin/Debug/`) typically lacks NuGet dependencies and will fail
