# OpenTelemetry Data in Elasticsearch

OTEL data ingested via the managed OTLP endpoint lands in standard index patterns. This reference covers querying OTEL logs, traces, and metrics.

## Index Patterns

| Signal | Default Index | Contains |
|--------|---------------|----------|
| Logs | `logs-generic.otel-default` | Application logs, custom events |
| Traces | `traces-generic.otel-default` | Spans and transactions |
| Metrics | `metrics-generic.otel-default` | Numeric measurements |

These indices are created automatically when data arrives via the OTLP endpoint.

## Field Structure

OTEL data maps to Elastic fields with a consistent structure:

```
@timestamp                          # Event timestamp
resource.attributes.service.name    # Service that emitted the signal
resource.attributes.*               # Resource-level attributes (deployment, host, etc.)
attributes.*                        # Signal-specific attributes
```

### Log Fields

```
body                                # Log message / event name
severityNumber                      # Numeric severity (1-24)
severityText                        # INFO, WARN, ERROR, etc.
attributes.*                        # Custom attributes set on the log
resource.attributes.service.name    # Originating service
traceId                             # Trace correlation (if emitted within a span)
spanId                              # Span correlation (if emitted within a span)
```

### Trace Fields (APM)

In Elastic APM, OTEL spans become:
- **Transaction** = root span (no parent) — the entry point
- **Span** = child span (has a parent) — operations within a transaction

```
trace.id                            # Links all spans in a distributed trace
span.id                             # This span's unique ID
parent.id                           # Parent span ID (empty for root/transaction)
span.name                           # Operation name
span.duration.us                    # Duration in microseconds
span.type                           # Span type (custom, db, http, etc.)
service.name                        # Service that emitted the span
```

## Querying OTEL Logs

### ES|QL

```bash
# All logs from a service
curl -s -X POST "$ES_URL/_query" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM logs-generic.otel-default | WHERE resource.attributes.service.name == \"my-app\" | SORT @timestamp DESC | LIMIT 50"
  }' | jq .

# Events by category
curl -s -X POST "$ES_URL/_query" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM logs-generic.otel-default | WHERE attributes.event.category == \"user.interaction\" | STATS count = COUNT(*) BY attributes.event.action | SORT count DESC"
  }' | jq .

# Errors in the last hour
curl -s -X POST "$ES_URL/_query" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM logs-generic.otel-default | WHERE severityText == \"ERROR\" AND @timestamp > NOW() - 1 hour | SORT @timestamp DESC | LIMIT 20"
  }' | jq .
```

### Query DSL

```bash
# Filter logs by custom attribute
curl -s "$ES_URL/logs-generic.otel-default/_search" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "bool": {
        "filter": [
          {"term": {"resource.attributes.service.name": "my-app"}},
          {"range": {"@timestamp": {"gte": "now-1h"}}}
        ]
      }
    },
    "sort": [{"@timestamp": {"order": "desc"}}],
    "size": 20
  }' | jq '.hits.hits[]._source'

# Full-text search on log body
curl -s "$ES_URL/logs-generic.otel-default/_search" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "bool": {
        "must": [{"match": {"body": "error timeout"}}],
        "filter": [{"range": {"@timestamp": {"gte": "now-24h"}}}]
      }
    },
    "size": 20
  }' | jq '.hits.hits[]._source'
```

## Querying OTEL Traces

### ES|QL

```bash
# Slowest transactions for a service
curl -s -X POST "$ES_URL/_query" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM traces-generic.otel-default | WHERE service.name == \"my-app\" AND parent.id IS NULL | SORT span.duration.us DESC | LIMIT 10"
  }' | jq .

# All spans in a trace (distributed trace view)
curl -s -X POST "$ES_URL/_query" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM traces-generic.otel-default | WHERE trace.id == \"abc123def456\" | SORT @timestamp ASC"
  }' | jq .

# Error rate by service
curl -s -X POST "$ES_URL/_query" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM traces-generic.otel-default | WHERE parent.id IS NULL | STATS total = COUNT(*), errors = COUNT_IF(event.outcome == \"failure\") BY service.name | EVAL error_rate = errors / total | SORT error_rate DESC"
  }' | jq .
```

### Query DSL

```bash
# Find transactions (root spans) for a service
curl -s "$ES_URL/traces-generic.otel-default/_search" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "bool": {
        "must": [{"term": {"service.name": "my-app"}}],
        "must_not": [{"exists": {"field": "parent.id"}}],
        "filter": [{"range": {"@timestamp": {"gte": "now-1h"}}}]
      }
    },
    "sort": [{"span.duration.us": {"order": "desc"}}],
    "size": 10
  }' | jq '.hits.hits[] | {name: ._source.span.name, duration_ms: (._source.span.duration.us / 1000), trace_id: ._source.trace.id}'
```

