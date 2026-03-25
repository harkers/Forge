# DisplayForge Source Model

## Objective

Define a unified model for RSS, calendar, and API data so DisplayForge can render all of them consistently.

## Unified Display Item

Each source item should be normalised into a structure like:

```typescript
interface DisplayItem {
  id: string;
  source_type: 'rss' | 'calendar' | 'api';
  source_name: string;
  title: string;
  summary: string;
  start_time?: Date;
  end_time?: Date;
  published_time?: Date;
  category?: string;
  priority?: 'low' | 'normal' | 'high' | 'critical';
  status?: 'pending' | 'active' | 'completed' | 'cancelled' | 'error';
  url?: string;
  freshness_state: 'fresh' | 'stale' | 'error' | 'unknown';
  raw?: any; // Original data for debugging
}
```

## Source Type Notes

### RSS
Usually provides:
- title
- description/summary
- published date
- link
- source name

### Calendar
Usually provides:
- event title
- start
- end
- location
- description
- calendar name

### API
Usually provides:
- status
- value
- labels
- timestamps
- message text

## Rendering Goal

The display layer should not care whether the item came from RSS, calendar, or API once it has been normalised.

All widgets, panels, and layouts work with `DisplayItem` and render based on:
- `source_type` (for styling)
- `priority` (for prominence)
- `freshness_state` (for trust indicator)
- timestamps (for sorting and display)

## Freshness States

| State | Meaning | Visual |
|-------|---------|--------|
| `fresh` | Recently refreshed | Normal display |
| `stale` | Refresh failed, using cache | Dimmed or marked "stale" |
| `error` | No data available | Error placeholder |
| `unknown` | Initial load | Loading state |

## Category Suggestions

| Source | Categories |
|--------|-----------|
| RSS | `news`, `updates`, `alerts`, `announcements` |
| Calendar | `meeting`, `event`, `deadline`, `reminder` |
| API | `metric`, `status`, `queue`, `health` |