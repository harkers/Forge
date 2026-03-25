# DisplayForge Runtime Configuration

## Configuration File

`config/runtime.yaml`:

```yaml
# Display settings
display:
  title: "DisplayForge"
  fullscreen: true
  refresh_interval: 60s

# Source polling
sources:
  refresh_interval: 300s
  timeout: 5s
  retries: 3
  cache_ttl: 600s

# UI settings
ui:
  theme: dark
  font_scale: 1.0
  layout: dashboard

# Logging
logging:
  level: info
  file: /var/log/displayforge/app.log
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DISPLAYFORGE_PORT` | 3000 | HTTP server port |
| `DISPLAYFORGE_CONFIG` | ./config | Config directory |
| `DISPLAYFORGE_LOG_LEVEL` | info | Log level |
| `DISPLAYFORGE_THEME` | dark | UI theme |

## Runtime Commands

### Start
```bash
pnpm start
```

### Start with config
```bash
DISPLAYFORGE_CONFIG=/path/to/config pnpm start
```

### Development mode
```bash
pnpm dev
```

### Build for production
```bash
pnpm build
```

## Health Endpoint

`GET /health` returns:
```json
{
  "status": "healthy",
  "uptime": 3600,
  "sources": {
    "rss-news": "fresh",
    "calendar-main": "fresh",
    "api-status": "stale"
  }
}
```