# DisplayForge

DisplayForge is a DevForge-family product focused on fullscreen operational display systems for a dedicated server and a 55-inch screen.

## Purpose

DisplayForge exists to make live system state, schedules, updates, and announcements visible at a glance on a large always-on display.

## Source Types

DisplayForge should support:

- RSS feeds
- calendar feeds and calendar APIs
- operational APIs
- queue and status feeds
- alerts and notices

## Deployment Context

DisplayForge is intended to run on a standalone server connected to a 55-inch screen.

That means it should prioritise:
- fullscreen readability
- large-format layout design
- unattended runtime stability
- source refresh and caching
- fallback behaviour when a source fails

## Example Use Cases

- organisation calendar wall
- news and update ticker from RSS
- today's schedule screen
- control-room style status board
- mixed dashboard with feeds, calendars, and system health

## Quick Start

```bash
cd products/displayforge/display
pnpm install
pnpm dev
```

## Architecture

See [architecture.md](./architecture.md) for detailed design.

## Documentation

- [Source Model](./docs/source-model.md) - Unified data model
- [Mermaid Diagrams](./docs/mermaid-diagrams.md) - Visual architecture
- [UI Concepts](./docs/ui-concepts.md) - Layout patterns
- [Screen Layouts](./docs/screen-layouts.md) - Display templates

## Skills

Agent skills for DisplayForge development are in [skills/](./skills/).

## Operations

Deployment and operations guides are in [ops/](./ops/).