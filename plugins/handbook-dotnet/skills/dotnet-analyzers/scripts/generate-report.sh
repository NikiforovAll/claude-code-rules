#!/usr/bin/env bash
set -euo pipefail

# Generate .NET Analyzer Dashboard HTML from dotnet format reports.
#
# Usage:
#   generate-report.sh [solution-or-project] [output.html]
#   generate-report.sh --sarif [solution-or-project] [output.html]
#
# --sarif mode: harvest Roslyn ErrorLog SARIF from a forced `dotnet build -t:Rebuild`
# instead of running `dotnet format`. Captures CS*/MUD* diagnostics that format
# skips, and respects editorconfig severity (filters SARIF level=note + suppressed).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="$SCRIPT_DIR/template.html"

BUILD_MODE=0
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --sarif) BUILD_MODE=1; shift ;;
    --dashboard) shift ;; # no-op: dashboard is always emitted
    --) shift; POSITIONAL+=("$@"); break ;;
    *) POSITIONAL+=("$1"); shift ;;
  esac
done
set -- "${POSITIONAL[@]}"

PROJECT="${1:-.}"
OUTPUT="${2:-analyzer-dashboard.html}"

# Resolve project root for relative paths
if [[ -d "$PROJECT" ]]; then
  PROJECT_ROOT="$(cd "$PROJECT" && pwd)"
elif [[ -f "$PROJECT" ]]; then
  PROJECT_ROOT="$(cd "$(dirname "$PROJECT")" && pwd)"
else
  PROJECT_ROOT="$(pwd)"
fi
PROJECT_NAME="$(basename "$PROJECT_ROOT")"
if [[ -f "$PROJECT" ]]; then
  PROJECT_NAME="$(basename "$PROJECT" | sed 's/\.\(sln\|csproj\|fsproj\)$//')"
fi

