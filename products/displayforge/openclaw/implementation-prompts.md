# DisplayForge Implementation Prompts

Prompts for implementing DisplayForge components.

## Source Connector Base

```text
PROJECT: DisplayForge

TASK: Implement the base SourceConnector class for DisplayForge.

REQUIREMENTS:
- Abstract base class for all source types
- Methods: fetch(), parse(), normalise(), cache(), health()
- Timeout handling (default 5s)
- Retry with exponential backoff
- Cache interface (get/set/clear)
- Health state tracking

OUTPUT:
- SourceConnector abstract class
- SourceHealth interface
- Cache interface
- TypeScript implementation
```

## RSS Connector

```text
PROJECT: DisplayForge

TASK: Implement RSS source connector for DisplayForge.

REQUIREMENTS:
- Fetch RSS/Atom feed from URL
- Parse XML safely
- Handle malformed feeds gracefully
- Normalise to DisplayItem[]
- Cache last successful result
- Track freshness state
- Isolate failures (don't break other sources)

OUTPUT:
- RSSConnector class extending SourceConnector
- XML parsing with error handling
- Normalisation to DisplayItem
- Cache integration
```

## Calendar Connector

```text
PROJECT: DisplayForge

TASK: Implement calendar source connector for DisplayForge.

REQUIREMENTS:
- Fetch iCal feed from URL
- Parse events correctly
- Handle timezone conversion
- Support all-day events
- Normalise to DisplayItem[]
- Filter to today/upcoming
- Cache and freshness tracking

OUTPUT:
- CalendarConnector class extending SourceConnector
- iCal parsing
- Timezone handling
- Event filtering logic
```

## API Connector

```text
PROJECT: DisplayForge

TASK: Implement API source connector for DisplayForge.

REQUIREMENTS:
- Fetch JSON from API endpoint
- Support Bearer token auth
- JSONPath extraction for metrics
- Normalise to DisplayItem[]
- Handle error responses
- Cache and freshness tracking

OUTPUT:
- APIConnector class extending SourceConnector
- Auth handling
- JSONPath extraction
- Error response handling
```

## Display Component

```text
PROJECT: DisplayForge

TASK: Implement the main display component.

REQUIREMENTS:
- Fullscreen mode on mount
- Panel grid layout (configurable)
- Source health indicators
- Stale data badges
- Error placeholders
- Responsive scaling

OUTPUT:
- DisplayContainer component
- Panel layout components
- Health indicator components
- TypeScript/React implementation
```

## State Management

```text
PROJECT: DisplayForge

TASK: Implement state management for DisplayForge.

REQUIREMENTS:
- Track all source states
- Track refresh cycles
- Track cache state
- Expose health status
- Emit update events

OUTPUT:
- StateManager class
- Source state interface
- Event emitter
- Health aggregation
```

## Polling System

```text
PROJECT: DisplayForge

TASK: Implement the polling system for source refresh.

REQUIREMENTS:
- Configurable intervals per source
- Independent polling per source
- Pause/resume capability
- Backoff on failure
- Skip if previous refresh pending

OUTPUT:
- PollingManager class
- Interval configuration
- Backoff logic
- State tracking
```