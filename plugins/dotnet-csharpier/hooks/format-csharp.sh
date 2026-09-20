#!/usr/bin/env bash
# shellcheck shell=bash
set -euo pipefail

# Check if hook is disabled via environment variable.
# CC_HANDBOOK_DOTNET_DISABLE_HOOKS is the name this hook carried inside handbook-dotnet.
if [ "${CC_DOTNET_CSHARPIER_DISABLE_HOOKS:-${CC_HANDBOOK_DOTNET_DISABLE_HOOKS:-false}}" = "true" ]; then
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

# CSharpier reads an unknown option as a path rather than rejecting it, so an option this hook does not
# have right fails every run with "There was no file or directory found at --flag" and nothing is ever
# formatted. The option that treats broken code as a warning was also renamed between 1.2.6
# (--compilation-errors-as-warnings) and 1.3.0 (--syntax-errors-as-warnings), and a machine can easily
# have both versions installed, so the name is chosen from the installed CLI's own help rather than
# hardcoded. The manifest records the names this hook knows about. SCRIPT_DIR rather than
# CLAUDE_PLUGIN_ROOT so the test suite reads the same manifest.
# jq on MSYS writes CRLF, so every value it returns needs the carriage return stripped.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$SCRIPT_DIR/../.claude-plugin/plugin.json"
help_text=$($FORMATTER_CMD format --help 2>&1 || true)
options=()

while read -r option; do
    if echo "$help_text" | grep -q -- "$option"; then
        options+=("$option")
    else
        echo "Warning: CSharpier does not list $option; skipping it. Check $MANIFEST." >&2
    fi
done < <(jq -r '.assumes.csharpier.options.required[]' "$MANIFEST" | tr -d '\r')

while read -r option; do
    if echo "$help_text" | grep -q -- "$option"; then
        options+=("$option")
        break
    fi
done < <(jq -r '.assumes.csharpier.options.errorsAsWarnings[]' "$MANIFEST" | tr -d '\r')

if ! $FORMATTER_CMD format "$file_path" "${options[@]}" 2>&1; then
    echo "Warning: CSharpier formatting failed for $file_path" >&2
    exit 1  # Non-zero exit (not 2) - warns user but doesn't block Claude
fi

exit 0
