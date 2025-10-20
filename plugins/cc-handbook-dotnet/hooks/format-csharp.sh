#!/usr/bin/env bash
set -euo pipefail

# Read JSON input from stdin
input=$(cat)

# Extract file path from tool_input
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Exit silently if no file path
if [ -z "$file_path" ]; then
    exit 0
fi

# Only process .cs files
if [[ ! "$file_path" =~ \.cs$ ]]; then
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
# --compilation-errors-as-warnings: Don't block on compilation errors
if ! $FORMATTER_CMD format "$file_path" --skip-validation --compilation-errors-as-warnings 2>&1; then
    echo "Warning: CSharpier formatting failed for $file_path" >&2
    exit 1  # Non-zero exit (not 2) - warns user but doesn't block Claude
fi

exit 0
