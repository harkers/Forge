# DisplayForge Calendar Test Sources

## Test Goals
- Validate event parsing
- Validate timezone handling
- Validate daily agenda view
- Validate upcoming event logic
- Validate cached fallback

## Test Cases

### TC-CAL-001: Normal Calendar
```yaml
name: "Normal Calendar"
url: "https://calendar.google.com/.../basic.ics"
expected:
  - Parse succeeds
  - Events extracted
  - Start/end times correct
  - Timezone converted
```

### TC-CAL-002: All-Day Events
```yaml
name: "All-Day Events"
mock: |
  BEGIN:VEVENT
  DTSTART;VALUE=DATE:20260325
  DTEND;VALUE=DATE:20260326
  SUMMARY:All-day meeting
  END:VEVENT
expected:
  - Parse succeeds
  - All-day flag set
  - Displayed as full-day block
```

### TC-CAL-003: Recurring Events
```yaml
name: "Recurring Events"
mock: |
  BEGIN:VEVENT
  DTSTART:20260325T100000Z
  DTEND:20260325T110000Z
  RRULE:FREQ=WEEKLY;COUNT=10
  SUMMARY:Weekly standup
  END:VEVENT
expected:
  - Recurrence handled
  - Only next instance shown
  - Or expanded as configured
```

### TC-CAL-004: Missing Description
```yaml
name: "Missing Description"
mock: |
  BEGIN:VEVENT
  DTSTART:20260325T100000Z
  DTEND:20260325T110000Z
  SUMMARY:Title only
  END:VEVENT
expected:
  - Parse succeeds
  - Description empty/null
  - Display shows title only
```

### TC-CAL-005: Timezone Handling
```yaml
name: "Timezone"
timezone: "Europe/London"
mock: |
  BEGIN:VEVENT
  DTSTART:20260325T100000Z
  DTEND:20260325T110000Z
  SUMMARY:UTC Event
  END:VEVENT
expected:
  - Start time converted to Europe/London
  - DST handled correctly
  - Display shows local time
```

### TC-CAL-006: Empty Calendar
```yaml
name: "Empty Calendar"
mock: |
  BEGIN:VCALENDAR
  END:VCALENDAR
expected:
  - Parse succeeds
  - Zero events
  - Empty state displayed
```

### TC-CAL-007: Past Events
```yaml
name: "Past Events"
mock: |
  BEGIN:VEVENT
  DTSTART:20200101T100000Z
  DTEND:20200101T110000Z
  SUMMARY:Old event
  END:VEVENT
expected:
  - Parse succeeds
  - Event filtered out (not shown)
  - Only upcoming events displayed
```

### TC-CAL-008: Timeout/Connection Error
```yaml
name: "Timeout"
url: "https://calendar.example.com:9999/calendar.ics"
expected:
  - Request times out (10s)
  - Stale cache used if available
  - Stale badge shown
  - Retry scheduled
```

### TC-CAL-009: Invalid iCal Format
```yaml
name: "Invalid Format"
mock: |
  BEGIN:VEVENT
  SUMMARY:Broken event
  # Missing required fields
expected:
  - Parse fails gracefully
  - Error logged
  - Stale cache used
```

### TC-CAL-010: Location Field
```yaml
name: "With Location"
mock: |
  BEGIN:VEVENT
  DTSTART:20260325T100000Z
  DTEND:20260325T110000Z
  SUMMARY:Meeting
  LOCATION:Conference Room A
  END:VEVENT
expected:
  - Location extracted
  - Location displayed in event card
```

## Today/Upcoming Logic

### Today View
- Show events where `start_time` is today
- Sort by start time
- Highlight current event
- Show time remaining for current event

### Upcoming View
- Show events in next N days (configurable)
- Skip events that have already ended
- Sort by start time
- Limit to configured max items

## Test Runner

```bash
# Run calendar tests
pnpm test:calendar

# Run specific test
pnpm test:calendar -- --case TC-CAL-001

# Run with verbose output
pnpm test:calendar -- --verbose
```

## Mock Server

```bash
# Start mock iCal server
pnpm mock-server

# Mock endpoints:
# http://localhost:3333/ical/normal
# http://localhost:3333/ical/allday
# http://localhost:3333/ical/recurring
# http://localhost:3333/ical/empty
# http://localhost:3333/ical/timeout
```