# DisplayForge Screen Layouts

## Layout Templates

### LAYOUT-001: Dashboard (2x3 Grid)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ HEADER: Time | Date | Status Badge                                      │
├─────────────────────────┬─────────────────────────┬─────────────────────┤
│                         │                         │                     │
│   CALENDAR: TODAY       │    MAIN DASHBOARD       │   RSS FEED          │
│   (6 events)            │    (KPIs + Charts)      │   (scrolling)       │
│                         │                         │                     │
│                         │                         │                     │
├─────────────────────────┼─────────────────────────┼─────────────────────┤
│                         │                         │                     │
│   UPCOMING              │    STATUS PANEL         │   ALERTS            │
│   (next 7 days)         │    (system health)      │   (priority items) │
│                         │                         │                     │
└─────────────────────────┴─────────────────────────┴─────────────────────┘
```

**Use case:** General operations dashboard
**Refresh:** 60s intervals
**Priority:** Balanced

---

### LAYOUT-002: Fullscreen Calendar

```
┌─────────────────────────────────────────────────────────────────────────┐
│ HEADER: Today's Schedule                                    14:32        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                                                                 │   │
│   │   NOW: Team Standup                                             │   │
│   │   14:00 - 14:15 • Conference Room A                             │   │
│   │                                                                 │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   NEXT:                                                                  │
│   • 14:30 - API Review                                        15 min    │
│   • 15:00 - 1:1 with Sarah                                    30 min    │
│   • 16:00 - Sprint Planning                                   60 min    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Use case:** Meeting room display, calendar wall
**Refresh:** 30s intervals
**Priority:** Time-sensitive

---

### LAYOUT-003: Status Board

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SYSTEM STATUS                                             All Healthy    │
├────────────────┬────────────────┬────────────────┬─────────────────────┤
│                │                │                │                     │
│   SERVICES     │   QUEUE        │   RESPONSE     │   UPTIME           │
│   12/12        │   23           │   145ms        │   99.97%           │
│   running      │   pending      │   avg          │   30 days         │
│                │                │                │                     │
├────────────────┴────────────────┴────────────────┴─────────────────────┤
│                                                                         │
│   RECENT EVENTS                                                          │
│   • 14:28 • Service A restarted                              [RESOLVED] │
│   • 14:15 • Queue spike detected                              [NORMAL]  │
│   • 13:45 • Backup completed                                  [INFO]    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Use case:** Control room, NOC, status wall
**Refresh:** 10s intervals
**Priority:** Critical

---

### LAYOUT-004: RSS News Wall

```
┌─────────────────────────────────────────────────────────────────────────┐
│ NEWS & UPDATES                                            14:32 GMT     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌───────────────────────────────────────────────────────────────┐    │
│   │  HEADLINE: Major update released for Forge platform            │    │
│   │  Source: Internal • 2 hours ago                                │    │
│   └───────────────────────────────────────────────────────────────┘    │
│                                                                         │
│   RECENT:                                                               │
│   • Security patch available for review                       4h ago    │
│   • New team member joining next week                          1d ago    │
│   • Infrastructure maintenance scheduled                      2d ago    │
│                                                                         │
│   ───────────────────────────────────────────────────────────────────   │
│   [RSS FEED] Breaking news from external sources...                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Use case:** News wall, announcement display
**Refresh:** 300s intervals
**Priority:** Informational

---

## Layout Selection Logic

| Priority | Source Health | Layout |
|----------|---------------|--------|
| Critical | Any | LAYOUT-003 (Status Board) |
| Calendar-heavy | All healthy | LAYOUT-002 (Fullscreen Calendar) |
| News-heavy | All healthy | LAYOUT-004 (RSS News Wall) |
| Mixed | All healthy | LAYOUT-001 (Dashboard) |

## Responsive Breakpoints

| Screen Size | Columns | Font Scale |
|-------------|---------|------------|
| 55"+ (default) | 3 | 1.0 |
| 40-55" | 2 | 0.85 |
| <40" | 1 | 0.7 |