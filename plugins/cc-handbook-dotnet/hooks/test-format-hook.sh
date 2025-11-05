#!/usr/bin/env bash
# shellcheck shell=bash
# Test script for CSharpier formatter hook

set -euo pipefail

# Get script directory and setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_SCRIPT="$SCRIPT_DIR/format-csharp.sh"
TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT

# Test counters
PASSED=0
FAILED=0
SKIPPED=0

# Convert paths for Windows (MINGW/Git Bash)
to_path() {
    if command -v cygpath &>/dev/null; then
        cygpath -w "$1" | sed 's/\\/\\\\/g'
    else
        echo "$1"
    fi
}

# Run a test
test_hook() {
    local name="$1"
    local json="$2"
    local env="${3:-}"

    echo -n "  $name ... "

    local exit_code=0
    if [ -n "$env" ]; then
        echo "$json" | $env bash "$HOOK_SCRIPT" &>/dev/null || exit_code=$?
    else
        echo "$json" | bash "$HOOK_SCRIPT" &>/dev/null || exit_code=$?
    fi

    if [ "$exit_code" -eq 0 ]; then
        echo "✓"
        PASSED=$((PASSED + 1))
    else
        echo "✗ (exit code: $exit_code)"
        FAILED=$((FAILED + 1))
    fi
}

echo "=============================="
echo "CSharpier Hook Test Suite"
echo "=============================="
echo ""

# File Type Filtering Tests
echo "File Type Filtering:"
echo "namespace Test{class X{}}" > "$TEST_DIR/test.cs"
test_hook "Processes .cs files" "{\"tool_input\":{\"file_path\":\"$(to_path "$TEST_DIR/test.cs")\"}}"

echo "class Test{}" > "$TEST_DIR/test.CS"
test_hook "Processes .CS files" "{\"tool_input\":{\"file_path\":\"$(to_path "$TEST_DIR/test.CS")\"}}"

echo "Console.WriteLine(\"test\");" > "$TEST_DIR/test.csx"
test_hook "Processes .csx files" "{\"tool_input\":{\"file_path\":\"$(to_path "$TEST_DIR/test.csx")\"}}"

echo "text" > "$TEST_DIR/test.txt"
test_hook "Ignores .txt files" "{\"tool_input\":{\"file_path\":\"$(to_path "$TEST_DIR/test.txt")\"}}"

echo "text" > "$TEST_DIR/test.cs.bak"
test_hook "Ignores .cs.bak files" "{\"tool_input\":{\"file_path\":\"$(to_path "$TEST_DIR/test.cs.bak")\"}}"

echo ""
echo "Input Validation:"
test_hook "Handles missing file_path" "{\"tool_input\":{}}"
test_hook "Handles empty file_path" "{\"tool_input\":{\"file_path\":\"\"}}"
test_hook "Handles nonexistent file" "{\"tool_input\":{\"file_path\":\"$(to_path "$TEST_DIR/missing.cs")\"}}"

echo ""
echo "Environment Variable:"

# Test that env var actually prevents formatting
cat > "$TEST_DIR/env-test.cs" << 'EOF'
class Example
{
}
EOF
BEFORE=$(cat "$TEST_DIR/env-test.cs")
ENV_PATH=$(to_path "$TEST_DIR/env-test.cs")

echo -n "  Respects DISABLE_HOOKS=true ... "
echo "{\"tool_input\":{\"file_path\":\"$ENV_PATH\"}}" | CC_HANDBOOK_DOTNET_DISABLE_HOOKS=true bash "$HOOK_SCRIPT" &>/dev/null || true
AFTER=$(cat "$TEST_DIR/env-test.cs")
if [ "$BEFORE" = "$AFTER" ]; then
    echo "✓"
    PASSED=$((PASSED + 1))
else
    echo "✗ (file was formatted despite env var)"
    FAILED=$((FAILED + 1))
fi

# Verify formatting works without env var
cat > "$TEST_DIR/env-test2.cs" << 'EOF'
class Example
{
}
EOF
BEFORE=$(cat "$TEST_DIR/env-test2.cs")
ENV_PATH2=$(to_path "$TEST_DIR/env-test2.cs")

echo -n "  Works by default (no env var) ... "
echo "{\"tool_input\":{\"file_path\":\"$ENV_PATH2\"}}" | bash "$HOOK_SCRIPT" &>/dev/null || true
AFTER=$(cat "$TEST_DIR/env-test2.cs")
if [ "$BEFORE" != "$AFTER" ]; then
    echo "✓"
    PASSED=$((PASSED + 1))
else
    echo "✗ (file was not formatted)"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "Code Formatting:"

# Check if CSharpier is available
if ! command -v csharpier &>/dev/null && ! dotnet csharpier --version &>/dev/null 2>&1; then
    echo "  Formats C# code ... ⊘ (CSharpier not installed)"
    SKIPPED=$((SKIPPED + 1))
else
    # Create badly formatted code
    cat > "$TEST_DIR/format-test.cs" << 'EOF'
class Example
{
}
EOF
    BEFORE=$(cat "$TEST_DIR/format-test.cs")

    # Run formatter
    FMT_PATH=$(to_path "$TEST_DIR/format-test.cs")
    echo "{\"tool_input\":{\"file_path\":\"$FMT_PATH\"}}" | bash "$HOOK_SCRIPT" &>/dev/null || true

    AFTER=$(cat "$TEST_DIR/format-test.cs")

    echo -n "  Formats C# code ... "
    if [ "$BEFORE" != "$AFTER" ]; then
        echo "✓"
        PASSED=$((PASSED + 1))
    else
        echo "✗ (no formatting occurred)"
        FAILED=$((FAILED + 1))
    fi
fi

# Results
echo ""
echo "=============================="
TOTAL=$((PASSED + FAILED + SKIPPED))
echo "Results: $PASSED/$TOTAL passed"
[ "$SKIPPED" -gt 0 ] && echo "         $SKIPPED skipped"
echo "=============================="

[ "$FAILED" -eq 0 ]
