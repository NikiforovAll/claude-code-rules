# Simple Guide: dotnet run files

Quick start guide for running C# files directly with `dotnet run`.

## Stdin Execution (One-liners)

Perfect for Claude Code and quick scripts:

```bash
# Basic output
echo 'Console.WriteLine("Hello");' | dotnet run -

# Math calculation
echo 'Console.WriteLine(Math.Sqrt(144));' | dotnet run -

# Date/time
echo 'Console.WriteLine(DateTime.Now.ToString("yyyy-MM-dd"));' | dotnet run -

# Environment info
echo 'Console.WriteLine(Environment.OSVersion);' | dotnet run -
```

## Multi-line with Heredoc

```bash
dotnet run - << 'EOF'
var numbers = new[] { 1, 2, 3, 4, 5 };
var sum = numbers.Sum();
Console.WriteLine($"Sum: {sum}");
EOF
```

## Using NuGet Packages

Add `#:package` directive:

```bash
# Humanizer for text manipulation
dotnet run - << 'EOF'
#:package Humanizer@*
using Humanizer;
Console.WriteLine(TimeSpan.FromMinutes(90).Humanize());
EOF

# JSON serialization (built-in, no package needed)
dotnet run - << 'EOF'
using System.Text.Json;
var data = new { Name = "Test", Value = 42 };
Console.WriteLine(JsonSerializer.Serialize(data));
EOF
```

## Common Use Cases

### Quick HTTP Request

```bash
dotnet run - << 'EOF'
var client = new HttpClient();
var response = await client.GetStringAsync("https://httpbin.org/get");
Console.WriteLine(response);
EOF
```

### Read and Process File

```bash
dotnet run - << 'EOF'
var lines = File.ReadAllLines("data.txt");
Console.WriteLine($"Lines: {lines.Length}");
foreach (var line in lines.Take(5))
    Console.WriteLine(line);
EOF
```

### JSON Processing

```bash
dotnet run - << 'EOF'
using System.Text.Json;

var json = """{"name":"Alice","age":30}""";
var doc = JsonDocument.Parse(json);
Console.WriteLine(doc.RootElement.GetProperty("name").GetString());
EOF
```

### Generate GUID

```bash
echo 'Console.WriteLine(Guid.NewGuid());' | dotnet run -
```

## Directives Quick Reference

| Directive | Purpose | Example |
|-----------|---------|---------|
| `#:package` | Add NuGet package | `#:package Humanizer@2.14.1` |
| `#:sdk` | Set SDK type | `#:sdk Microsoft.NET.Sdk.Web` |
| `#:property` | MSBuild property | `#:property LangVersion preview` |
| `#:project` | Project reference | `#:project ../MyLib` |


## Directives Reference

### Package References (`#:package`)

Version is required. Use wildcards for flexibility:

```csharp
#:package Humanizer@*                  // Latest version
#:package Dapper@2.*                   // Latest 2.x
#:package Newtonsoft.Json@13.0.3       // Specific version
```

### SDK Selection (`#:sdk`)

```csharp
#:sdk Microsoft.NET.Sdk              // Default console
#:sdk Microsoft.NET.Sdk.Web          // ASP.NET Core
#:sdk Microsoft.NET.Sdk.Worker       // Worker services
#:sdk Aspire.AppHost.Sdk@9.0.0       // .NET Aspire
```

### MSBuild Properties (`#:property`)

```csharp
#:property LangVersion preview
#:property Nullable enable
#:property ImplicitUsings enable
#:property UserSecretsId my-app-secrets
```

### Project References (`#:project`)

```csharp
#:project ../src/MyLibrary
#:project ../src/MyLibrary/MyLibrary.csproj
```

## Tips

- Use single quotes around heredoc delimiter (`'EOF'`) to prevent shell expansion
- Directives must be at the top of the file/input
- Top-level statements work by default (no Main method needed)
- `await` works at top level for async operations
