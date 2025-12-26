---
name: dotnet-test
description: This skill should be used when running .NET tests selectively with a build-first, test-targeted workflow. Use it for running tests with xUnit focus.
allowed-tools: Bash(dotnet build:*), Bash(dotnet test:*), Read, Grep, Glob
---

# .NET Test Runner

Run .NET tests selectively using a build-first, test-targeted workflow optimized for development speed.

## Core Workflow

Follow this workflow to run tests efficiently:

### Step 1: Build Solution First

Build the entire solution with minimal output to catch compile errors early:

```bash
dotnet build -p:WarningLevel=0 /clp:ErrorsOnly --verbosity minimal
```

### Step 2: Run Specific Project Tests

Run tests for the specific test project with `--no-build` to skip redundant compilation:

```bash
dotnet test path/to/project --no-build --verbosity minimal
```

### Step 3: Filter When Targeting Specific Tests

Narrow down to specific tests using filter expressions:

```bash
# By method name (contains)
dotnet test --no-build --filter "Name~MyTestMethod"

# By class name (exact match)
dotnet test --no-build --filter "ClassName=MyNamespace.MyTestClass"

# Combined filters
dotnet test --no-build --filter "Name~Create|Name~Update"
```

## Quick Reference

### Commands

| Command                                                              | Purpose                              |
| -------------------------------------------------------------------- | ------------------------------------ |
| `dotnet build -p:WarningLevel=0 /clp:ErrorsOnly --verbosity minimal` | Build solution with minimal output   |
| `dotnet test path/to/Tests.csproj --no-build`                        | Run project tests (skip build)       |
| `dotnet test --no-build --logger "console;verbosity=detailed"`       | Show ITestOutputHelper output        |
| `dotnet test --no-build --filter "..."`                              | Run filtered tests                   |
| `dotnet test --no-build --list-tests`                                | List available tests without running |

### Filter Operators

| Operator | Meaning          | Example                                                        |
| -------- | ---------------- | -------------------------------------------------------------- |
| `=`      | Exact match      | `ClassName=MyTests`                                            |
| `!=`     | Not equal        | `Name!=SkipThis`                                               |
| `~`      | Contains         | `Name~Create`                                                  |
| `!~`     | Does not contain | `Name!~Integration`                                            |
| `\|`     | OR               | `Name~Test1\|Name~Test2` (note '\|' is an escape for markdown) |
| `&`      | AND              | `Name~User&Category=Unit`                                      |

### xUnit Filter Properties

| Property             | Description                   | Example                                  |
| -------------------- | ----------------------------- | ---------------------------------------- |
| `FullyQualifiedName` | Full test name with namespace | `FullyQualifiedName~MyNamespace.MyClass` |
| `DisplayName`        | Test display name             | `DisplayName=My_Test_Name`               |
| `Name`               | Method name                   | `Name~ShouldCreate`                      |
| `Category`           | Trait category                | `Category=Unit`                          |

### Common Filter Patterns

```bash
# Run tests containing "Create" in method name
dotnet test --no-build --filter "Name~Create"

# Run tests in a specific class
dotnet test --no-build --filter "ClassName=MyNamespace.UserServiceTests"

# Run tests matching namespace pattern
dotnet test --no-build --filter "FullyQualifiedName~MyApp.Tests.Unit"

# Run tests with specific trait
dotnet test --no-build --filter "Category=Integration"

# Exclude slow tests
dotnet test --no-build --filter "Category!=Slow"

# Combined: class AND method pattern
dotnet test --no-build --filter "ClassName=OrderTests&Name~Validate"
```

### ITestOutputHelper Output

To see output from xUnit's `ITestOutputHelper`, use the console logger with detailed verbosity:

```bash
dotnet test --no-build --logger "console;verbosity=detailed"
```

### Reducing Output Noise

Verbosity levels for `dotnet test`:

| Level      | Flag      | Description                     |
| ---------- | --------- | ------------------------------- |
| quiet      | `-v q`    | Minimal output (pass/fail only) |
| minimal    | `-v m`    | Clean summary, no test output   |
| normal     | `-v n`    | Default, shows discovered tests |
| detailed   | `-v d`    | Shows more details              |
| diagnostic | `-v diag` | Most verbose                    |

To see test output, use grep to filter out discovery messages (for xUnit):

```bash
dotnet test --no-build --logger "console;verbosity=detailed" 2>&1 | grep -v "Discovered \[execution\]"
```

## Framework Differences

This skill focuses on **xUnit**. For MSTest or NUnit, filter property names differ:

| Property       | xUnit       | MSTest         | NUnit       |
| -------------- | ----------- | -------------- | ----------- |
| Method name    | `Name`      | `Name`         | `Name`      |
| Class name     | `ClassName` | `ClassName`    | `ClassName` |
| Category/Trait | `Category`  | `TestCategory` | `Category`  |
| Priority       | -           | `Priority`     | `Priority`  |

## Progressive Disclosure

For advanced debugging scenarios, load additional references:

- **references/blame-mode.md** - Debugging test crashes and hangs with `--blame`
- **references/parallel-execution.md** - Controlling parallel test execution

Load these references when:

- Tests are crashing or hanging unexpectedly
- Diagnosing test isolation issues
- Optimizing test run performance

## When to Use This Skill

Invoke when the user needs to:

- Run targeted tests during development
- Filter tests by method or class name
- Understand test output and filtering options
- Debug failing or hanging tests
