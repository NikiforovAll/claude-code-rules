# Search API Reference

## Query DSL

The primary search endpoint. Supports GET and POST with a JSON body.

```bash
# Basic search
es "my-index/_search" -d '{
  "query": {
    "bool": {
      "must": [
        {"match": {"message": "error"}}
      ],
      "filter": [
        {"range": {"@timestamp": {"gte": "now-1h"}}}
      ]
    }
  },
  "size": 20,
  "sort": [{"@timestamp": {"order": "desc"}}]
}'
```

### Common Query Types

**match** — full-text search (analyzed):
```json
{"query": {"match": {"message": "connection timeout"}}}
```

**term** — exact value match (not analyzed, use for keywords/enums):
```json
{"query": {"term": {"status.keyword": "error"}}}
```

**bool** — combine queries:
```json
{"query": {"bool": {
  "must": [...],      // AND — contributes to score
  "filter": [...],    // AND — no scoring, faster
  "should": [...],    // OR — at least one if no must
  "must_not": [...]   // NOT — excludes
}}}
```

**range** — numeric/date ranges:
```json
{"query": {"range": {"@timestamp": {"gte": "now-24h", "lte": "now"}}}}
```

**wildcard** — pattern matching (use sparingly, slow):
```json
{"query": {"wildcard": {"host.keyword": "prod-web-*"}}}
```

**exists** — field exists:
```json
{"query": {"exists": {"field": "error.stack_trace"}}}
```

**multi_match** — search across multiple fields:
```json
{"query": {"multi_match": {"query": "timeout", "fields": ["message", "error.message", "log.message"]}}}
```

**query_string** — Lucene syntax (powerful, user-facing):
```json
{"query": {"query_string": {"query": "status:error AND service:api-gateway"}}}
```

### Sorting

```json
{
  "sort": [
    {"@timestamp": {"order": "desc"}},
    {"_score": {"order": "desc"}}
  ]
}
```

### Highlighting

```json
{
  "query": {"match": {"message": "error"}},
  "highlight": {
    "fields": {"message": {}},
    "pre_tags": [">>"],
    "post_tags": ["<<"]
  }
}
```

### Pagination

**Basic** (up to 10,000 hits):
```json
{"from": 0, "size": 20}
```

**search_after** (for deep pagination):
```json
{
  "size": 20,
  "sort": [{"@timestamp": "desc"}, {"_id": "asc"}],
  "search_after": ["2026-01-31T10:00:00.000Z", "doc-id-123"]
}
```

**Point-in-time + search_after** (consistent pagination):
```bash
# Open PIT
PIT=$(es "_pit" -d '{"index":"my-index","keep_alive":"5m"}' | jq -r '.id')

# Search with PIT
es "_search" -d "{\"pit\":{\"id\":\"$PIT\",\"keep_alive\":\"5m\"},\"size\":100,\"sort\":[{\"@timestamp\":\"desc\"}]}"
```

### Count

```bash
es "my-index/_count" -d '{"query": {"range": {"@timestamp": {"gte": "now-1h"}}}}'
```

## ES|QL (Elasticsearch Query Language)

Pipe-based query language. Simpler than DSL for analytics.

```bash
es "_query" -d '{
  "query": "FROM logs-* | WHERE @timestamp > NOW() - 1 hour AND level == \"error\" | STATS count = COUNT(*) BY service.name | SORT count DESC | LIMIT 10"
}'
```

### ES|QL Patterns

```sql
-- Top error-producing services in the last hour
FROM logs-*
| WHERE @timestamp > NOW() - 1 hour AND level == "error"
| STATS error_count = COUNT(*) BY service.name
| SORT error_count DESC
| LIMIT 10

-- P99 latency by endpoint
FROM traces-*
| WHERE @timestamp > NOW() - 24 hours
| STATS p99 = PERCENTILE(duration, 99), avg = AVG(duration) BY url.path
| WHERE p99 > 1000
| SORT p99 DESC

-- Unique users per day
FROM logs-*
| WHERE @timestamp > NOW() - 7 days
| EVAL day = DATE_TRUNC(1 day, @timestamp)
| STATS unique_users = COUNT_DISTINCT(user.id) BY day
| SORT day
```

## EQL (Event Query Language)

Sequence-based queries for event correlation:

```bash
es "logs-*/_eql/search" -d '{
  "query": "sequence by host.name [process where event.type == \"start\" and process.name == \"cmd.exe\"] [file where event.type == \"creation\"]",
  "size": 10
}'
```
