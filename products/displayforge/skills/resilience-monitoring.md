# Skill: Resilience Monitoring

## Scope
- Source failure detection
- Fallback strategies
- Stale data handling
- Error recovery

## Capability

Monitor source health and handle failures gracefully without breaking the display.

## Key Requirements
- Per-source health tracking
- Cached data fallback
- Visual stale indicators
- Automatic recovery retry
- Isolated failures (one source fails → others continue)

## Health States

| State | Data | Visual | Recovery |
|-------|------|--------|----------|
| Fresh | Latest refresh | Normal | Continue polling |
| Stale | Cached | Dimmed + badge | Retry with backoff |
| Error | None | Error placeholder | Retry after interval |

## Fallback Flow

```
Source → Fetch → Success → Update cache → Display (fresh)
       ↓
       Fail → Cache exists? → Yes → Use cache → Display (stale)
             ↓                        ↑
             No → Error placeholder ────┘
```

## Retry Strategy

- **Initial retry:** 5s
- **Backoff:** 2x each failure, max 60s
- **Reset:** On successful fetch

## Output
- Health monitor component
- Retry logic
- Stale indicators