# Analysis Script Templates

Ready-to-use templates for common Roslyn queries. Each is a self-contained `dotnet run file.cs` script.

## Template 1: Taint Analysis — Property Assignment Audit

Find all assignments to tracked properties and check if a sanitizer is in the RHS.

**Tier:** Syntax-only | **Use case:** Verify all paths to a sink use a sanitizer

```csharp
#:package Microsoft.CodeAnalysis.CSharp@4.*

using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

var srcDir = args.Length > 0
    ? Path.GetFullPath(args[0])
    : Directory.GetCurrentDirectory();

// CONFIGURE: properties to track and expected sanitizer
var trackedProps = new HashSet<string> { "Content", "Description", "Notes" };
var sanitizer = "EscapePlainTextLines";

var files = Directory.EnumerateFiles(srcDir, "*.cs", SearchOption.AllDirectories);
var results = new List<(string File, int Line, string Prop, string Rhs, bool Ok)>();

foreach (var file in files)
{
    var tree = CSharpSyntaxTree.ParseText(File.ReadAllText(file), path: file);
    foreach (var a in tree.GetRoot().DescendantNodes().OfType<AssignmentExpressionSyntax>())
    {
        if (a.Left is not MemberAccessExpressionSyntax ma) continue;
        if (!trackedProps.Contains(ma.Name.Identifier.Text)) continue;

        var rhs = a.Right.ToString();
        var ok = ContainsCall(a.Right, sanitizer);
        results.Add((Path.GetRelativePath(srcDir, file), 
            a.GetLocation().GetLineSpan().StartLinePosition.Line + 1,
            ma.Name.Identifier.Text, rhs, ok));
    }
}

var violations = results.Where(r => !r.Ok).ToList();
var safe = results.Where(r => r.Ok).ToList();

if (violations.Count > 0)
{
    Console.ForegroundColor = ConsoleColor.Yellow;
    Console.WriteLine($"UNESCAPED ({violations.Count}):");
    Console.ResetColor();
    foreach (var r in violations)
        Console.WriteLine($"  {r.File}:{r.Line}  .{r.Prop} = {Truncate(r.Rhs, 100)}");
}
if (safe.Count > 0)
{
    Console.ForegroundColor = ConsoleColor.Green;
    Console.WriteLine($"Sanitized ({safe.Count}):");
    Console.ResetColor();
    foreach (var r in safe)
        Console.WriteLine($"  {r.File}:{r.Line}  .{r.Prop} = {Truncate(r.Rhs, 100)}");
}

Console.WriteLine($"\nTotal: {results.Count} | Safe: {safe.Count} | Unescaped: {violations.Count}");
return violations.Count > 0 ? 1 : 0;

static bool ContainsCall(SyntaxNode node, string name) =>
    node.DescendantNodesAndSelf().OfType<InvocationExpressionSyntax>().Any(inv =>
        inv.Expression switch
        {
            MemberAccessExpressionSyntax ma => ma.Name.Identifier.Text == name,
            IdentifierNameSyntax id => id.Identifier.Text == name,
            _ => false
        });

static string Truncate(string s, int max)
{
    var one = s.ReplaceLineEndings(" ");
    return one.Length > max ? one[..max] + "..." : one;
}
```

## Template 2: Empty Catch Block Detection

Find catch blocks that swallow exceptions silently.

**Tier:** Syntax-only | **Use case:** Code quality audit

```csharp
#:package Microsoft.CodeAnalysis.CSharp@4.*

using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

var srcDir = args.Length > 0 ? Path.GetFullPath(args[0]) : Directory.GetCurrentDirectory();
var count = 0;

foreach (var file in Directory.EnumerateFiles(srcDir, "*.cs", SearchOption.AllDirectories))
{
    var root = CSharpSyntaxTree.ParseText(File.ReadAllText(file), path: file).GetRoot();
    foreach (var c in root.DescendantNodes().OfType<CatchClauseSyntax>())
    {
        if (c.Block.Statements.Count == 0)
        {
            var line = c.GetLocation().GetLineSpan().StartLinePosition.Line + 1;
            Console.WriteLine($"  {Path.GetRelativePath(srcDir, file)}:{line} - empty catch");
            count++;
        }
    }
}

Console.WriteLine($"\nFound {count} empty catch blocks");
return count > 0 ? 1 : 0;
```

