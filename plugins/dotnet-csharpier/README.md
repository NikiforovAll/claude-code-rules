# dotnet-csharpier

Automatic CSharpier formatting for C# files after Claude writes or edits them.

This was part of `handbook-dotnet` until 1.20.1. It is its own plugin now so you can take the .NET skills without the formatting hook, or the hook without the skills.

## Features

- A `PostToolUse` hook that formats `.cs`, `.CS`, `.csx` and `.CSX` files after `Write` or `Edit`
- Picks up `dotnet csharpier` (repo tool manifest) first, then a global `csharpier`
- Reads your `.csharpierrc` if you have one
- Non-blocking: a failure warns and never stops Claude
- Survives the CSharpier option rename between 1.2.x and 1.3.x

## Prerequisites

CSharpier, and `jq` for reading the hook's JSON input.

```bash
dotnet tool install -g csharpier
```

## Installation

```bash
claude plugin marketplace add nikiforovall/claude-code-rules
claude plugin install dotnet-csharpier@cc-handbook
```

## Configuration

Disable the hook:

```bash
# For your shell
export CC_DOTNET_CSHARPIER_DISABLE_HOOKS=true

# For one Claude Code session
CC_DOTNET_CSHARPIER_DISABLE_HOOKS=true claude
```

`CC_HANDBOOK_DOTNET_DISABLE_HOOKS`, the name this hook used inside `handbook-dotnet`, still works.

To change how CSharpier formats, put a `.csharpierrc` or `.csharpierrc.json` in your project root.

## What the plugin assumes about CSharpier

`.claude-plugin/plugin.json` records the CSharpier version the hook is written against and the CLI options it passes:

```json
"assumes": {
  "csharpier": {
    "majorVersion": 1,
    "testedWith": ["1.2.6", "1.3.0"],
    "options": {
      "required": ["--skip-validation"],
      "errorsAsWarnings": [
        "--compilation-errors-as-warnings",
        "--syntax-errors-as-warnings"
      ]
    }
  }
}
```

This is not decoration. CSharpier reads an option it does not know as a *path*, so a wrong option name does not produce a clear error — every run fails with `There was no file or directory found at --flag` and nothing is ever formatted. That is exactly what happened when `--compilation-errors-as-warnings` (1.2.6) became `--syntax-errors-as-warnings` (1.3.0).

So the hook does not hardcode a name. It reads `format --help` from whichever CSharpier is installed and uses the first spelling that CLI actually lists. When you add support for a new CSharpier version, add its option names here and the hook follows.

## Tests

```bash
bash hooks/test-format-hook.sh
```

The suite checks file-type filtering, input validation, both disable variables, real formatting, and — against every CSharpier on the machine — that the options recorded in the manifest still exist. That last group is the one that catches an upstream rename before your next edit does.
