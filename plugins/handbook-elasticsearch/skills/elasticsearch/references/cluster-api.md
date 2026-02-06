# Cluster & Node API Reference

## Cluster Health

```bash
# Quick health check
es "_cluster/health" | jq '{status, number_of_nodes, active_shards, unassigned_shards}'

# Per-index health
es "_cluster/health?level=indices" | jq '.indices | to_entries[] | select(.value.status != "green") | {index: .key, status: .value.status}'
```

Status meanings:
- **green**: All primary and replica shards assigned
- **yellow**: All primaries assigned, some replicas missing (common on single-node)
- **red**: Some primary shards unassigned — data may be unavailable

## Cluster Stats

```bash
es "_cluster/stats" | jq '{
  nodes: .nodes.count.total,
  indices: .indices.count,
  docs: .indices.docs.count,
  store_size: .indices.store.size_in_bytes,
  memory: .nodes.jvm.mem.heap_used_in_bytes
}'
```

## Cluster Settings

```bash
# Get all settings (persistent + transient)
es "_cluster/settings?include_defaults=true&flat_settings=true"

# Update persistent setting
es "_cluster/settings" -XPUT -d '{
  "persistent": {
    "cluster.routing.allocation.enable": "all"
  }
}'
```

## Node Stats

```bash
# All node stats
es "_nodes/stats" | jq '.nodes | to_entries[] | {name: .value.name, heap_pct: .value.jvm.mem.heap_used_percent, cpu: .value.os.cpu.percent, disk: .value.fs.total}'

# Specific metrics
es "_nodes/stats/jvm,os,fs"

# Hot threads (debugging slow nodes)
es "_nodes/hot_threads"
```

## Node Info

```bash
es "_nodes" | jq '.nodes | to_entries[] | {name: .value.name, roles: .value.roles, version: .value.version, os: .value.os.pretty_name}'
```

## Shard Allocation

```bash
# List shards with allocation
es "_cat/shards?v&s=store:desc&h=index,shard,prirep,state,store,node"

# Why a shard is unassigned
es "_cluster/allocation/explain" -XPOST -d '{
  "index": "my-index",
  "shard": 0,
  "primary": true
}'

# Reroute a shard manually
es "_cluster/reroute" -XPOST -d '{
  "commands": [
    {"allocate_replica": {"index": "my-index", "shard": 0, "node": "node-2"}}
  ]
}'
```

## Pending Tasks

```bash
es "_cluster/pending_tasks"
es "_cat/pending_tasks?v"
```

## Task Management

```bash
# List running tasks
es "_tasks?detailed=true&actions=*reindex*"

# Cancel a task
es "_tasks/node_id:task_id/_cancel" -XPOST
```

## Cat APIs

Quick cluster overview commands (append `?v` for headers, `?format=json` for JSON):

```bash
es "_cat/health?v"                    # Cluster health one-liner
es "_cat/nodes?v&h=name,heap.percent,ram.percent,cpu,load_1m,disk.used_percent,node.role"
es "_cat/indices?v&s=store.size:desc" # Indices sorted by size
es "_cat/shards?v&s=store:desc"       # Shards sorted by size
es "_cat/segments?v"                  # Segment info
es "_cat/recovery?v&active_only"      # Active recoveries
es "_cat/thread_pool?v&h=node_name,name,active,queue,rejected"  # Thread pools
es "_cat/fielddata?v"                 # Fielddata memory usage
```
