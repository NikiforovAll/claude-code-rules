# Query DSL Reference

Full reference for Elasticsearch Query DSL query types. All examples assume `ES_URL` and `ES_API_KEY` are set.

## Table of Contents

- [Full-Text Queries](#full-text-queries)
- [Term-Level Queries](#term-level-queries)
- [Compound Queries](#compound-queries)
- [Nested & Join Queries](#nested--join-queries)
- [Geo Queries](#geo-queries)
- [Special Queries](#special-queries)
- [Search Features](#search-features)

## Full-Text Queries

### match

Analyzes the query string and finds documents with matching terms:

```json
{ "query": { "match": { "message": { "query": "error timeout", "operator": "and" } } } }
```

- Default operator is `or` (any term matches)
- Use `"operator": "and"` to require all terms
- `"fuzziness": "AUTO"` enables typo tolerance

### multi_match

Search across multiple fields:

```json
{
  "query": {
    "multi_match": {
      "query": "connection refused",
      "fields": ["message", "error.message", "log.original"],
      "type": "best_fields"
    }
  }
}
```

Types: `best_fields` (default), `most_fields`, `cross_fields`, `phrase`, `phrase_prefix`

### match_phrase

Matches exact phrase in order:

```json
{ "query": { "match_phrase": { "message": "connection refused" } } }
```

### match_phrase_prefix

Like match_phrase but last term is a prefix (autocomplete):

```json
{ "query": { "match_phrase_prefix": { "message": "connect" } } }
```

### query_string

Lucene syntax — powerful but can throw parse errors on bad input:

```json
{ "query": { "query_string": { "query": "message:error AND level:critical", "default_field": "message" } } }
```

### simple_query_string

Safer version — never throws parse errors, ignores invalid syntax:

```json
{ "query": { "simple_query_string": { "query": "error + timeout -debug", "fields": ["message"] } } }
```

Operators: `+` (AND), `|` (OR), `-` (NOT), `"..."` (phrase), `*` (prefix), `(...)` (precedence)

## Term-Level Queries

These operate on exact values (no analysis). Use on `keyword`, `numeric`, `date`, `boolean` fields.

### term

Exact match on a single value:

```json
{ "query": { "term": { "level": { "value": "error" } } } }
```

⚠️ Don't use `term` on `text` fields — they're analyzed, so exact match won't work as expected.

### terms

Match any of several values (like SQL `IN`):

```json
{ "query": { "terms": { "level": ["error", "critical", "fatal"] } } }
```

### range

Numeric/date ranges:

```json
{ "query": { "range": { "@timestamp": { "gte": "now-1h", "lt": "now" } } } }
{ "query": { "range": { "response_time": { "gte": 500, "lte": 5000 } } } }
```

Operators: `gt`, `gte`, `lt`, `lte`. Date math: `now`, `now-1d`, `now/d` (round to day).

### exists

Field exists and has a non-null value:

```json
{ "query": { "exists": { "field": "error.message" } } }
```

### wildcard

Wildcard pattern matching (`*` = any chars, `?` = single char):

```json
{ "query": { "wildcard": { "hostname": { "value": "web-prod-*" } } } }
```

⚠️ Leading wildcards (`*error`) are expensive. Avoid in production.

### regexp

Regular expression match:

```json
{ "query": { "regexp": { "path": { "value": "/api/v[0-9]+/users.*" } } } }
```

### prefix

Matches documents where field starts with value:

```json
{ "query": { "prefix": { "hostname": { "value": "web-" } } } }
```

### fuzzy

Typo-tolerant matching:

```json
{ "query": { "fuzzy": { "message": { "value": "eror", "fuzziness": "AUTO" } } } }
```

### ids

Match by document IDs:

```json
{ "query": { "ids": { "values": ["doc-1", "doc-2", "doc-3"] } } }
```

## Compound Queries

### bool

Combine multiple queries with boolean logic:

```json
{
  "query": {
    "bool": {
      "must":     [ { "match": { "message": "error" } } ],
      "filter":   [ { "range": { "@timestamp": { "gte": "now-1h" } } } ],
      "should":   [ { "term": { "level": "critical" } } ],
      "must_not": [ { "term": { "env": "dev" } } ],
      "minimum_should_match": 1
    }
  }
}
```

- `must` — required, contributes to score
- `filter` — required, does NOT contribute to score (faster, cacheable)
- `should` — optional boost (or required if no must/filter)
- `must_not` — excluded, does NOT contribute to score

**Best practice:** Put exact filters in `filter`, free-text in `must`.

### boosting

Demote results matching a negative query without excluding them:

```json
{
  "query": {
    "boosting": {
      "positive": { "match": { "message": "error" } },
      "negative": { "term": { "level": "debug" } },
      "negative_boost": 0.2
    }
  }
}
```

### constant_score

Wrap a filter to return a fixed score:

```json
{ "query": { "constant_score": { "filter": { "term": { "level": "error" } }, "boost": 1.0 } } }
```

### function_score

Custom scoring functions (decay, random, field_value_factor):

```json
{
  "query": {
    "function_score": {
      "query": { "match_all": {} },
      "functions": [
        { "field_value_factor": { "field": "popularity", "modifier": "log1p" } }
      ]
    }
  }
}
```

## Nested & Join Queries

### nested

Query nested objects (requires `nested` field type in mapping):

```json
{
  "query": {
    "nested": {
      "path": "comments",
      "query": {
        "bool": {
          "must": [
            { "match": { "comments.author": "david" } },
            { "range": { "comments.date": { "gte": "now-7d" } } }
          ]
        }
      }
    }
  }
}
```

### has_child / has_parent

Join queries for parent-child relationships:

```json
{ "query": { "has_child": { "type": "answer", "query": { "match": { "body": "elasticsearch" } } } } }
```

## Geo Queries

### geo_bounding_box

```json
{
  "query": {
    "geo_bounding_box": {
      "location": {
        "top_left": { "lat": 43.1, "lon": -79.0 },
        "bottom_right": { "lat": 42.8, "lon": -78.7 }
      }
    }
  }
}
```

### geo_distance

```json
{ "query": { "geo_distance": { "distance": "10km", "location": { "lat": 42.886, "lon": -78.878 } } } }
```

## Special Queries

### match_all / match_none

```json
{ "query": { "match_all": {} } }
{ "query": { "match_none": {} } }
```

### script

Custom scoring/filtering via Painless scripts:

```json
{
  "query": {
    "script": {
      "script": {
        "source": "doc['response_time'].value > params.threshold",
        "params": { "threshold": 1000 }
      }
    }
  }
}
```

## Search Features

### Sorting

```json
{ "sort": [ { "@timestamp": "desc" }, { "_score": "desc" } ] }
```

### Source filtering

```json
{ "_source": ["message", "level", "@timestamp"] }
{ "_source": { "includes": ["error.*"], "excludes": ["error.stack"] } }
```

### Highlighting

```json
{ "highlight": { "fields": { "message": { "pre_tags": [">>"], "post_tags": ["<<"] } } } }
```

### search_after (pagination beyond 10k)

```json
{
  "size": 100,
  "sort": [ { "@timestamp": "desc" }, { "_id": "asc" } ],
  "search_after": ["2026-01-31T12:00:00.000Z", "abc123"]
}
```

### collapse (deduplicate by field)

```json
{ "collapse": { "field": "hostname" }, "sort": [ { "@timestamp": "desc" } ] }
```

### runtime fields (query-time computed fields)

```json
{
  "runtime_mappings": {
    "duration_ms": {
      "type": "double",
      "script": "emit(doc['end_time'].value.toInstant().toEpochMilli() - doc['start_time'].value.toInstant().toEpochMilli())"
    }
  },
  "query": { "range": { "duration_ms": { "gte": 1000 } } }
}
```