if [[ $BUILD_MODE -eq 1 ]]; then
  # SARIF approach: Roslyn writes a structured JSON diagnostics file per project
  # when `-p:ErrorLog=<name>%2cversion=2.1` is set. `%2c` URL-encodes the comma
  # so MSBuild keeps both the path and the version flag in one property value.
  # `-t:Rebuild` forces analyzers to re-run on already-compiled assemblies.
  #
  # Coverage: CS* (compiler) + CA*/S*/IDE*/IDISP*/ASP*/MUD*/etc. (Roslyn analyzers).
  # Excluded by design: NU* (restore), MSB* (build engine).
  SARIF_NAME="_analyzer-diag.sarif"
  echo "Cleaning prior SARIF artefacts..." >&2
  fd -t f "^${SARIF_NAME}$" --no-ignore -HI -x rm -f {} 2>/dev/null || true
  echo "Running dotnet build -t:Rebuild with SARIF output..." >&2
  dotnet build "$PROJECT" -t:Rebuild "-p:ErrorLog=${SARIF_NAME}%2cversion=2.1" -nologo > /dev/null 2>&1 || true

  SARIF_FILES=$(fd -t f "^${SARIF_NAME}$" --no-ignore -HI)
  if [[ -z "$SARIF_FILES" ]]; then
    echo "No SARIF files produced — build may have failed before analyzer phase." >&2
    exit 1
  fi

  win_root="$(cd "$PROJECT_ROOT" && pwd -W 2>/dev/null || echo "$PROJECT_ROOT" | sed 's|^/\([a-zA-Z]\)/|\1:/|')"

  # Flatten all SARIF rules+results into one normalized list, dedup by id+location.
  # Each record carries id, desc (rule shortDescription/text), uri, line, col.
  ALL_JSON=$(echo "$SARIF_FILES" | xargs -I@@ jq -c '
    [.runs[] as $r |
      ($r.tool.driver.rules // []) as $rules |
      $r.results[]? |
      select((.suppressions // []) | length == 0) |
      select((.level // "warning") | IN("error","warning")) |
      . as $res |
      ($rules[.ruleIndex // -1]? // {}) as $rule |
      {
        id: .ruleId,
        desc: ($rule.shortDescription.text // $rule.fullDescription.text // .message.text),
        uri: (.locations[0].physicalLocation.artifactLocation.uri // ""),
        line: (.locations[0].physicalLocation.region.startLine // 0),
        col: (.locations[0].physicalLocation.region.startColumn // 0)
      }
    ] | .[]' @@ | jq -s --arg root "$win_root" '
      unique_by("\(.id)|\(.uri)|\(.line)|\(.col)") |
      map(.uri |= (sub("^file:///"; "") | sub($root + "/"; "")))
    ')

  # Build dashboard data. Route IDE* → style bucket, everything else → analyzer bucket
  # (template uses these split arrays for the IDE/CA toggle UI).
  STYLE_V=$(echo "$ALL_JSON" | jq '
    [.[] | select(.id | startswith("IDE"))] |
    group_by(.id) |
    map({id: .[0].id, count: length, desc: .[0].desc}) |
    sort_by(-.count)')
  ANALYZER_V=$(echo "$ALL_JSON" | jq '
    [.[] | select(.id | startswith("IDE") | not)] |
    group_by(.id) |
    map({id: .[0].id, count: length, desc: .[0].desc}) |
    sort_by(-.count)')
  STYLE_F=$(echo "$ALL_JSON" | jq '
    [.[] | select(.id | startswith("IDE"))] |
    group_by(.uri) |
    map({file: .[0].uri, diagnostics: ([.[].id] | unique)})')
  ANALYZER_F=$(echo "$ALL_JSON" | jq '
    [.[] | select(.id | startswith("IDE") | not)] |
    group_by(.uri) |
    map({file: .[0].uri, diagnostics: ([.[].id] | unique)})')

  DATA_JS=$(cat <<JSDATA
const styleViolations = ${STYLE_V};

const analyzerViolations = ${ANALYZER_V};

const styleFiles = ${STYLE_F};

const analyzerFiles = ${ANALYZER_F};
JSDATA
)

  sed -e "s|__PROJECT_NAME__|${PROJECT_NAME}|g" \
      -e "/\/\*__DATA__\*\//{
        r /dev/stdin
        d
      }" "$TEMPLATE" <<< "$DATA_JS" > "$OUTPUT"

  TOTAL=$(echo "$ALL_JSON" | jq 'length')
  IDE_COUNT=$(echo "$STYLE_V" | jq '[.[].count] | add // 0')
  ANALYZER_COUNT=$(echo "$ANALYZER_V" | jq '[.[].count] | add // 0')

  echo "Dashboard generated: $OUTPUT"
  echo "  Source:               SARIF (CS* + analyzers; excludes NU*/MSB*)"
  echo "  Total unique:         $TOTAL"
  echo "  Style (IDE*):         $IDE_COUNT"
  echo "  Analyzer (CA/S/CS/…): $ANALYZER_COUNT"
  echo "  SARIF artefacts:      <project>/${SARIF_NAME}"
  exit 0
fi

# Temp dirs for reports
STYLE_DIR="$(mktemp -d)"
ANALYZER_DIR="$(mktemp -d)"
trap 'rm -rf "$STYLE_DIR" "$ANALYZER_DIR"' EXIT

echo "Running dotnet format style..."
dotnet format style --verify-no-changes --severity warn --report "$STYLE_DIR" "$PROJECT" 2>/dev/null || true

echo "Running dotnet format analyzers..."
dotnet format analyzers --verify-no-changes --severity warn --report "$ANALYZER_DIR" "$PROJECT" 2>/dev/null || true

STYLE_REPORT="$STYLE_DIR/format-report.json"
ANALYZER_REPORT="$ANALYZER_DIR/format-report.json"

# Fallback to empty array if no report generated
[[ -f "$STYLE_REPORT" ]] || echo '[]' > "$STYLE_REPORT"
[[ -f "$ANALYZER_REPORT" ]] || echo '[]' > "$ANALYZER_REPORT"

echo "Processing reports..."

# jq filter: extract violations summary {id, count, desc} from format-report.json
# FormatDescription looks like "warning IDE0370: Use coalescing assignment"
read -r -d '' JQ_VIOLATIONS <<'JQ' || true
[
  [.[].FileChanges[] | {DiagnosticId, FormatDescription}]
  | group_by(.DiagnosticId)
  | map({
      id: .[0].DiagnosticId,
      count: length,
      desc: (.[0].FormatDescription | capture("^warning [A-Z0-9]+: (?<d>.+)$") | .d // .[0].FormatDescription)
    })
  | sort_by(-.count)
  | .[]
]
JQ

# jq filter: extract file-level detail [{file, diagnostics}]
# Uses --arg root to strip the project root prefix and normalize separators
read -r -d '' JQ_FILES <<'JQ' || true
[
  [.[] | select(.FileChanges | length > 0) | {FilePath, diagnostics: [.FileChanges[].DiagnosticId] | unique}]
  | group_by(.FilePath)
  | map({
      file: (.[0].FilePath | gsub("\\\\"; "/") | gsub($root + "/"; "")),
      diagnostics: ([.[].diagnostics[]] | unique)
    })
  | .[]
]
JQ

# Generate JS data, making paths relative to project root
# The sed converts backslashes and strips the project root prefix
generate_data() {
  local style_v analyzer_v style_f analyzer_f
  # Convert MSYS /c/... path to C:/... for matching against dotnet output
  local win_root
  win_root="$(cd "$PROJECT_ROOT" && pwd -W 2>/dev/null || echo "$PROJECT_ROOT" | sed 's|^/\([a-zA-Z]\)/|\1:/|')"

  style_v=$(jq "$JQ_VIOLATIONS" "$STYLE_REPORT")
  analyzer_v=$(jq "$JQ_VIOLATIONS" "$ANALYZER_REPORT")

  style_f=$(jq --arg root "$win_root" "$JQ_FILES" "$STYLE_REPORT")
  analyzer_f=$(jq --arg root "$win_root" "$JQ_FILES" "$ANALYZER_REPORT")

  cat <<JSDATA
const styleViolations = ${style_v};

const analyzerViolations = ${analyzer_v};

const styleFiles = ${style_f};

const analyzerFiles = ${analyzer_f};
JSDATA
}

DATA_JS="$(generate_data)"

# Inject data into template
sed -e "s|__PROJECT_NAME__|${PROJECT_NAME}|g" \
    -e "/\/\*__DATA__\*\//{
      r /dev/stdin
      d
    }" "$TEMPLATE" <<< "$DATA_JS" > "$OUTPUT"

echo "Dashboard generated: $OUTPUT"
echo "  Style violations:    $(jq '[.[].FileChanges[].DiagnosticId] | length' "$STYLE_REPORT")"
echo "  Analyzer violations: $(jq '[.[].FileChanges[].DiagnosticId] | length' "$ANALYZER_REPORT")"
