# Kibana API Reference

Kibana has its own REST API, separate from Elasticsearch. Use `$KIBANA_URL` (not `$ES_URL`).

## Authentication

```bash
# Set Kibana URL (typically .kb. domain, vs .es. for Elasticsearch)
KIBANA_URL="https://your-deployment.kb.us-east-1.aws.elastic.cloud"

# All Kibana mutations require kbn-xsrf header
curl -s "$KIBANA_URL/<endpoint>" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '<json-body>'
```

**Key differences from ES API:**
- `kbn-xsrf: true` header required on all POST/PUT/DELETE requests
- Same API key works for both ES and Kibana
- URL pattern: replace `.es.` with `.kb.` from your ES URL

## Health Check

```bash
curl -s "$KIBANA_URL/api/status" \
  -H "Authorization: ApiKey $ES_API_KEY" | jq '{name: .name, status: .status.overall.level, version: .version.number}'
```

## Spaces

Kibana spaces scope dashboards, saved objects, and data views. Prefix API paths with `/s/{spaceId}` for non-default spaces:

```bash
# Default space — no prefix
curl -s "$KIBANA_URL/api/data_views" -H "Authorization: ApiKey $ES_API_KEY"

# Custom space
curl -s "$KIBANA_URL/s/my-space/api/data_views" -H "Authorization: ApiKey $ES_API_KEY"
```

## Data Views

Data views (formerly index patterns) tell Kibana which indices to query.

```bash
# List data views
curl -s "$KIBANA_URL/api/data_views" \
  -H "Authorization: ApiKey $ES_API_KEY" | jq '.data_view[] | {id, title}'

# Create data view
curl -s -X POST "$KIBANA_URL/api/data_views/data_view" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
    "data_view": {
      "id": "my-logs-view",
      "title": "logs-*",
      "timeFieldName": "@timestamp"
    },
    "override": true
  }'

# Delete data view
curl -s -X DELETE "$KIBANA_URL/api/data_views/data_view/my-logs-view" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "kbn-xsrf: true"
```

**`override: true`** — overwrites if a data view with that ID already exists. Useful for idempotent scripts.

## Saved Objects

Saved objects are Kibana's storage model — dashboards, visualizations, data views, searches, etc.

```bash
# Get a saved object — NOT available on serverless
curl -s "$KIBANA_URL/api/saved_objects/dashboard/my-dashboard-id" \
  -H "Authorization: ApiKey $ES_API_KEY" | jq .

# Find saved objects by type — NOT available on serverless
curl -s "$KIBANA_URL/api/saved_objects/_find?type=dashboard&per_page=100" \
  -H "Authorization: ApiKey $ES_API_KEY" | jq '.saved_objects[] | {id, title: .attributes.title}'

# Bulk create (with overwrite) — NOT available on serverless
curl -s -X POST "$KIBANA_URL/api/saved_objects/_bulk_create?overwrite=true" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "type": "dashboard",
      "id": "my-dashboard",
      "attributes": { "title": "My Dashboard" }
    }
  ]'

# Delete saved object — NOT available on serverless
curl -s -X DELETE "$KIBANA_URL/api/saved_objects/dashboard/my-dashboard-id" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "kbn-xsrf: true"
```

Saved object types: `dashboard`, `visualization`, `lens`, `search`, `index-pattern`, `map`, `tag`.

**Serverless Kibana:** On Elastic Cloud Serverless, only `_import` and `_export` are available for saved objects. The `_find`, `_bulk_create`, individual GET, and DELETE endpoints all return `400 Bad Request`. Use `_import?overwrite=true` for create/update operations.

## Dashboard Import / Export

```bash
# Export dashboard (includes dependencies)
curl -s -X POST "$KIBANA_URL/api/saved_objects/_export" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
    "objects": [{"type": "dashboard", "id": "my-dashboard-id"}],
    "includeReferencesDeep": true
  }' > dashboard-export.ndjson

# Import dashboard (NDJSON format, overwrite existing)
curl -s -X POST "$KIBANA_URL/api/saved_objects/_import?overwrite=true" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "kbn-xsrf: true" \
  --form file=@dashboard-export.ndjson
```

**Import format** is newline-delimited JSON (NDJSON) — one saved object per line.

## Programmatic Dashboard Creation

For Elastic Cloud Serverless and portability, use **by-value** dashboards where visualizations are embedded inline (no separate saved objects needed).

### Dashboard Structure

