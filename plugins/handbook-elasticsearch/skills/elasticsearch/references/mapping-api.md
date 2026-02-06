# Mapping & Template API Reference

## Get Mapping

```bash
# Full mapping
es "my-index/_mapping" | jq '.[]|.mappings.properties'

# Specific field
es "my-index/_mapping/field/message" | jq .
```

## Put Mapping (Add Fields)

Mappings can only be extended, not changed for existing fields. To change a field type, reindex.

```bash
es "my-index/_mapping" -XPUT -d '{
  "properties": {
    "new_field": {"type": "keyword"},
    "location": {"type": "geo_point"}
  }
}'
```

## Common Field Types

| Type | Use for | Notes |
|------|---------|-------|
| `text` | Full-text search | Analyzed, not aggregatable |
| `keyword` | Exact values, filtering, aggregations | Not analyzed, max 256 chars default |
| `long`/`integer`/`short`/`byte` | Whole numbers | Pick smallest that fits |
| `float`/`double`/`half_float`/`scaled_float` | Decimals | `scaled_float` for money |
| `date` | Timestamps | Supports multiple formats |
| `boolean` | true/false | |
| `ip` | IPv4/IPv6 addresses | Supports CIDR queries |
| `geo_point` | Lat/lon coordinates | For geo queries |
| `nested` | Arrays of objects | Preserves object boundaries |
| `object` | JSON objects | Flattened by default |
| `flattened` | Arbitrary JSON | Single field, keyword-like queries |

## Multi-fields

Map a single field multiple ways:

```json
{
  "properties": {
    "title": {
      "type": "text",
      "fields": {
        "keyword": {"type": "keyword"},
        "autocomplete": {
          "type": "text",
          "analyzer": "autocomplete_analyzer"
        }
      }
    }
  }
}
```

Search with `title` (full-text), aggregate with `title.keyword` (exact), suggest with `title.autocomplete`.

## Dynamic Mapping

Control how new fields are handled:

```json
{
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "known_field": {"type": "text"}
    }
  }
}
```

Values: `true` (auto-map, default), `runtime` (map as runtime fields), `false` (ignore in mapping, still stored), `strict` (reject unknown fields).

## Dynamic Templates

Auto-map fields by pattern:

```json
{
  "mappings": {
    "dynamic_templates": [
      {
        "strings_as_keywords": {
          "match_mapping_type": "string",
          "mapping": {"type": "keyword"}
        }
      },
      {
        "labels_as_keywords": {
          "path_match": "labels.*",
          "mapping": {"type": "keyword"}
        }
      }
    ]
  }
}
```

## Index Templates

Apply settings/mappings to new indices matching a pattern:

```bash
# Create index template
es "_index_template/logs-template" -XPUT -d '{
  "index_patterns": ["logs-*"],
  "priority": 100,
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "@timestamp": {"type": "date"},
        "message": {"type": "text"},
        "level": {"type": "keyword"}
      }
    }
  }
}'

# List templates
es "_index_template" | jq '.index_templates[].name'

# Get specific template
es "_index_template/logs-template"

# Delete template
es "_index_template/logs-template" -XDELETE
```

## Component Templates

Reusable template building blocks:

```bash
es "_component_template/base-mappings" -XPUT -d '{
  "template": {
    "mappings": {
      "properties": {
        "@timestamp": {"type": "date"},
        "host.name": {"type": "keyword"}
      }
    }
  }
}'

# Use in index template
es "_index_template/my-template" -XPUT -d '{
  "index_patterns": ["my-*"],
  "composed_of": ["base-mappings"],
  "priority": 200
}'
```

## Runtime Fields

Define fields at query time (no reindex needed):

```bash
es "my-index/_search" -d '{
  "runtime_mappings": {
    "day_of_week": {
      "type": "keyword",
      "script": "emit(doc[\"@timestamp\"].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ROOT))"
    }
  },
  "query": {"term": {"day_of_week": "Monday"}}
}'
```
