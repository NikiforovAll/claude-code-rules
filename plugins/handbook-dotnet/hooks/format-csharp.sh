#!/usr/bin/env bash
# shellcheck shell=bash
set -euo pipefail

# Check if hook is disabled via environment variable
if [ "${CC_HANDBOOK_DOTNET_DISABLE_HOOKS:-false}" = "true" ]; then
    exit 0
fi

# Read JSON input from stdin
input=$(cat)

# Extract file path from tool_input
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Exit silently if no file path
if [ -z "$file_path" ]; then
    exit 0
fi

# Only process C# files (.cs, .CS, .csx, .CSX)
if [[ ! "$file_path" =~ \.(cs|CS|csx|CSX)$ ]]; then
    exit 0
fi

# Check if file exists
if [ ! -f "$file_path" ]; then
    exit 0
fi

# Determine which CSharpier command to use
# Try dotnet csharpier first (local or global dotnet tool)
if dotnet csharpier --version &>/dev/null; then
    FORMATTER_CMD="dotnet csharpier"
# Fall back to csharpier executable (global standalone)
elif command -v csharpier &>/dev/null; then
    FORMATTER_CMD="csharpier"
else
    echo "Error: CSharpier not found. Install with: dotnet tool install -g csharpier" >&2
    exit 1
fi

# Run CSharpier with specified options
# --skip-validation: Skip validation for better performance
# --syntax-errors-as-warnings: Don't block on syntax errors (CSharpier 1.x; was --compilation-errors-as-warnings in 0.x)
if ! $FORMATTER_CMD format "$file_path" --skip-validation --syntax-errors-as-warnings 2>&1; then
    echo "Warning: CSharpier formatting failed for $file_path" >&2
    exit 1  # Non-zero exit (not 2) - warns user but doesn't block Claude
fi

exit 0
