# DisplayForge Architecture

## Product Role

DisplayForge is a fullscreen presentation system for a dedicated server and a 55-inch screen.

It should consume multiple live sources and render them into a stable, readable wall display.

## Source Categories

### 1. RSS Sources
Used for:
- news feeds
- internal updates
- blog feeds
- system notices
- announcement streams

### 2. Calendar Sources
Used for:
- daily events
- upcoming schedules
- room/resource bookings
- organisational timelines
- rotating agenda panels

### 3. API Sources
Used for:
- queue state
- metrics
- service health
- custom dashboards

## Core Layers

### 1. Source Connector Layer
- RSS parser
- iCal or calendar API connector
- JSON API connector

### 2. Normalisation Layer
Convert all source types into a consistent internal display model with fields such as:
- title
- timestamp
- source
- status
- priority
- category
- body/summary

### 3. Display Layer
- agenda panels
- RSS tickers
- headline cards
- KPI boards
- fullscreen layouts

### 4. Runtime Layer
- polling / refresh
- caching
- stale-data handling
- source failure isolation

## Design Principles

1. **Isolation:** One broken feed must not break the whole screen
2. **Readability:** Large-format readability comes first
3. **Predictability:** Source refresh should be predictable
4. **Resilience:** Cached last-known-good data should be available where possible

## Source Isolation Model

```
┌─────────────────────────────────────────────────────────────┐
│                     DisplayForge Runtime                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│  │ RSS #1  │  │ RSS #2  │  │ Cal #1  │  │ API #1  │  ...   │
│  │ (cached)│  │ (cached)│  │ (cached)│  │ (cached)│         │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘         │
│       │            │            │            │               │
│       └────────────┴────────────┴────────────┘               │
│                           │                                   │
│                    Normaliser                                │
│                           │                                   │
│                    Display Layer                              │
│                           │                                   │
│                    ┌──────┴──────┐                            │
│                    │  55" Screen │                            │
│                    └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

Each source:
- Refreshes independently
- Caches its own data
- Fails without affecting others
- Shows stale-state when degraded

## Technology Stack

- **Frontend:** React/TypeScript or similar
- **Build:** Vite or similar
- **Source Connectors:** Native fetch with timeout/caching
- **State Management:** Local state with polling intervals

## Related Projects

- **RankForge:** Processing and optimisation (data producer)
- **ForgeOrchestra:** Orchestration commands
- **ForgePipeline:** Status and health reporting