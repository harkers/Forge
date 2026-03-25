# Skill: Realtime Status Panels

## Scope
- Real-time status display
- Health indicators
- KPI panels
- Metric sparklines

## Capability

Build real-time status panels for system health and operational metrics.

## Key Requirements
- Live updates without flicker
- Status colour coding
- Trend indicators (up/down/flat)
- Mini-sparklines for metrics
- Graceful data gaps

## Panel Types

### Single Metric
```
┌───────────────┐
│   SERVICES    │
│               │
│     12/12     │
│   running     │
│               │
│   ● ● ● ●     │
└───────────────┘
```

### Trend Panel
```
┌───────────────┐
│   RESPONSE    │
│               │
│    145ms      │
│    avg        │
│               │
│   ▁▂▃▄▅▆▇█   │
│   -15%       │
└───────────────┘
```

### Status Grid
```
┌───────────────┐
│   HEALTH      │
│               │
│  API    ●     │
│  Queue  ●     │
│  DB     ●     │
│  Cache  ●     │
└───────────────┘
```

## Output
- Status panel components
- Metric sparklines
- Health indicators