```json
{
  "type": "dashboard",
  "id": "my-dashboard",
  "coreMigrationVersion": "8.8.0",
  "typeMigrationVersion": "10.3.0",
  "attributes": {
    "title": "My Dashboard",
    "description": "Dashboard description",
    "timeRestore": true,
    "timeTo": "now",
    "timeFrom": "now-24h",
    "refreshInterval": {"pause": false, "value": 30000},
    "panelsJSON": "[...panels array as JSON string...]",
    "optionsJSON": "{\"useMargins\":true,\"syncColors\":false}"
  },
  "references": []
}
```

**Critical:** `coreMigrationVersion` and `typeMigrationVersion` are **required** for serverless Kibana imports. Without them, the import returns a 500 Internal Server Error. Include them on all saved objects in NDJSON payloads.

### Panel Format (By-Value)

Each panel in `panelsJSON` has grid position and an embedded visualization:

```json
{
  "type": "lens",
  "gridData": {"x": 0, "y": 0, "w": 12, "h": 8, "i": "panel-1"},
  "panelIndex": "panel-1",
  "embeddableConfig": {
    "attributes": {
      "visualizationType": "lnsMetric",
      "title": "Total Events",
      "state": {
        "filters": [],
        "query": {"query": "", "language": "kuery"},
        "datasourceStates": {
          "formBased": {
            "layers": {
              "layer1": {
                "columns": {
                  "col1": {
                    "operationType": "count",
                    "label": "Count",
                    "dataType": "number",
                    "isBucketed": false,
                    "sourceField": "___records___"
                  }
                },
                "columnOrder": ["col1"]
              }
            }
          }
        },
        "visualization": {
          "layerId": "layer1",
          "layerType": "data",
          "metricAccessor": "col1"
        }
      },
      "references": [
        {"type": "index-pattern", "id": "my-data-view", "name": "indexpattern-datasource-layer-layer1"}
      ]
    }
  }
}
```

Grid uses a 48-column layout. Common panel sizes: metric `w:12 h:7`, chart `w:24 h:14`, table `w:48 h:12`.

**Layer properties:** Each layer in `datasourceStates.formBased.layers` should include:
- `"indexPatternId": "data-view-id"` — links the layer to its data view
- `"incompleteColumns": {}` — required empty object
- `"columns"` and `"columnOrder"` — the column definitions

### Lens Visualization Types

| Type | `visualizationType` | Use Case |
|------|---------------------|----------|
| Metric | `lnsMetric` | Single number KPI |
| XY Chart | `lnsXY` | Line, bar, area charts |
| Pie / Donut | `lnsPie` | Proportion breakdown |
| Data Table | `lnsDatatable` | Tabular drill-down |

### Column Operation Types

| Operation | Description | `isBucketed` | `sourceField` | `scale` |
|-----------|-------------|--------------|---------------|---------|
| `count` | Document count | false | `"___records___"` (required!) | `"ratio"` |
| `unique_count` | Cardinality | false | field name | `"ratio"` |
| `sum`, `avg`, `min`, `max` | Metric aggregations | false | field name | `"ratio"` (see TSDB caveat) |
| `terms` | Top values grouping | true | field name | `"ordinal"` |
| `date_histogram` | Time buckets | true | field name | `"interval"` |
| `filters` | Custom filter groups | true | — | `"ordinal"` |

**Critical:**
- `count` columns **must** include `"sourceField": "___records___"`. Without it, Kibana throws `aggValueCount requires the "field" argument`.
- All columns **should** include `"scale"` for XY charts. Without it, XY charts may silently render empty despite correct configuration. Use `"interval"` for date_histogram, `"ordinal"` for terms/filters, `"ratio"` for metrics.
- **TSDB gauge metrics** (e.g., `metrics.system.memory.utilization`, `metrics.system.cpu.utilization`) with `time_series_metric: gauge` in their mapping **cannot** be aggregated via `avg`/`sum`/`min`/`max` in programmatic Lens panels — the chart renders blank with no error. Use `count`-based panels for TSDB data instead, or view these metrics through Kibana's built-in Infrastructure/Metrics Explorer UI.

### Column with Filter

```json
{
  "col1": {
    "operationType": "count",
    "label": "Error Count",
    "dataType": "number",
    "isBucketed": false,
    "filter": {
      "query": "attributes.event.category: \"user.error\"",
      "language": "kuery"
    }
  }
}
```

### XY Chart Visualization Config

**Critical:** XY charts require a `layers` array wrapper, `preferredSeriesType`, `legend`, and `fittingFunction` at the top level. Without the `layers` array, charts render empty with no error. Without `legend`/`fittingFunction`, charts may also silently fail to render.

