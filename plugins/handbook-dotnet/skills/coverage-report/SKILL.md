---
name: coverage-report
description: Generate a .NET code coverage report scoped to files changed in the current branch. Runs tests with coverage collection and produces filtered HTML reports.
allowed-tools: Bash(dotnet test:*), Bash(dotnet reportgenerator:*), Bash(git diff:*), Bash(git merge-base:*), Bash(start:*), Read, Grep, Glob
---

# Code Coverage Report

Generate a code coverage report scoped to source files changed in the current branch compared to a base branch.

## Workflow

### 1. Determine base branch

Detect the base branch to diff against. Use the MR/PR target branch if known, otherwise default to `main` or `master` (whichever exists). Ask the user if ambiguous.

```bash
git merge-base --fork-point main HEAD || git merge-base --fork-point master HEAD
```

### 2. Detect changed source files

```bash
git diff <base-branch> --name-only -- '*.cs'
```

Filter out test files (paths containing `Test`, `Tests`, `.Tests`, `.Test`).
If no source files changed, stop and inform the user.

### 3. Identify test project(s)

Determine which test project(s) to run. Strategies (in order):

1. **User-specified**: If the user names a test project, use it
2. **Convention-based**: Look for test projects whose name matches the changed project (e.g., `MyProject` -> `MyProject.Tests`)
3. **Solution-wide**: Run all tests in the solution if scope is unclear
4. **Ask**: If ambiguous, ask the user which test project(s) to run

### 4. Clean previous results

```bash
rm -rf TestResults/
```

### 5. Run tests with coverage

```bash
dotnet test <test-project-or-solution> \
  --collect:"XPlat Code Coverage" \
  --results-directory ./TestResults/
```

### 6. Build file filters

From the changed file list (step 2), extract basenames and build a filter string:

```
+*FileName1.cs;+*FileName2.cs;+*FileName3.cs
```

### 7. Generate report

```bash
dotnet reportgenerator \
  -reports:"TestResults/**/coverage.cobertura.xml" \
  -targetdir:"TestResults/CoverageReport" \
  -reporttypes:"Html;TextSummary" \
  -filefilters:"<filters>"
```

### 8. Display results

1. Print `TestResults/CoverageReport/Summary.txt` to the terminal
2. Open the HTML report (platform-aware):
   - Windows: `start TestResults/CoverageReport/index.html`
   - macOS: `open TestResults/CoverageReport/index.html`
   - Linux: `xdg-open TestResults/CoverageReport/index.html`

## Tips

- For large solutions, scope to specific test projects to speed up collection
- The `-filefilters` flag accepts wildcards -- basename matching avoids path sensitivity
