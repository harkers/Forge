# DisplayForge Architecture Prompts

Prompts for designing and refining DisplayForge architecture.

## Architecture Overview

```text
PROJECT: DisplayForge

TASK: Design the architecture for a fullscreen operational display system.

REQUIREMENTS:
- 55-inch display target
- Multiple source types: RSS, calendar, API
- Independent source refresh with isolation
- Unified normalisation layer
- Resilient display layer
- Cached fallback on failure

OUTPUT:
- System architecture diagram
- Layer definitions
- Data flow model
```

## Source Isolation

```text
PROJECT: DisplayForge

TASK: Design source isolation so one failing source cannot break the display.

REQUIREMENTS:
- Each source refreshes independently
- Timeout on slow sources (default 5s)
- Cache per source
- Visual stale indicator when cached
- Error placeholder when no cache
- Automatic retry with backoff

OUTPUT:
- Source isolation architecture
- Cache strategy
- Error handling flow
```

## Normalisation Layer

```text
PROJECT: DisplayForge

TASK: Design the normalisation layer that converts RSS, calendar, and API data into a unified DisplayItem model.

REQUIREMENTS:
- Single DisplayItem interface for all sources
- Common fields: id, title, timestamp, source, status
- Source-specific extensions allowed
- Freshness tracking per item
- Graceful handling of missing fields

OUTPUT:
- DisplayItem TypeScript interface
- Normaliser implementations per source type
- Field mapping documentation
```

## Display Layer

```text
PROJECT: DisplayForge

TASK: Design the display layer for fullscreen 55-inch screens.

REQUIREMENTS:
- Fullscreen mode on launch
- No scrollbars or window chrome
- Large typography (24px+ body)
- High contrast themes (dark/light)
- Responsive panel layouts
- Passive display (minimal interaction)

OUTPUT:
- Layout component hierarchy
- Typography scale
- Theme system
- Widget patterns
```

## Runtime Architecture

```text
PROJECT: DisplayForge

TASK: Design the runtime architecture for unattended operation.

REQUIREMENTS:
- Auto-start on boot
- Graceful degradation
- Health monitoring endpoint
- Logging and metrics
- Auto-restart on crash

OUTPUT:
- Runtime lifecycle
- Health check specification
- Error recovery procedures
```