## Template 3: Method Complexity Report

Compute cyclomatic complexity per method, flag methods above threshold.

**Tier:** Syntax-only | **Use case:** Code quality metrics

```csharp
#:package Microsoft.CodeAnalysis.CSharp@4.*

using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

var srcDir = args.Length > 0 ? Path.GetFullPath(args[0]) : Directory.GetCurrentDirectory();
var threshold = args.Length > 1 ? int.Parse(args[1]) : 10;
var findings = new List<(string File, int Line, string Method, int Complexity)>();

foreach (var file in Directory.EnumerateFiles(srcDir, "*.cs", SearchOption.AllDirectories))
{
    var root = CSharpSyntaxTree.ParseText(File.ReadAllText(file), path: file).GetRoot();
    foreach (var method in root.DescendantNodes().OfType<MethodDeclarationSyntax>())
    {
        var complexity = 1; // base
        foreach (var node in method.DescendantNodes())
        {
            complexity += node switch
            {
                IfStatementSyntax => 1,
                WhileStatementSyntax => 1,
                ForStatementSyntax => 1,
                ForEachStatementSyntax => 1,
                CaseSwitchLabelSyntax => 1,
                CasePatternSwitchLabelSyntax => 1,
                ConditionalExpressionSyntax => 1,
                CatchClauseSyntax => 1,
                BinaryExpressionSyntax b when b.OperatorToken.Text is "&&" or "||" or "??" => 1,
                _ => 0
            };
        }

        if (complexity >= threshold)
        {
            var line = method.GetLocation().GetLineSpan().StartLinePosition.Line + 1;
            var name = method.Identifier.Text;
            findings.Add((Path.GetRelativePath(srcDir, file), line, name, complexity));
        }
    }
}

foreach (var f in findings.OrderByDescending(f => f.Complexity))
    Console.WriteLine($"  {f.File}:{f.Line}  {f.Method}() — complexity {f.Complexity}");

Console.WriteLine($"\n{findings.Count} methods above threshold ({threshold})");
```

## Template 4: Find Interface Implementations

Find all classes implementing a specific interface.

**Tier:** Syntax-only (heuristic) | **Use case:** API audit

```csharp
#:package Microsoft.CodeAnalysis.CSharp@4.*

using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

var srcDir = args.Length > 0 ? Path.GetFullPath(args[0]) : Directory.GetCurrentDirectory();
var target = args.Length > 1 ? args[1] : "IFileHandler";

foreach (var file in Directory.EnumerateFiles(srcDir, "*.cs", SearchOption.AllDirectories))
{
    var root = CSharpSyntaxTree.ParseText(File.ReadAllText(file), path: file).GetRoot();
    foreach (var cls in root.DescendantNodes().OfType<ClassDeclarationSyntax>())
    {
        var bases = cls.BaseList?.Types.Select(t => t.Type.ToString()) ?? [];
        if (bases.Any(b => b == target || b.EndsWith($".{target}")))
        {
            var line = cls.GetLocation().GetLineSpan().StartLinePosition.Line + 1;
            Console.WriteLine($"  {Path.GetRelativePath(srcDir, file)}:{line}  {cls.Identifier.Text} : {target}");
        }
    }
}
```

## Template 5: Find Method Override Chain

Find all overrides of a virtual/abstract method.

**Tier:** Syntax-only (heuristic) | **Use case:** Trace all implementations of a base method

