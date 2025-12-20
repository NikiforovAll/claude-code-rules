# Parallel Test Execution Control

By default, .NET test runner executes tests in parallel for performance. This reference covers controlling parallelism at different levels.

## Default Behavior

- **Solution level**: Test projects run in parallel
- **Project level**: Depends on test framework settings
- **Multi-targeted projects**: Target frameworks run in parallel (.NET 9+)

## Controlling Parallelism

### Solution/Project Level

Disable parallel execution across target frameworks (multi-targeted projects):

```bash
dotnet test -p:TestTfmsInParallel=false
```

Limit parallel test assemblies:

```bash
dotnet test -p:MaxCpuCount=1
```

### xUnit Parallelism

xUnit runs test collections in parallel by default. Control via `xunit.runner.json`:

```json
{
  "$schema": "https://xunit.net/schema/current/xunit.runner.schema.json",
  "parallelizeAssembly": false,
  "parallelizeTestCollections": true,
  "maxParallelThreads": 4
}
```

Or via assembly attribute in code:

```csharp
[assembly: CollectionBehavior(DisableTestParallelization = true)]
```

### Collection-Based Control

Group related tests into collections to control execution:

```csharp
[Collection("Database")]
public class UserRepositoryTests { }

[Collection("Database")]
public class OrderRepositoryTests { }
```

Tests in the same collection run sequentially; different collections run in parallel.

To disable parallelism for a collection:

```csharp
[CollectionDefinition("Database", DisableParallelization = true)]
public class DatabaseCollection { }
```

## When to Disable Parallelism

### Shared Resources

- Database connections with transactions
- File system operations on same files
- In-memory caches or singletons
- External service dependencies with rate limits

### Test Isolation Issues

- Tests modify global state
- Tests use static fields
- Tests share test fixtures incorrectly

### Debugging

- Reproducing intermittent failures
- Analyzing test execution order
- Profiling individual tests

## Performance Optimization

### Maximize Parallelism

For well-isolated tests, increase parallel threads:

```json
{
  "maxParallelThreads": -1
}
```

`-1` uses processor count × 1 thread.

### Balance Memory and Speed

For memory-intensive tests, limit parallelism:

```json
{
  "maxParallelThreads": 2
}
```

### Parallel Categories

Run integration tests sequentially, unit tests in parallel:

```bash
# Fast unit tests (parallel)
dotnet test --filter "Category=Unit"

# Slow integration tests (sequential)
dotnet test --filter "Category=Integration" -p:MaxCpuCount=1
```

## Command Line Options

| Option                                            | Purpose                        |
| ------------------------------------------------- | ------------------------------ |
| `-p:TestTfmsInParallel=false`                     | Disable multi-TFM parallelism  |
| `-p:MaxCpuCount=N`                                | Limit parallel test assemblies |
| `-- RunConfiguration.DisableParallelization=true` | Disable via runsettings        |

## RunSettings File

Create `test.runsettings` for persistent configuration:

```xml
<?xml version="1.0" encoding="utf-8"?>
<RunSettings>
  <RunConfiguration>
    <DisableParallelization>true</DisableParallelization>
    <MaxCpuCount>1</MaxCpuCount>
  </RunConfiguration>
</RunSettings>
```

Use with:

```bash
dotnet test --settings test.runsettings
```

## Troubleshooting

### Symptom: Random test failures in CI

Cause: Tests share state without proper isolation.

Fix: Use `[Collection]` to group dependent tests, or disable parallelism temporarily while fixing isolation issues.

### Symptom: Tests pass individually, fail together

Cause: Parallel execution exposes race conditions.

Fix: Identify shared resources. Use dependency injection for test-scoped resources.

### Symptom: High memory usage during tests

Cause: Too many parallel test processes.

Fix: Reduce `maxParallelThreads` or use `-p:MaxCpuCount=2`.