```json
{
  "visualization": {
    "preferredSeriesType": "area_stacked",
    "legend": {"isVisible": true, "position": "right"},
    "fittingFunction": "None",
    "layers": [
      {
        "layerId": "layer1",
        "layerType": "data",
        "seriesType": "area_stacked",
        "xAccessor": "col-date",
        "accessors": ["col-count"],
        "splitAccessor": "col-category"
      }
    ]
  }
}
```

Series types: `line`, `bar`, `bar_stacked`, `area`, `area_stacked`, `bar_horizontal`, `bar_horizontal_stacked`.

## Control Groups (Dashboard Filters)

Add interactive filter controls to dashboards:

```json
{
  "controlGroupInput": {
    "controlStyle": "oneLine",
    "chainingSystem": "HIERARCHICAL",
    "panelsJSON": {
      "panel-filter-1": {
        "order": 0,
        "width": "medium",
        "type": "optionsListControl",
        "explicitInput": {
          "id": "panel-filter-1",
          "fieldName": "attributes.user.id",
          "title": "User",
          "dataViewId": "my-data-view"
        }
      }
    }
  }
}
```

## Deploy Dashboard (Full Example)

```bash
# Generate NDJSON with data view + dashboard
# NOTE: coreMigrationVersion + typeMigrationVersion are required for serverless
cat > /tmp/dashboard.ndjson << 'EOF'
{"type":"index-pattern","id":"my-logs","coreMigrationVersion":"8.8.0","attributes":{"title":"logs-*","timeFieldName":"@timestamp"}}
{"type":"dashboard","id":"my-dashboard","coreMigrationVersion":"8.8.0","typeMigrationVersion":"10.3.0","attributes":{"title":"My Dashboard","timeRestore":true,"timeFrom":"now-24h","timeTo":"now","panelsJSON":"[{\"type\":\"lens\",\"gridData\":{\"x\":0,\"y\":0,\"w\":48,\"h\":8,\"i\":\"p1\"},\"panelIndex\":\"p1\",\"embeddableConfig\":{\"attributes\":{\"visualizationType\":\"lnsMetric\",\"title\":\"Total Docs\",\"state\":{\"filters\":[],\"query\":{\"query\":\"\",\"language\":\"kuery\"},\"datasourceStates\":{\"formBased\":{\"layers\":{\"l1\":{\"columns\":{\"c1\":{\"operationType\":\"count\",\"label\":\"Count\",\"dataType\":\"number\",\"isBucketed\":false}},\"columnOrder\":[\"c1\"]}}}},\"visualization\":{\"layerId\":\"l1\",\"layerType\":\"data\",\"metricAccessor\":\"c1\"}},\"references\":[{\"type\":\"index-pattern\",\"id\":\"my-logs\",\"name\":\"indexpattern-datasource-layer-l1\"}]}}}]"},"references":[]}
EOF

# Import to Kibana
curl -s -X POST "$KIBANA_URL/api/saved_objects/_import?overwrite=true" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "kbn-xsrf: true" \
  --form file=@/tmp/dashboard.ndjson | jq .
```

For complex dashboards with many panels, use a Python script to generate the NDJSON rather than hand-crafting the JSON strings. See the `panelsJSON` nesting: it's a JSON string containing an array of panel objects, each with deeply nested Lens state. Errors in this structure cause silent 500 errors on import.

## Alerting Rules

```bash
# List rules
curl -s "$KIBANA_URL/api/alerting/rules/_find?per_page=100" \
  -H "Authorization: ApiKey $ES_API_KEY" | jq '.data[] | {id, name: .name, enabled: .enabled}'

# Disable a rule
curl -s -X POST "$KIBANA_URL/api/alerting/rule/{rule_id}/_disable" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "kbn-xsrf: true"

# Enable a rule
curl -s -X POST "$KIBANA_URL/api/alerting/rule/{rule_id}/_enable" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "kbn-xsrf: true"
```

## Tips

- **`kbn-xsrf: true`** is required on every write operation — Kibana returns 400 without it.
- **By-value dashboards** embed visualizations inline — no separate saved object IDs to manage. Required for Elastic Cloud Serverless.
- **NDJSON import** is the most reliable way to deploy dashboards programmatically.
- **Data view IDs** must match between visualization references and actual data views — mismatches cause "field not found" errors.
- **Space prefix** `/s/{spaceId}/api` — omit for the default space.
- **Derive Kibana URL from ES URL** — swap `.es.` for `.kb.` in the hostname.