```csharp
#:package Microsoft.CodeAnalysis.CSharp@4.*

using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

var srcDir = args.Length > 0 ? Path.GetFullPath(args[0]) : Directory.GetCurrentDirectory();
var methodName = args.Length > 1 ? args[1] : "GetContent";

foreach (var file in Directory.EnumerateFiles(srcDir, "*.cs", SearchOption.AllDirectories))
{
    var root = CSharpSyntaxTree.ParseText(File.ReadAllText(file), path: file).GetRoot();
    foreach (var method in root.DescendantNodes().OfType<MethodDeclarationSyntax>())
    {
        if (method.Identifier.Text != methodName) continue;

        var modifiers = method.Modifiers.ToString();
        var cls = method.FirstAncestorOrSelf<ClassDeclarationSyntax>();
        var className = cls?.Identifier.Text ?? "?";
        var line = method.GetLocation().GetLineSpan().StartLinePosition.Line + 1;
        var tag = modifiers.Contains("override") ? "override"
            : modifiers.Contains("abstract") ? "abstract"
            : modifiers.Contains("virtual") ? "virtual"
            : "new";

        Console.WriteLine($"  {Path.GetRelativePath(srcDir, file)}:{line}  {className}.{methodName}() [{tag}]");
    }
}
```

## Template 6: Find Return Paths Missing Sanitizer

Find all `return` statements inside methods that return a tracked type, checking if the returned expression passes through a sanitizer.

**Tier:** Syntax-only | **Use case:** Verify all return paths from content-producing methods are sanitized

```csharp
#:package Microsoft.CodeAnalysis.CSharp@4.*

using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

var srcDir = args.Length > 0 ? Path.GetFullPath(args[0]) : Directory.GetCurrentDirectory();
var methodNames = new HashSet<string> { "GetContent", "ExtractContent", "GetConfigNotes" };
var sanitizer = "EscapePlainTextLines";

foreach (var file in Directory.EnumerateFiles(srcDir, "*.cs", SearchOption.AllDirectories))
{
    var root = CSharpSyntaxTree.ParseText(File.ReadAllText(file), path: file).GetRoot();
    foreach (var method in root.DescendantNodes().OfType<MethodDeclarationSyntax>())
    {
        if (!methodNames.Contains(method.Identifier.Text)) continue;
        var cls = method.FirstAncestorOrSelf<ClassDeclarationSyntax>()?.Identifier.Text ?? "?";

        foreach (var ret in method.DescendantNodes().OfType<ReturnStatementSyntax>())
        {
            if (ret.Expression is null) continue;
            var expr = ret.Expression.ToString();
            var ok = ret.Expression.DescendantNodesAndSelf()
                .OfType<InvocationExpressionSyntax>()
                .Any(inv => inv.Expression switch
                {
                    MemberAccessExpressionSyntax ma => ma.Name.Identifier.Text == sanitizer,
                    IdentifierNameSyntax id => id.Identifier.Text == sanitizer,
                    _ => false
                });

            var line = ret.GetLocation().GetLineSpan().StartLinePosition.Line + 1;
            var status = ok ? "OK" : "MISSING";
            var color = ok ? ConsoleColor.Green : ConsoleColor.Yellow;
            Console.ForegroundColor = color;
            Console.Write($"  [{status}]");
            Console.ResetColor();
            Console.WriteLine($" {Path.GetRelativePath(srcDir, file)}:{line}  {cls}.{method.Identifier.Text}() -> {Truncate(expr, 80)}");
        }
    }
}

static string Truncate(string s, int max)
{
    var one = s.ReplaceLineEndings(" ");
    return one.Length > max ? one[..max] + "..." : one;
}
```

## Template 7: Call Tree Tracer

Recursively trace all method calls from a given entry point, producing an indented call tree with source locations.

**Tier:** Semantic | **Use case:** Understand execution flow, trace dependencies from a method

