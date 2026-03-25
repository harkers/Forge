# DisplayForge Source Configuration

## Source Types

DisplayForge supports:
- RSS feeds
- Calendar feeds (iCal)
- API sources (JSON)

## Configuration File

`config/sources.yaml`:

```yaml
sources:
  # RSS Sources
  - name: "Company News"
    type: rss
    url: "https://example.com/news.rss"
    enabled: true
    refresh_interval: 300s
    category: "news"
    display:
      panel: "rss-ticker"
      max_items: 10

  - name: "Security Alerts"
    type: rss
    url: "https://example.com/security.rss"
    enabled: true
    refresh_interval: 60s
    category: "alerts"
    priority: high
    display:
      panel: "alerts"
      max_items: 5

  # Calendar Sources
  - name: "Team Calendar"
    type: calendar
    url: "https://calendar.google.com/.../basic.ics"
    enabled: true
    refresh_interval: 300s
    timezone: "Europe/London"
    display:
      panel: "calendar-today"
      show_today: true
      show_upcoming: 7

  # API Sources
  - name: "System Status"
    type: api
    url: "https://api.example.com/status"
    enabled: true
    refresh_interval: 10s
    auth:
      type: bearer
      token: "${STATUS_API_TOKEN}"
    display:
      panel: "status-board"
      metrics:
        - path: "$.services"
          label: "Services"
        - path: "$.queue"
          label: "Queue"
```

## Per-Source Settings

### RSS
| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `name` | string | required | Display name |
| `url` | string | required | Feed URL |
| `refresh_interval` | duration | 300s | Polling interval |
| `category` | string | null | Category tag |
| `priority` | enum | normal | low/normal/high/critical |

### Calendar
| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `name` | string | required | Display name |
| `url` | string | required | iCal URL |
| `timezone` | string | UTC | Event timezone |
| `show_today` | bool | true | Show today's events |
| `show_upcoming` | int | 7 | Days to show upcoming |

### API
| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `name` | string | required | Display name |
| `url` | string | required | API endpoint |
| `auth` | object | null | Authentication config |
| `metrics` | array | [] | JSONPath extractions |

## Operational Rules

1. Each source refreshes independently
2. Failures are isolated per source
3. Stale data is visibly marked
4. Cached data reused if live refresh fails
5. Timeout prevents blocking on slow sources