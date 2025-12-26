# Handbook CSharp LSP

C# Language Server Protocol support using csharp-ls for code intelligence features.

## Features

- Go to definition
- Find references
- Hover information
- Document symbols
- Workspace symbols
- Call hierarchy

## Prerequisites

- .NET 10 SDK or later
- csharp-ls installed globally:

```bash
dotnet tool install --global csharp-ls
```

## Installation

```bash
/plugin marketplace add nikiforovall/claude-code-rules
/plugin install handbook-csharp-lsp
```

## Usage

Once installed, the LSP tool will automatically provide C# code intelligence for `.cs` files.

```
# Example LSP operations
goToDefinition, findReferences, hover, documentSymbol, workspaceSymbol
```