```csharp
#:package Microsoft.CodeAnalysis.CSharp.Workspaces@4.*
#:package Microsoft.CodeAnalysis.Workspaces.MSBuild@4.*
#:package Microsoft.Build.Locator@1.*
#:property DisableMSBuildAssemblyCopyCheck=true

using Microsoft.Build.Locator;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.MSBuild;

MSBuildLocator.RegisterDefaults();

var projectPath = args.Length > 0 ? args[0] : throw new ArgumentException("Usage: call-tree.cs <project.csproj> <Class> <Method> [depth]");
var className = args.Length > 1 ? args[1] : "MyService";
var methodName = args.Length > 2 ? args[2] : "ExecuteAsync";
var maxDepth = args.Length > 3 ? int.Parse(args[3]) : 5;

Console.WriteLine($"Loading project: {projectPath}");
using var workspace = MSBuildWorkspace.Create();
workspace.WorkspaceFailed += (_, e) => { };

var project = await workspace.OpenProjectAsync(projectPath);
var solution = project.Solution;
Console.WriteLine($"Loaded {solution.Projects.Count()} projects (via transitive refs)");

var visited = new HashSet<string>();

IMethodSymbol? rootSymbol = null;
foreach (var proj in solution.Projects)
{
    var compilation = await proj.GetCompilationAsync();
    if (compilation is null) continue;

    var candidates = compilation.GetSymbolsWithName(methodName, SymbolFilter.Member)
        .OfType<IMethodSymbol>()
        .Where(m => m.ContainingType.Name == className);

    rootSymbol = candidates.FirstOrDefault();
    if (rootSymbol is not null) break;
}

if (rootSymbol is null)
{
    Console.ForegroundColor = ConsoleColor.Red;
    Console.WriteLine($"Could not find {className}.{methodName}");
    Console.ResetColor();
    return 1;
}

Console.WriteLine($"\nCall tree for {rootSymbol.ContainingType.Name}.{rootSymbol.Name}:\n");
await PrintCallTree(rootSymbol, solution, 0, maxDepth, visited);
return 0;

async Task PrintCallTree(IMethodSymbol method, Solution sol, int depth, int max, HashSet<string> seen)
{
    var key = method.OriginalDefinition.ToDisplayString();
    var indent = new string(' ', depth * 2);
    var loc = method.Locations.FirstOrDefault();
    var locStr = "";
    if (loc?.IsInSource == true)
    {
        var span = loc.GetLineSpan();
        locStr = $" ({Path.GetFileName(span.Path)}:{span.StartLinePosition.Line + 1})";
    }

    var prefix = depth == 0 ? ">" : "|";
    Console.ForegroundColor = loc?.IsInSource == true ? ConsoleColor.Cyan : ConsoleColor.DarkGray;
    Console.Write($"{indent}{prefix} ");
    Console.ResetColor();
    Console.Write($"{method.ContainingType?.Name ?? "?"}.{method.Name}");
    Console.ForegroundColor = ConsoleColor.DarkYellow;
    Console.WriteLine(locStr);
    Console.ResetColor();

    if (seen.Contains(key))
    {
        Console.ForegroundColor = ConsoleColor.DarkGray;
        Console.WriteLine($"{indent}  (already visited)");
        Console.ResetColor();
        return;
    }
    if (depth >= max)
    {
        Console.ForegroundColor = ConsoleColor.DarkGray;
        Console.WriteLine($"{indent}  (max depth)");
        Console.ResetColor();
        return;
    }

    seen.Add(key);

    var syntaxRef = method.DeclaringSyntaxReferences.FirstOrDefault();
    if (syntaxRef is null) return;

    var syntaxNode = await syntaxRef.GetSyntaxAsync();
    var doc = sol.GetDocument(syntaxNode.SyntaxTree);
    if (doc is null) return;

    var semanticModel = await doc.GetSemanticModelAsync();
    if (semanticModel is null) return;

    foreach (var inv in syntaxNode.DescendantNodes().OfType<InvocationExpressionSyntax>())
    {
        var symbolInfo = semanticModel.GetSymbolInfo(inv);
        if (symbolInfo.Symbol is IMethodSymbol calledMethod)
            await PrintCallTree(calledMethod, sol, depth + 1, max, seen);
    }

    foreach (var oc in syntaxNode.DescendantNodes().OfType<ObjectCreationExpressionSyntax>())
    {
        var symbolInfo = semanticModel.GetSymbolInfo(oc);
        if (symbolInfo.Symbol is IMethodSymbol ctor && ctor.Locations.Any(l => l.IsInSource))
        {
            var ctorIndent = new string(' ', (depth + 1) * 2);
            Console.ForegroundColor = ConsoleColor.Green;
            Console.Write($"{ctorIndent}| ");
            Console.ResetColor();
            var ctorLoc = ctor.Locations.First().GetLineSpan();
            Console.WriteLine($"new {ctor.ContainingType.Name}() ({Path.GetFileName(ctorLoc.Path)}:{ctorLoc.StartLinePosition.Line + 1})");
        }
    }
}
```
