# Skill: Calendar Integration

## Scope
- Calendar feed connection
- iCal or API source support
- Event parsing
- Daily/upcoming views
- Refresh and caching

## Capability

Connect DisplayForge to calendar sources and transform events into display-ready schedule items.

## Key Requirements
- Support one or more calendar sources
- Normalise event data
- Support current-day and upcoming-event display
- Handle timezone and missing-field issues safely
- Cache last-known-good event set

## Implementation Notes

### Calendar Configuration
```typescript
interface CalendarConfig {
  name: string;
  url: string; // iCal URL or API endpoint
  type: 'ical' | 'api';
  refreshInterval: number; // seconds
  timezone: string;
  enabled: boolean;
}
```

### Parsing Strategy
1. Fetch calendar data
2. Parse events (iCal or API format)
3. Extract: title, start, end, location, description
4. Normalise to DisplayItem with calendar-specific fields
5. Sort by start time
6. Store in cache

### Event Filtering
- Today's events (for current view)
- Upcoming events (for agenda view)
- Filter by category if configured

### Timezone Handling
- Parse event times in source timezone
- Convert to display timezone
- Handle all-day events correctly

## Output
- Stable calendar connector
- Normalised event items
- Today/upcoming view support
- Freshness state tracking