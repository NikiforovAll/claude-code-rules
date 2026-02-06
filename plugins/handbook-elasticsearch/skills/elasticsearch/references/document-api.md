# Document API Reference

## Get Document

```bash
# By ID
es "my-index/_doc/abc123" | jq '._source'

# Specific fields only
es "my-index/_doc/abc123?_source_includes=timestamp,message"
```

## Index (Create/Replace) Document

```bash
# With specific ID (PUT = create or replace)
es "my-index/_doc/abc123" -XPUT -d '{
  "timestamp": "2026-02-01T12:00:00Z",
  "message": "Hello from Nox",
  "level": "info"
}'

# Auto-generate ID (POST)
es "my-index/_doc" -XPOST -d '{
  "timestamp": "2026-02-01T12:00:00Z",
  "message": "Auto-ID document"
}'
```

## Update Document

**Partial update** (merge fields):
```bash
es "my-index/_update/abc123" -XPOST -d '{
  "doc": {
    "level": "warn",
    "updated_at": "2026-02-01T13:00:00Z"
  }
}'
```

**Script update** (computed values):
```bash
es "my-index/_update/abc123" -XPOST -d '{
  "script": {
    "source": "ctx._source.retry_count += 1",
    "lang": "painless"
  }
}'
```

**Upsert** (create if missing, update if exists):
```bash
es "my-index/_update/abc123" -XPOST -d '{
  "doc": {"counter": 1},
  "upsert": {"counter": 1, "created": "2026-02-01T12:00:00Z"}
}'
```

## Delete Document

```bash
es "my-index/_doc/abc123" -XDELETE
```

## Delete by Query

```bash
es "my-index/_delete_by_query" -XPOST -d '{
  "query": {
    "range": {"@timestamp": {"lt": "now-90d"}}
  }
}'
```

## Update by Query

```bash
es "my-index/_update_by_query" -XPOST -d '{
  "query": {"term": {"status": "pending"}},
  "script": {
    "source": "ctx._source.status = \"expired\"",
    "lang": "painless"
  }
}'
```

## Multi-Get

```bash
es "_mget" -XPOST -d '{
  "docs": [
    {"_index": "my-index", "_id": "abc123"},
    {"_index": "my-index", "_id": "def456"}
  ]
}'
```

## Bulk API

The most efficient way to index many documents. Uses NDJSON format (newline-delimited JSON).

```bash
es "_bulk" -XPOST -H "Content-Type: application/x-ndjson" -d '
{"index": {"_index": "my-index", "_id": "1"}}
{"timestamp": "2026-02-01T12:00:00Z", "message": "first"}
{"index": {"_index": "my-index", "_id": "2"}}
{"timestamp": "2026-02-01T12:01:00Z", "message": "second"}
{"delete": {"_index": "my-index", "_id": "old-doc"}}
'
```

**Bulk from file**:
```bash
es "_bulk" -XPOST -H "Content-Type: application/x-ndjson" --data-binary @bulk-data.ndjson
```

**Performance tips**:
- Optimal bulk size: 5-15 MB per request
- Use `_bulk` instead of individual requests for >10 documents
- Check response for `errors: true` and inspect individual item statuses
