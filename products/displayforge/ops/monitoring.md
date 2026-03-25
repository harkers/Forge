# DisplayForge Monitoring

## Health Monitoring

### Health Endpoint

`GET /health` returns system status:

```json
{
  "status": "healthy",
  "uptime": 86400,
  "version": "1.0.0",
  "sources": {
    "rss-news": {
      "status": "fresh",
      "last_refresh": "2026-03-25T14:30:00Z",
      "items": 15
    },
    "calendar-main": {
      "status": "fresh",
      "last_refresh": "2026-03-25T14:29:45Z",
      "events": 8
    },
    "api-status": {
      "status": "stale",
      "last_refresh": "2026-03-25T14:20:00Z",
      "error": "Connection timeout"
    }
  }
}
```

### Status Values

| Status | Meaning | Action |
|--------|---------|--------|
| `healthy` | All sources fresh | None |
| `degraded` | Some sources stale | Monitor |
| `error` | Critical source failed | Alert |

## Logging

### Log Levels
- `error`: Source failures, critical issues
- `warn`: Stale data, retry attempts
- `info`: Refresh cycles, configuration
- `debug`: Full request/response data

### Log Format
```
[2026-03-25 14:30:00] INFO  Source "rss-news" refreshed (15 items)
[2026-03-25 14:30:05] WARN  Source "api-status" timeout, using cache
[2026-03-25 14:30:10] ERROR Source "calendar-main" failed: Connection refused
```

## Metrics

### Built-in Metrics
- `source_refresh_total`: Counter of source refreshes
- `source_refresh_errors`: Counter of failed refreshes
- `source_refresh_duration_seconds`: Histogram of refresh times
- `display_items_current`: Gauge of displayed items

### Prometheus Format
```
# HELP source_refresh_total Total source refreshes
# TYPE source_refresh_total counter
source_refresh_total{source="rss-news",status="success"} 150
source_refresh_total{source="rss-news",status="error"} 2

# HELP display_items_current Current displayed items
# TYPE display_items_current gauge
display_items_current{source="rss-news"} 15
display_items_current{source="calendar-main"} 8
```

## Alerting Rules

### Source Down
```
alert: SourceDown
expr: source_refresh_errors{status="error"} > 3
for: 5m
severity: warning
annotations:
  summary: "Source {{ $labels.source }} failing"
```

### All Sources Stale
```
alert: AllSourcesStale
expr: count(source_status{status="stale"}) == count(source_status)
for: 10m
severity: critical
annotations:
  summary: "All sources are stale"
```

## Dashboards

### Recommended Panels
1. **Source Health Grid** - Status by source
2. **Refresh Latency** - Histogram of refresh times
3. **Error Rate** - Errors per minute
4. **Uptime** - System availability