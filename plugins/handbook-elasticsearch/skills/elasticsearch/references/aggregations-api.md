# Aggregations API Reference

Aggregations run inside `_search` requests under the `aggs` key. Combine with `"size": 0` to skip hits and only return aggregation results.

## Metric Aggregations

```bash
es "my-index/_search" -d '{
  "size": 0,
  "aggs": {
    "avg_duration": {"avg": {"field": "duration_ms"}},
    "max_duration": {"max": {"field": "duration_ms"}},
    "p95_duration": {"percentiles": {"field": "duration_ms", "percents": [50, 95, 99]}},
    "unique_users": {"cardinality": {"field": "user.id"}},
    "total_bytes": {"sum": {"field": "response.bytes"}},
    "duration_stats": {"stats": {"field": "duration_ms"}}
  }
}'
```

## Bucket Aggregations

**Terms** (group by field value):
```json
{
  "size": 0,
  "aggs": {
    "by_status": {
      "terms": {"field": "status.keyword", "size": 20},
      "aggs": {
        "avg_duration": {"avg": {"field": "duration_ms"}}
      }
    }
  }
}
```

**Date histogram** (time buckets):
```json
{
  "size": 0,
  "aggs": {
    "over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "fixed_interval": "1h"
      },
      "aggs": {
        "error_count": {
          "filter": {"term": {"level": "error"}},
          "aggs": {"count": {"value_count": {"field": "_id"}}}
        }
      }
    }
  }
}
```

**calendar_interval** options: `minute`, `hour`, `day`, `week`, `month`, `quarter`, `year`
**fixed_interval** options: `30s`, `1m`, `5m`, `1h`, `1d`, etc.

**Range** (custom buckets):
```json
{
  "size": 0,
  "aggs": {
    "latency_ranges": {
      "range": {
        "field": "duration_ms",
        "ranges": [
          {"to": 100, "key": "fast"},
          {"from": 100, "to": 500, "key": "normal"},
          {"from": 500, "key": "slow"}
        ]
      }
    }
  }
}
```

**Histogram** (fixed-width numeric buckets):
```json
{
  "size": 0,
  "aggs": {
    "response_sizes": {
      "histogram": {"field": "response.bytes", "interval": 1000}
    }
  }
}
```

**Filter / Filters** (named query buckets):
```json
{
  "size": 0,
  "aggs": {
    "levels": {
      "filters": {
        "filters": {
          "errors": {"term": {"level": "error"}},
          "warnings": {"term": {"level": "warn"}},
          "info": {"term": {"level": "info"}}
        }
      }
    }
  }
}
```

## Nested Aggregations

Aggregations can nest — buckets contain sub-aggregations:

```json
{
  "size": 0,
  "aggs": {
    "by_service": {
      "terms": {"field": "service.name", "size": 10},
      "aggs": {
        "over_time": {
          "date_histogram": {"field": "@timestamp", "fixed_interval": "1h"},
          "aggs": {
            "p99": {"percentiles": {"field": "duration_ms", "percents": [99]}}
          }
        }
      }
    }
  }
}
```

## Pipeline Aggregations

Compute on other aggregation results:

**Derivative** (rate of change):
```json
{
  "aggs": {
    "per_hour": {
      "date_histogram": {"field": "@timestamp", "fixed_interval": "1h"},
      "aggs": {
        "total": {"sum": {"field": "bytes"}},
        "bytes_rate": {"derivative": {"buckets_path": "total"}}
      }
    }
  }
}
```

**Moving average**:
```json
{
  "aggs": {
    "per_day": {
      "date_histogram": {"field": "@timestamp", "calendar_interval": "day"},
      "aggs": {
        "daily_errors": {"value_count": {"field": "_id"}},
        "smoothed": {
          "moving_avg": {"buckets_path": "daily_errors", "window": 7}
        }
      }
    }
  }
}
```

**Bucket sort** (top-N buckets):
```json
{
  "aggs": {
    "by_service": {
      "terms": {"field": "service.name", "size": 100},
      "aggs": {
        "error_rate": {
          "avg": {"script": {"source": "doc['level'].value == 'error' ? 1 : 0"}}
        },
        "worst_first": {
          "bucket_sort": {"sort": [{"error_rate": {"order": "desc"}}], "size": 5}
        }
      }
    }
  }
}
```

## Composite Aggregation

Efficient pagination over all buckets (for exports):

```bash
es "my-index/_search" -d '{
  "size": 0,
  "aggs": {
    "my_composite": {
      "composite": {
        "size": 1000,
        "sources": [
          {"service": {"terms": {"field": "service.name"}}},
          {"hour": {"date_histogram": {"field": "@timestamp", "fixed_interval": "1h"}}}
        ]
      }
    }
  }
}'
# Use "after" from response to paginate: "after": {"service": "api", "hour": 1706745600000}
```
