---
name: dotnet-verify
description: This skill should be used when working with Verify snapshot tests in .NET projects. Use when updating verified snapshots after intentional code changes, accepting new snapshots, discovering verify tests, or troubleshooting snapshot mismatches. Trigger phrases include "verify tests", "update snapshots", "accept snapshots", "verified files", ".verified.txt".
---

# .NET Verify Snapshot Testing

Manage [Verify](https://github.com/VerifyTests/Verify) snapshot tests using the `verify.tool` dotnet local tool.

## Discovery

To list all test files using Verify snapshots:

```bash
rg -l "Verifier\.Verify|UsesVerify|\.verified\." --type cs
```

To scope to a specific directory:

```bash
rg -l "Verifier\.Verify|UsesVerify|\.verified\." --type cs <path/to/test/directory>
```

## Update Snapshots

To update snapshots after intentional code changes:

1. Build the solution:
   ```bash
   dotnet build -p:WarningLevel=0 /clp:ErrorsOnly --verbosity minimal
   ```

2. Run affected verify tests (they fail, generating `.received.` files):
   ```bash
   dotnet test <test-project> --no-build --filter "FullyQualifiedName~<TestClass>" -v m
   ```

3. Accept all new snapshots:
   ```bash
   dotnet verify accept -y
   ```
   To scope to a specific directory:
   ```bash
   dotnet verify accept -y -w <path/to/test/directory>
   ```

4. Re-run tests to confirm they pass:
   ```bash
   dotnet test <test-project> --no-build --filter "FullyQualifiedName~<TestClass>" -v m
   ```

## File Conventions

- `ClassName.MethodName.verified.txt` — accepted snapshot (committed to git)
- `ClassName.MethodName.received.txt` — latest test output (not committed, gitignored)
- Parameterized tests: `ClassName.MethodName_param=value.verified.txt`

## Quick Reference

| Command | Purpose |
|---|---|
| `dotnet verify accept -y` | Accept all pending snapshots |
| `dotnet verify accept -y -w <dir>` | Accept snapshots in specific directory |
| `rg -l "Verifier\.Verify\|UsesVerify\|\.verified\." --type cs` | List all test files using Verify |
