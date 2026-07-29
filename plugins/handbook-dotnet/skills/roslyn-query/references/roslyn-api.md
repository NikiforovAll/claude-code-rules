# Roslyn API Quick Reference

## Syntax-Only APIs

No compilation needed. Parse individual files with `CSharpSyntaxTree.ParseText()`.

### Core Types

```csharp
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
```

### Parse and Walk

```csharp
var tree = CSharpSyntaxTree.ParseText(File.ReadAllText(filePath), path: filePath);
var root = tree.GetRoot();

// Find specific node types
var assignments = root.DescendantNodes().OfType<AssignmentExpressionSyntax>();
var invocations = root.DescendantNodes().OfType<InvocationExpressionSyntax>();
var catches = root.DescendantNodes().OfType<CatchClauseSyntax>();
var methods = root.DescendantNodes().OfType<MethodDeclarationSyntax>();
var classes = root.DescendantNodes().OfType<ClassDeclarationSyntax>();
var properties = root.DescendantNodes().OfType<PropertyDeclarationSyntax>();
```

### Get Location Info

```csharp
var lineSpan = node.GetLocation().GetLineSpan();
var line = lineSpan.StartLinePosition.Line + 1;
var file = lineSpan.Path;
```

### Check Assignment Target

```csharp
if (assignment.Left is MemberAccessExpressionSyntax memberAccess)
{
    var propName = memberAccess.Name.Identifier.Text;
    var objectName = memberAccess.Expression.ToString();
}
```

### Check Invocation Name

```csharp
if (invocation.Expression is MemberAccessExpressionSyntax ma)
{
    var methodName = ma.Name.Identifier.Text;
    var receiver = ma.Expression.ToString();
}
if (invocation.Expression is IdentifierNameSyntax id)
{
    var methodName = id.Identifier.Text;
}
```

### Walk RHS for Specific Calls

```csharp
static bool ContainsCall(SyntaxNode node, string methodName)
{
    return node.DescendantNodesAndSelf()
        .OfType<InvocationExpressionSyntax>()
        .Any(inv => inv.Expression switch
        {
            MemberAccessExpressionSyntax ma => ma.Name.Identifier.Text == methodName,
            IdentifierNameSyntax id => id.Identifier.Text == methodName,
            _ => false
        });
}
```

### Common Syntax Node Types

| Node Type | Matches |
|-----------|---------|
| `ClassDeclarationSyntax` | `class Foo { }` |
| `InterfaceDeclarationSyntax` | `interface IFoo { }` |
| `MethodDeclarationSyntax` | `void Foo() { }` |
| `PropertyDeclarationSyntax` | `int Foo { get; set; }` |
| `AssignmentExpressionSyntax` | `x = y`, `x += y` |
| `InvocationExpressionSyntax` | `Foo()`, `x.Foo()` |
| `ObjectCreationExpressionSyntax` | `new Foo()` |
| `CatchClauseSyntax` | `catch (Exception) { }` |
| `ThrowStatementSyntax` | `throw new ...;` |
| `ReturnStatementSyntax` | `return x;` |
| `IfStatementSyntax` | `if (...) { }` |
| `ForEachStatementSyntax` | `foreach (var x in y) { }` |
| `LiteralExpressionSyntax` | `42`, `"hello"`, `true` |
| `BaseListSyntax` | `: IFoo, Bar` |
| `UsingDirectiveSyntax` | `using System;` |
| `AttributeSyntax` | `[Fact]`, `[HttpGet]` |

### SyntaxWalker Pattern

For complex analysis, subclass `CSharpSyntaxWalker`:

```csharp
class MyWalker : CSharpSyntaxWalker
{
    public List<(string File, int Line, string Message)> Findings = [];

    public override void VisitAssignmentExpression(AssignmentExpressionSyntax node)
    {
        // analyze node
        base.VisitAssignmentExpression(node);
    }
}

var walker = new MyWalker();
walker.Visit(root);
```

## Semantic APIs (MSBuildWorkspace)

Requires project/solution loading. Slower but enables cross-file type resolution.

### Setup

```csharp
#:package Microsoft.CodeAnalysis.CSharp.Workspaces@4.*
#:package Microsoft.CodeAnalysis.Workspaces.MSBuild@4.*
#:package Microsoft.Build.Locator@1.*

using Microsoft.Build.Locator;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.MSBuild;
using Microsoft.CodeAnalysis.FindSymbols;

MSBuildLocator.RegisterDefaults();

using var workspace = MSBuildWorkspace.Create();
var project = await workspace.OpenProjectAsync("path/to.csproj");
var compilation = await project.GetCompilationAsync();
```

### Find Symbol by Name

```csharp
var symbol = compilation.GetSymbolsWithName("MyMethod", SymbolFilter.Member).First();
```

### Find All Callers

```csharp
var callers = await SymbolFinder.FindCallersAsync(symbol, project.Solution);
foreach (var caller in callers)
{
    Console.WriteLine($"{caller.CallingSymbol.ContainingType}.{caller.CallingSymbol.Name}");
}
```

### Find Interface Implementations

```csharp
var interfaceSymbol = compilation.GetTypeByMetadataName("MyNamespace.IMyInterface");
var implementations = await SymbolFinder.FindImplementationsAsync(interfaceSymbol, project.Solution);
```

### Data Flow Analysis

```csharp
var tree = compilation.SyntaxTrees.First();
var model = compilation.GetSemanticModel(tree);
var block = tree.GetRoot().DescendantNodes().OfType<BlockSyntax>().First();
var dataFlow = model.AnalyzeDataFlow(block);

// dataFlow.DataFlowsIn — symbols flowing into the block
// dataFlow.DataFlowsOut — symbols flowing out
// dataFlow.ReadInside — symbols read inside
// dataFlow.WrittenInside — symbols written inside
```

### Get Type Info for Expression

```csharp
var typeInfo = model.GetTypeInfo(expression);
var symbolInfo = model.GetSymbolInfo(expression);
```
