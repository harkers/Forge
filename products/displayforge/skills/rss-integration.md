# Skill: RSS Integration

## Scope
- RSS source connection
- Feed polling
- Parsing
- Normalisation
- Refresh and caching

## Capability

Connect DisplayForge to RSS feeds and transform entries into display-ready items.

## Key Requirements
- Support multiple feeds
- Parse feed items safely
- Handle malformed feeds gracefully
- Cache latest successful feed
- Support headline panels and tickers

## Implementation Notes

### Feed Configuration
```typescript
interface RSSConfig {
  name: string;
  url: string;
  refreshInterval: number; // seconds
  enabled: boolean;
  category?: string;
}
```

### Parsing Strategy
1. Fetch with timeout (5s default)
2. Parse XML safely (try/catch)
3. Extract: title, description, link, pubDate, source
4. Normalise to DisplayItem
5. Store in cache
6. Mark stale if refresh fails

### Error Handling
- Malformed XML: Log, use cached, mark stale
- Timeout: Log, use cached, mark stale
- No cached data: Show error placeholder

## Output
- Stable RSS source connector
- Normalised feed items ready for display
- Freshness state tracking