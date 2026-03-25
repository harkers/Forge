# DisplayForge RSS Test Feeds

## Test Goals
- Validate feed parsing
- Validate malformed feed handling
- Validate refresh logic
- Validate stale-data fallback

## Test Cases

### TC-RSS-001: Normal RSS Feed
```yaml
name: "Normal RSS"
url: "https://feeds.bbci.co.uk/news/rss.xml"
expected:
  - Parse succeeds
  - Items extracted
  - Title, description, link present
  - Timestamps parsed
```

### TC-RSS-002: Atom Feed
```yaml
name: "Atom Feed"
url: "https://example.com/atom.xml"
expected:
  - Parse succeeds
  - Atom structure handled
  - Items normalised correctly
```

### TC-RSS-003: Feed with Missing Dates
```yaml
name: "Missing Dates"
url: "https://example.com/no-dates.xml"
mock: |
  <item>
    <title>Test Item</title>
    <description>Content</description>
  </item>
expected:
  - Parse succeeds
  - Items extracted
  - Timestamp defaults to current time
```

### TC-RSS-004: Malformed XML
```yaml
name: "Malformed XML"
url: "https://example.com/broken.xml"
mock: |
  <rss><item><title>Broken
expected:
  - Parse fails gracefully
  - Error logged
  - Stale cache used if available
  - Error placeholder if no cache
```

### TC-RSS-005: Timeout
```yaml
name: "Timeout"
url: "https://example.com:9999/feed.xml"
expected:
  - Request times out (5s)
  - Retry attempted
  - Stale cache used
  - Stale badge shown
```

### TC-RSS-006: Large Feed (100+ items)
```yaml
name: "Large Feed"
url: "https://example.com/large.xml"
expected:
  - Parse succeeds
  - Only configured max_items kept
  - Memory stable
  - No performance impact
```

### TC-RSS-007: Unicode Content
```yaml
name: "Unicode"
url: "https://example.com/unicode.xml"
mock: |
  <item>
    <title>日本語 ニュース</title>
    <description>Émojis 🎉 and symbols ∞</description>
  </item>
expected:
  - Unicode rendered correctly
  - No encoding issues
```

### TC-RSS-008: Empty Feed
```yaml
name: "Empty Feed"
url: "https://example.com/empty.xml"
mock: |
  <rss><channel></channel></rss>
expected:
  - Parse succeeds
  - Zero items
  - Empty state displayed
```

## Test Runner

```bash
# Run RSS tests
pnpm test:rss

# Run specific test
pnpm test:rss -- --case TC-RSS-001

# Run with verbose output
pnpm test:rss -- --verbose
```

## Mock Server

For testing, use a mock server:
```bash
# Start mock server
pnpm mock-server

# Mock endpoints available:
# http://localhost:3333/rss/normal
# http://localhost:3333/rss/malformed
# http://localhost:3333/rss/timeout
# http://localhost:3333/rss/empty
```