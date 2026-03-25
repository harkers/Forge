# DisplayForge Validation Checklist

## Pre-Deployment Validation

### Source Configuration
- [ ] At least one source configured
- [ ] All source URLs reachable
- [ ] Auth tokens valid (if required)
- [ ] Refresh intervals reasonable (>= 10s)
- [ ] Categories assigned

### Display Configuration
- [ ] Theme set (dark/light)
- [ ] Layout selected
- [ ] Font scale appropriate
- [ ] Fullscreen enabled

### System Requirements
- [ ] Node.js 18+ installed
- [ ] 2GB+ RAM available
- [ ] Network connectivity confirmed
- [ ] Display connected (55" target)

## Functional Testing

### Source Polling
- [ ] RSS feeds parse correctly
- [ ] Calendar events display
- [ ] API sources connect
- [ ] Stale data handled gracefully
- [ ] Error states display properly

### Display Rendering
- [ ] Fullscreen mode activates
- [ ] All panels render
- [ ] Typography readable at distance
- [ ] Colours visible on target display
- [ ] Animations smooth

### Error Handling
- [ ] Single source failure doesn't break display
- [ ] Cache fallback works
- [ ] Error placeholders show correctly
- [ ] Recovery happens automatically

## Performance Testing

### Load Testing
- [ ] 10+ sources refresh without lag
- [ ] Display remains responsive during refresh
- [ ] Memory usage stable over 24h
- [ ] No memory leaks

### Network Testing
- [ ] Timeout handling works (5s default)
- [ ] Retry backoff functions
- [ ] Offline mode degrades gracefully

## Security Testing

- [ ] No credentials in logs
- [ ] Auth tokens masked in health endpoint
- [ ] No external script execution
- [ ] Input sanitisation for all sources

## Deployment Checklist

- [ ] Config reviewed
- [ ] Logs directory writable
- [ ] Auto-start configured
- [ ] Health endpoint accessible
- [ ] Browser kiosk mode tested