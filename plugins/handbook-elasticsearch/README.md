# handbook-elasticsearch

Elasticsearch and Kibana REST API skill for Claude Code. Teaches Claude how to interact with Elasticsearch clusters via `curl` — no SDK, no MCP server, just markdown.

## What's Included

| File | Coverage |
|------|----------|
| `SKILL.md` | Auth, search, CRUD, bulk ops, index management, cluster health, ILM, ES\|QL, ingest pipelines |
| `references/query-dsl.md` | Full Query DSL — bool, match, term, range, nested, geo, wildcards, runtime fields |
| `references/aggregations.md` | Metric, bucket, and pipeline aggregations — SRE patterns (error rates, top-N) |
| `references/aggregations-api.md` | Aggregation API patterns with composite pagination |
| `references/search-api.md` | Search endpoint, ES\|QL, EQL, pagination (PIT + search_after) |
| `references/document-api.md` | CRUD, bulk API, delete/update by query |
| `references/index-api.md` | Index create/delete, reindex, aliases, ILM, shrink/split, rollover |
| `references/cluster-api.md` | Cluster health, node stats, shard allocation, cat APIs |
| `references/mapping-api.md` | Field types, dynamic mapping/templates, runtime fields |
| `references/kibana-api.md` | Data views, dashboards, saved objects, programmatic Lens panels, alerting |
| `references/otel-data.md` | OpenTelemetry logs/traces/metrics querying, trace-log correlation |

## Configuration

Set cluster credentials as environment variables:

```bash
export ES_URL="https://your-cluster.es.cloud.elastic.co:443"
export ES_API_KEY="your-base64-api-key"

# Optional, for Kibana API access:
export KIBANA_URL="https://your-cluster.kb.cloud.elastic.co:443"
```

## Credits

Based on [davidgeorgehope/elasticsearch-skill](https://github.com/davidgeorgehope/elasticsearch-skill).
