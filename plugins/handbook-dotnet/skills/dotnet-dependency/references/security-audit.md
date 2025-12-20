# Security Audit for Dependencies

Audit .NET project dependencies for security vulnerabilities, outdated packages, and deprecated libraries.

## Vulnerable Packages

Find packages with known security vulnerabilities:

```bash
# Check for vulnerable packages
dotnet list package --vulnerable

# Include transitive dependencies
dotnet list package --vulnerable --include-transitive

# JSON output for CI/CD
dotnet list package --vulnerable --format json
```

Requirements: .NET SDK 9.0.300+ for vulnerability scanning.

## Outdated Packages

### Using built-in commands

```bash
# Find packages with newer versions
dotnet list package --outdated

# Include prerelease versions
dotnet list package --outdated --include-prerelease

# Limit to patch updates only (same major.minor)
dotnet list package --outdated --highest-patch

# Limit to minor updates only (same major)
dotnet list package --outdated --highest-minor

# JSON output
dotnet list package --outdated --format json
```

### Using dotnet outdated (Third-party)

Install: `dotnet tool install -g dotnet-outdated-tool`

```bash
# Check for outdated packages (nicer output)
dotnet outdated

# Auto-update all packages to latest
dotnet outdated -u

# Include specific packages only
dotnet outdated -u -inc PackageName

# Exclude specific packages
dotnet outdated -u -exc PackageName

# Update to highest minor version only
dotnet outdated -u -vl Minor

# Update to highest patch version only
dotnet outdated -u -vl Patch
```

## Deprecated Packages

```bash
# Find deprecated packages
dotnet list package --deprecated

# Include transitive dependencies
dotnet list package --deprecated --include-transitive
```

## Framework-Specific Auditing

```bash
# Audit specific framework only
dotnet list package --outdated --framework net8.0
dotnet list package --vulnerable --framework net8.0
```

## CI/CD Integration

Generate JSON reports for automated pipelines:

```bash
# Full security report
dotnet list package --vulnerable --include-transitive --format json > vulnerable.json
dotnet list package --outdated --format json > outdated.json
dotnet list package --deprecated --format json > deprecated.json
```

## Combined Workflow

For a comprehensive security audit:

```bash
# 1. Check for vulnerabilities (critical)
dotnet list package --vulnerable --include-transitive

# 2. Check for deprecated packages
dotnet list package --deprecated

# 3. Check for outdated packages
dotnet list package --outdated

# 4. Update packages (using dotnet outdated)
dotnet outdated -u
```

## Package Source Configuration

Vulnerability data comes from configured NuGet sources. Ensure your `nuget.config` includes vulnerability-aware sources:

```xml
<configuration>
  <packageSources>
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
  </packageSources>
  <auditSources>
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
  </auditSources>
</configuration>
```

## References

- [dotnet list package](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-list-package)
- [dotnet-outdated tool](https://github.com/dotnet-outdated/dotnet-outdated)
