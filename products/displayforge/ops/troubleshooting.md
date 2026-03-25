# DisplayForge Troubleshooting

## Common Issues

### Display Not Loading

**Symptoms:** Blank screen, loading spinner forever

**Causes & Fixes:**
1. **No sources configured**
   ```bash
   # Check sources file
   cat config/sources.yaml
   # Add at least one source
   ```

2. **All sources failing**
   ```bash
   # Check health endpoint
   curl http://localhost:3000/health
   # Review logs for errors
   tail -f /var/log/displayforge/app.log
   ```

3. **Network issues**
   ```bash
   # Test connectivity
   curl -I https://your-source-url.com
   # Check DNS
   nslookup your-source-url.com
   ```

### Source Shows "Stale"

**Symptoms:** Source displays with stale badge

**Causes & Fixes:**
1. **Source timeout**
   - Increase `timeout` in source config
   - Check if source URL is reachable

2. **Invalid response**
   ```bash
   # Test source manually
   curl https://source-url.com/feed.rss
   # Check for XML parsing errors
   ```

3. **Auth failure**
   - Verify API tokens
   - Check auth configuration

### Calendar Events Missing

**Symptoms:** Calendar panel empty or showing wrong events

**Causes & Fixes:**
1. **Timezone mismatch**
   ```yaml
   # Set timezone in config
   calendar:
     timezone: "Europe/London"
   ```

2. **No upcoming events**
   - Calendar may be empty
   - Check `show_upcoming` days setting

3. **iCal parsing error**
   ```bash
   # Validate iCal format
   curl https://calendar-url.ics | head -20
   ```

### Display Shows Errors

**Symptoms:** Error placeholders on panels

**Causes & Fixes:**
1. **Source down**
   - Check source availability
   - Check firewall rules

2. **Auth expired**
   - Refresh API tokens
   - Update auth config

3. **Rate limited**
   - Reduce refresh frequency
   - Add authentication

## Diagnostic Commands

```bash
# Check service status
sudo systemctl status displayforge

# View recent logs
journalctl -u displayforge -n 100

# Check health
curl http://localhost:3000/health | jq

# Test source connectivity
curl -I https://source-url.com

# Restart service
sudo systemctl restart displayforge
```

## Log Analysis

### Finding Errors
```bash
grep ERROR /var/log/displayforge/app.log
grep WARN /var/log/displayforge/app.log
```

### Recent Activity
```bash
tail -f /var/log/displayforge/app.log
```

### Source Refresh Logs
```bash
grep "Source.*refreshed" /var/log/displayforge/app.log | tail -20
```

## Recovery Procedures

### Full Restart
```bash
sudo systemctl restart displayforge
# Check status after 10s
sleep 10 && sudo systemctl status displayforge
```

### Clear Cache
```bash
rm -rf /var/lib/displayforge/cache/*
sudo systemctl restart displayforge
```

### Factory Reset
```bash
# Backup config
cp -r config config.backup
# Reset to defaults
git checkout config/sources.yaml
# Restart
sudo systemctl restart displayforge
```