## Trace-Log Correlation

Logs emitted within an active trace context automatically include `traceId` and `spanId`. Use these to correlate:

```bash
# Step 1: Find a slow trace
curl -s -X POST "$ES_URL/_query" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM traces-generic.otel-default | WHERE service.name == \"my-app\" AND span.duration.us > 5000000 | KEEP trace.id, span.name, span.duration.us | LIMIT 5"
  }' | jq .

# Step 2: Get all logs for that trace
curl -s -X POST "$ES_URL/_query" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM logs-generic.otel-default | WHERE traceId == \"abc123def456\" | SORT @timestamp ASC"
  }' | jq .

# Step 3: Get all spans for the same trace
curl -s -X POST "$ES_URL/_query" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM traces-generic.otel-default | WHERE trace.id == \"abc123def456\" | SORT @timestamp ASC | KEEP span.name, span.duration.us, parent.id"
  }' | jq .
```

## Aggregations on OTEL Data

```bash
# Log volume by service over time
curl -s "$ES_URL/logs-generic.otel-default/_search?size=0" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {"range": {"@timestamp": {"gte": "now-24h"}}},
    "aggs": {
      "over_time": {
        "date_histogram": {"field": "@timestamp", "fixed_interval": "1h"},
        "aggs": {
          "by_service": {
            "terms": {"field": "resource.attributes.service.name", "size": 10}
          }
        }
      }
    }
  }' | jq '.aggregations'

# Average span duration by operation
curl -s "$ES_URL/traces-generic.otel-default/_search?size=0" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "bool": {
        "filter": [
          {"term": {"service.name": "my-app"}},
          {"range": {"@timestamp": {"gte": "now-1h"}}}
        ]
      }
    },
    "aggs": {
      "by_operation": {
        "terms": {"field": "span.name", "size": 20},
        "aggs": {
          "avg_duration_ms": {"avg": {"field": "span.duration.us"}},
          "p99_duration": {"percentiles": {"field": "span.duration.us", "percents": [99]}}
        }
      }
    }
  }' | jq '.aggregations'

# Unique users per service (custom attribute)
curl -s "$ES_URL/logs-generic.otel-default/_search?size=0" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "aggs": {
      "by_service": {
        "terms": {"field": "resource.attributes.service.name", "size": 10},
        "aggs": {
          "unique_users": {"cardinality": {"field": "attributes.user.id"}}
        }
      }
    }
  }' | jq '.aggregations'
```

## KQL Patterns for Discover

Common KQL queries for the Kibana Discover tab:

```
# All events from a service
resource.attributes.service.name: "my-app"

# Error logs
severityText: "ERROR"

# Custom attribute filtering
attributes.user.id: "david"

# Exists check (has frustration data)
attributes.frustration.type: *

# Combine filters
resource.attributes.service.name: "my-app" AND severityText: "ERROR" AND @timestamp >= now-1h
```

## OTLP Endpoint Setup

Elastic Cloud provides a managed OTLP endpoint (no APM Server needed):

```bash
# Endpoint (from Kibana: Add data → Applications → OpenTelemetry)
OTEL_EXPORTER_OTLP_ENDPOINT="https://your-otlp-endpoint.elastic.cloud:443"

# Authentication
OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey YOUR_BASE64_KEY"

# Service identity
OTEL_RESOURCE_ATTRIBUTES="service.name=my-app,deployment.environment=production"
```

The OTLP endpoint accepts:
- `POST /v1/logs` — log signals
- `POST /v1/traces` — trace signals
- `POST /v1/metrics` — metric signals

## Tips

- **OTEL attributes are nested** — query `attributes.my.field`, not `my.field`. Check mappings if unsure.
- **`resource.attributes`** vs **`attributes`** — resource attributes describe the source (service, host), signal attributes describe the event.
- **Trace correlation** — `traceId` on logs links to `trace.id` on traces. Note the different field names.
- **Transactions vs spans** — root spans (no `parent.id`) become Elastic APM transactions. Filter with `parent.id IS NULL` or `NOT exists parent.id`.
- **Duration is in microseconds** — `span.duration.us`. Divide by 1000 for milliseconds.
- **Data streams** — OTEL indices are data streams. Use `_data_stream/logs-generic.otel-default` to check health.
- **Field type conflicts** — if the same attribute has different types across services, Elasticsearch may reject documents. Use consistent types.
