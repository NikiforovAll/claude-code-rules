# Blame Mode for Test Debugging

Blame mode helps identify tests that cause crashes, hangs, or process termination. It sequences test execution and logs which test was running when a failure occurred.

## When to Use Blame Mode

- Tests crash the test host process
- Tests hang indefinitely
- Debugging intermittent test failures
- Identifying tests that corrupt shared state
- CI pipelines fail mysteriously

## Basic Blame Mode

Enable blame mode to log test sequence and identify the last running test:

```bash
dotnet test --blame
```

Output: Creates a `Sequence.xml` file in `TestResults/` showing test execution order.

## Crash Dump Collection

Collect crash dumps when tests crash the host process:

```bash
# Collect crash dump on failure
dotnet test --blame-crash

# Specify dump type (mini or full)
dotnet test --blame-crash --blame-crash-dump-type mini
dotnet test --blame-crash --blame-crash-dump-type full

# Collect dump on unexpected exit
dotnet test --blame-crash-collect-always
```

### Dump Types

| Type   | Size         | Content                      |
| ------ | ------------ | ---------------------------- |
| `mini` | Small (~5MB) | Stack traces, loaded modules |
| `full` | Large        | Complete process memory      |

Recommendation: Start with `mini` dumps. Use `full` only when mini dumps lack sufficient detail.

## Hang Detection

Detect and collect information when tests hang:

```bash
# Detect hangs with timeout
dotnet test --blame-hang --blame-hang-timeout 5m

# Specify dump type for hangs
dotnet test --blame-hang --blame-hang-dump-type mini --blame-hang-timeout 3m
```

### Timeout Format

- `5m` - 5 minutes
- `30s` - 30 seconds
- `1h` - 1 hour
- `5000ms` - 5000 milliseconds

## Combined Usage

For comprehensive debugging, combine options:

```bash
dotnet test \
  --blame \
  --blame-crash \
  --blame-crash-dump-type mini \
  --blame-hang \
  --blame-hang-timeout 5m \
  --blame-hang-dump-type mini
```

## Results Location

Blame data is saved to:

```
TestResults/
├── {guid}/
│   ├── Sequence.xml          # Test execution sequence
│   ├── crash_dump.dmp        # Crash dump (if crash occurred)
│   └── hang_dump.dmp         # Hang dump (if timeout occurred)
```

Specify custom location:

```bash
dotnet test --blame --results-directory ./MyResults
```

## Analyzing Results

### Reading Sequence.xml

The sequence file shows tests in execution order:

```xml
<TestSequence>
  <Test Name="Test1" Source="Tests.dll" />
  <Test Name="Test2" Source="Tests.dll" />  <!-- Last test before crash -->
</TestSequence>
```

### Analyzing Dumps

Use Visual Studio or WinDbg to analyze `.dmp` files:

```bash
# Windows: Open in Visual Studio
# Linux/Mac: Use lldb or dotnet-dump
dotnet-dump analyze crash_dump.dmp
```

## CI/CD Integration

For CI pipelines, enable blame mode to diagnose failures:

```bash
dotnet test \
  --blame \
  --blame-crash \
  --blame-hang --blame-hang-timeout 10m \
  --logger trx \
  --results-directory ./TestResults
```

Artifacts to preserve:

- `TestResults/` directory
- Any `.dmp` files
- `Sequence.xml` files

## Common Scenarios

### Scenario: Random test failures in CI

```bash
dotnet test --blame --blame-crash
```

Check `Sequence.xml` to find which test was running during failure.

### Scenario: Tests hang indefinitely

```bash
dotnet test --blame-hang --blame-hang-timeout 5m --blame-hang-dump-type full
```

Analyze the hang dump to find deadlocks or infinite loops.

### Scenario: Test host crashes with no output

```bash
dotnet test --blame-crash --blame-crash-dump-type full --blame-crash-collect-always
```

Use full dump to get complete memory state for analysis.
