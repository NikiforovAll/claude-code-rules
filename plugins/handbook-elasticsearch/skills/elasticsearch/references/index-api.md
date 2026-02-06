# Index Management API Reference

## Create Index

```bash
es "my-new-index" -XPUT -d '{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "timestamp": {"type": "date"},
      "message": {"type": "text"},
      "level": {"type": "keyword"},
      "duration_ms": {"type": "float"}
    }
  }
}'
```

## Delete Index

```bash
es "my-old-index" -XDELETE
```

**With wildcard** (dangerous — requires `action.destructive_requires_name: false`):
```bash
es "temp-*" -XDELETE
```

## Index Settings

**Get settings**:
```bash
es "my-index/_settings" | jq '.[]|.settings.index'
```

**Update settings** (dynamic only):
```bash
es "my-index/_settings" -XPUT -d '{
  "index": {
    "number_of_replicas": 2,
    "refresh_interval": "30s"
  }
}'
```

Common dynamic settings: `number_of_replicas`, `refresh_interval`, `max_result_window`, `routing.allocation.require.*`

## List Indices

```bash
# Human-readable, sorted by size
es "_cat/indices?v&s=store.size:desc&h=index,health,status,docs.count,store.size"

# JSON format
es "_cat/indices?format=json&s=store.size:desc" | jq '.[] | {index: .index, docs: .["docs.count"], size: .["store.size"]}'

# Filter by pattern
es "_cat/indices/logs-*?v&s=store.size:desc"
```

## Open / Close

Closed indices consume no resources but can't be searched.

```bash
es "my-index/_close" -XPOST
es "my-index/_open" -XPOST
```

## Reindex

Copy data between indices (useful for mapping changes):

```bash
es "_reindex" -XPOST -d '{
  "source": {"index": "old-index"},
  "dest": {"index": "new-index"}
}'
```

**With query filter**:
```bash
es "_reindex" -XPOST -d '{
  "source": {
    "index": "logs-*",
    "query": {"range": {"@timestamp": {"gte": "2026-01-01"}}}
  },
  "dest": {"index": "logs-2026"}
}'
```

**Remote reindex** (cross-cluster):
```bash
es "_reindex" -XPOST -d '{
  "source": {
    "remote": {"host": "https://other-cluster:9200"},
    "index": "source-index"
  },
  "dest": {"index": "dest-index"}
}'
```

## Aliases

```bash
# List aliases
es "_cat/aliases?v"

# Create alias
es "_aliases" -XPOST -d '{
  "actions": [
    {"add": {"index": "logs-2026.02", "alias": "logs-current"}}
  ]
}'

# Swap alias atomically
es "_aliases" -XPOST -d '{
  "actions": [
    {"remove": {"index": "logs-2026.01", "alias": "logs-current"}},
    {"add": {"index": "logs-2026.02", "alias": "logs-current"}}
  ]
}'
```

## Index Lifecycle Management (ILM)

```bash
# Get ILM policy
es "_ilm/policy/my-policy"

# Get ILM status for index
es "my-index/_ilm/explain"

# Retry failed ILM step
es "my-index/_ilm/retry" -XPOST
```

## Shrink / Split

```bash
# Shrink (reduce shard count — index must be read-only first)
es "my-index/_settings" -XPUT -d '{"index.blocks.write": true}'
es "my-index/_shrink/my-index-shrunk" -XPOST -d '{"settings": {"index.number_of_shards": 1}}'

# Split (increase shard count)
es "my-index/_split/my-index-split" -XPOST -d '{"settings": {"index.number_of_shards": 4}}'
```

## Rollover

```bash
es "logs-current/_rollover" -XPOST -d '{
  "conditions": {
    "max_age": "7d",
    "max_size": "50gb",
    "max_docs": 10000000
  }
}'
```

## Index Stats

```bash
# All stats
es "my-index/_stats" | jq '.indices["my-index"].total'

# Specific metrics
es "my-index/_stats/docs,store,indexing,search"
```
