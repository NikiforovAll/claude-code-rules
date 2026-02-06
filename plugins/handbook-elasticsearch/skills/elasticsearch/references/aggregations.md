# Aggregations Reference

Full reference for Elasticsearch aggregation types. All examples are JSON bodies for `POST /<index>/_search?size=0`.

## Table of Contents

- [Metric Aggregations](#metric-aggregations)
- [Bucket Aggregations](#bucket-aggregations)
- [Pipeline Aggregations](#pipeline-aggregations)
- [Patterns](#patterns)

## Metric Aggregations

### Basic metrics

```json
{
  "aggs": {
    "avg_response":  { "avg":  { "field": "response_time" } },
    "max_response":  { "max":  { "field": "response_time" } },
    "min_response":  { "min":  { "field": "response_time" } },
    "sum_bytes":     { "sum":  { "field": "bytes" } },
    "total_docs":    { "value_count": { "field": "_id" } }
  }
}
```

### stats / extended_stats

All basic metrics in one shot:

```json
{ "aggs": { "response_stats": { "stats": { "field": "response_time" } } } }
{ "aggs": { "response_ext": { "extended_stats": { "field": "response_time" } } } }
```

extended_stats adds: std_deviation, variance, std_deviation_bounds

### cardinality (approximate distinct count)

```json
{ "aggs": { "unique_users": { "cardinality": { "field": "user_id" } } } }
```

### percentiles / percentile_ranks

```json
{ "aggs": { "latency_pcts": { "percentiles": { "field": "response_time", "percents": [50, 90, 95, 99] } } } }
{ "aggs": { "under_200ms": { "percentile_ranks": { "field": "response_time", "values": [200, 500, 1000] } } } }
```

### top_hits (get sample documents per bucket)

```json
{
  "aggs": {
    "by_service": {
      "terms": { "field": "service.name" },
      "aggs": {
        "latest": {
          "top_hits": { "size": 3, "sort": [ { "@timestamp": "desc" } ], "_source": ["message", "level"] }
        }
      }
    }
  }
}
```

### weighted_avg

```json
{
  "aggs": {
    "weighted_score": {
      "weighted_avg": {
        "value": { "field": "score" },
        "weight": { "field": "importance" }
      }
    }
  }
}
```

## Bucket Aggregations

### terms (top N values)

```json
{
  "aggs": {
    "top_services": {
      "terms": { "field": "service.name", "size": 20, "order": { "_count": "desc" } }
    }
  }
}
```

Use `"missing": "unknown"` to include docs where field is absent.

### date_histogram

```json
{
  "aggs": {
    "over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "fixed_interval": "1h",
        "min_doc_count": 0,
        "extended_bounds": { "min": "now-24h", "max": "now" }
      }
    }
  }
}
```

Intervals: `fixed_interval` (e.g., `30s`, `5m`, `1h`, `1d`) or `calendar_interval` (`minute`, `hour`, `day`, `week`, `month`, `year`).

### histogram (numeric buckets)

```json
{ "aggs": { "response_dist": { "histogram": { "field": "response_time", "interval": 100 } } } }
```

### range / date_range

```json
{
  "aggs": {
    "latency_buckets": {
      "range": {
        "field": "response_time",
        "ranges": [
          { "key": "fast",   "to": 100 },
          { "key": "medium", "from": 100, "to": 500 },
          { "key": "slow",   "from": 500 }
        ]
      }
    }
  }
}
```

### filters (named buckets from queries)

```json
{
  "aggs": {
    "status": {
      "filters": {
        "filters": {
          "errors": { "term": { "level": "error" } },
          "warnings": { "term": { "level": "warn" } },
          "info": { "term": { "level": "info" } }
        }
      }
    }
  }
}
```

### significant_terms (unusual terms vs background)

```json
{
  "query": { "term": { "level": "error" } },
  "aggs": {
    "unusual_words": { "significant_terms": { "field": "message.keyword", "size": 10 } }
  }
}
```

### composite (paginated aggregation — for large cardinality)

```json
{
  "aggs": {
    "paginated": {
      "composite": {
        "size": 100,
        "sources": [
          { "service": { "terms": { "field": "service.name" } } },
          { "level":   { "terms": { "field": "level" } } }
        ]
      }
    }
  }
}
```

Paginate by passing `"after": { "service": "last-value", "level": "last-value" }` from previous response.

### multi_terms (group by multiple fields)

```json
{
  "aggs": {
    "service_level": {
      "multi_terms": {
        "terms": [
          { "field": "service.name" },
          { "field": "level" }
        ],
        "size": 50
      }
    }
  }
}
```

### nested (aggregate on nested objects)

```json
{
  "aggs": {
    "comments": {
      "nested": { "path": "comments" },
      "aggs": {
        "top_authors": { "terms": { "field": "comments.author.keyword" } }
      }
    }
  }
}
```

### sampler / diversified_sampler

Limit analysis to top N scoring docs (performance optimization):

```json
{
  "aggs": {
    "sample": {
      "sampler": { "shard_size": 200 },
      "aggs": {
        "keywords": { "significant_terms": { "field": "message.keyword" } }
      }
    }
  }
}
```

## Pipeline Aggregations

Operate on output of other aggregations.

### moving_avg / moving_fn

```json
{
  "aggs": {
    "over_time": {
      "date_histogram": { "field": "@timestamp", "fixed_interval": "1h" },
      "aggs": {
        "avg_response": { "avg": { "field": "response_time" } },
        "smoothed": {
          "moving_fn": { "buckets_path": "avg_response", "window": 5, "script": "MovingFunctions.unweightedAvg(values)" }
        }
      }
    }
  }
}
```

### derivative (rate of change)

```json
{
  "aggs": {
    "over_time": {
      "date_histogram": { "field": "@timestamp", "fixed_interval": "1h" },
      "aggs": {
        "total": { "sum": { "field": "count" } },
        "rate_of_change": { "derivative": { "buckets_path": "total" } }
      }
    }
  }
}
```

### cumulative_sum

```json
{
  "aggs": {
    "over_time": {
      "date_histogram": { "field": "@timestamp", "fixed_interval": "1d" },
      "aggs": {
        "daily_count": { "value_count": { "field": "_id" } },
        "running_total": { "cumulative_sum": { "buckets_path": "daily_count" } }
      }
    }
  }
}
```

### bucket_script (compute across sibling metrics)

```json
{
  "aggs": {
    "by_service": {
      "terms": { "field": "service.name" },
      "aggs": {
        "errors":  { "filter": { "term": { "level": "error" } } },
        "total":   { "value_count": { "field": "_id" } },
        "error_rate": {
          "bucket_script": {
            "buckets_path": { "err": "errors._count", "tot": "total" },
            "script": "params.err / params.tot * 100"
          }
        }
      }
    }
  }
}
```

### bucket_sort (sort/limit aggregation buckets)

```json
{
  "aggs": {
    "by_service": {
      "terms": { "field": "service.name", "size": 100 },
      "aggs": {
        "avg_latency": { "avg": { "field": "response_time" } },
        "sort_by_latency": {
          "bucket_sort": { "sort": [ { "avg_latency": { "order": "desc" } } ], "size": 10 }
        }
      }
    }
  }
}
```

### bucket_selector (filter buckets by condition)

```json
{
  "aggs": {
    "by_service": {
      "terms": { "field": "service.name" },
      "aggs": {
        "avg_latency": { "avg": { "field": "response_time" } },
        "slow_only": {
          "bucket_selector": {
            "buckets_path": { "lat": "avg_latency" },
            "script": "params.lat > 500"
          }
        }
      }
    }
  }
}
```

## Patterns

### Error rate over time (SRE dashboard)

```json
{
  "size": 0,
  "query": { "range": { "@timestamp": { "gte": "now-24h" } } },
  "aggs": {
    "over_time": {
      "date_histogram": { "field": "@timestamp", "fixed_interval": "15m" },
      "aggs": {
        "total":  { "value_count": { "field": "_id" } },
        "errors": { "filter": { "term": { "level": "error" } } },
        "error_rate": {
          "bucket_script": {
            "buckets_path": { "err": "errors._count", "tot": "total" },
            "script": "params.tot > 0 ? (params.err / params.tot * 100) : 0"
          }
        }
      }
    }
  }
}
```

### Top N with details (leaderboard)

```json
{
  "size": 0,
  "aggs": {
    "top_endpoints": {
      "terms": { "field": "url.path.keyword", "size": 10 },
      "aggs": {
        "avg_latency": { "avg": { "field": "response_time" } },
        "p99_latency": { "percentiles": { "field": "response_time", "percents": [99] } },
        "error_count": { "filter": { "range": { "http.response.status_code": { "gte": 500 } } } }
      }
    }
  }
}
```
