# DisplayForge UI Concepts

## Design Philosophy

DisplayForge is designed for **55-inch fullscreen displays** viewed from a distance. This requires:
- Large, readable fonts (minimum 24px for body, 48px+ for headers)
- High contrast colour schemes
- Clear visual hierarchy
- Minimal interaction (passive display)

## Layout Patterns

### 1. Dashboard Grid
- 2x2 or 3x2 grid of panels
- Each panel shows one data source
- Status colours: green (healthy), amber (stale), red (error)

### 2. Split View
- Left: Calendar/schedule (takes 40%)
- Right: RSS/news ticker (takes 60%)
- Header: Time and system status

### 3. Fullscreen Calendar
- Entire screen shows today's schedule
- Current event highlighted
- Upcoming events listed below

### 4. Status Board
- KPIs across the top
- Status panels in rows
- Alerts prominently displayed

## Typography Scale

| Element | Size | Weight |
|---------|------|--------|
| Main title | 72px | Bold |
| Section header | 48px | Semi-bold |
| Item title | 32px | Medium |
| Body text | 24px | Regular |
| Timestamp | 18px | Light |

## Colour System

### Status Colours
- **Fresh/Healthy:** `#22c55e` (green-500)
- **Stale/Warning:** `#f59e0b` (amber-500)
- **Error/Critical:** `#ef4444` (red-500)
- **Unknown/Loading:** `#6b7280` (gray-500)

### Background Options
- **Dark mode (default):** `#0f172a` (slate-900)
- **Light mode:** `#f8fafc` (slate-50)

## Animation Guidelines

- **Subtle:** Fade transitions between content (300ms)
- **Ticker:** Smooth horizontal scroll for RSS
- **Status changes:** Pulse or flash for state changes
- **Avoid:** Jarring animations, rapid updates

## Widget Patterns

### Calendar Widget
- Shows current event or "Next up" countdown
- Lists upcoming events with times
- Highlights current event

### RSS Ticker
- Horizontal scrolling feed
- Shows title + source badge
- Pauses on hover (if touchscreen)

### Status Panel
- Large metric or state
- Trend indicator (up/down)
- Mini-sparkline if relevant

### Alert Banner
- Full-width banner
- Priority-based styling
- Auto-dismiss after timeout