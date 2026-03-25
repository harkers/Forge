# DisplayForge Source Prompts

Prompts for implementing source connectors.

## RSS Source Connector

```text
PROJECT: DisplayForge

TASK: Implement RSS source connectors for a standalone fullscreen display system.

REQUIREMENTS:
- Support multiple RSS feeds
- Poll feeds on a schedule
- Parse and normalise items
- Cache last successful result
- Isolate source failures
- Prepare output for ticker, headlines, and card layouts

OUTPUT:
- RSS connector layer
- Normalised display items
- Refresh and fallback model
```

## Calendar Source Connector

```text
PROJECT: DisplayForge

TASK: Implement calendar source connectors for a standalone fullscreen display system.

REQUIREMENTS:
- Support calendar feeds or calendar APIs
- Parse event start/end and descriptive fields
- Normalise into display items
- Support today and upcoming views
- Handle timezone cleanly
- Cache last successful result
- Isolate source failures

OUTPUT:
- Calendar connector layer
- Normalised schedule items
- Refresh and fallback model
```

## API Source Connector

```text
PROJECT: DisplayForge

TASK: Implement API source connectors for a standalone fullscreen display system.

REQUIREMENTS:
- Support JSON API endpoints
- Support Bearer token authentication
- Extract metrics via JSONPath
- Normalise into display items
- Handle error responses gracefully
- Cache and freshness tracking

OUTPUT:
- API connector layer
- Normalised status items
- Auth integration
```

## Source Manager

```text
PROJECT: DisplayForge

TASK: Implement the source manager that coordinates all connectors.

REQUIREMENTS:
- Register multiple sources of different types
- Start/stop individual sources
- Aggregate health status
- Provide unified item stream
- Handle source failures without affecting others

OUTPUT:
- SourceManager class
- Source registration interface
- Health aggregation
- Item stream emitter
```

## Cache Layer

```text
PROJECT: DisplayForge

TASK: Implement the cache layer for source data.

REQUIREMENTS:
- Per-source cache storage
- TTL-based expiration
- Persist to disk (optional)
- Fast read/write
- Clear on config change

OUTPUT:
- CacheLayer class
- Cache key/value interface
- TTL management
- Disk persistence option
```

## Normalisation Pipeline

```text
PROJECT: DisplayForge

TASK: Implement the normalisation pipeline for source data.

REQUIREMENTS:
- Accept raw data from any source type
- Transform to unified DisplayItem
- Preserve source-specific fields
- Add metadata (freshness, timestamp)
- Validate required fields

OUTPUT:
- NormalisationPipeline class
- Per-source-type transformers
- Validation logic
- DisplayItem interface
```