# DisplayForge Architecture

## Purpose

DisplayForge renders visual content for:
- Digital signage (public displays)
- Kiosk systems (interactive terminals)
- Dashboard screens (monitoring/analytics)
- Control surfaces (operator interfaces)

## Components

### Display Engine
- Rendering pipeline for multiple output targets
- Layout management and responsive adaptation
- Animation and transition engine

### Content Management
- Template-based content system
- Real-time data binding
- Scheduled content rotation

### Output Adapters
- Web renderer (HTML/CSS/Canvas)
- Native renderers (future)
- Hardware interfaces (future)

## Data Flow

```
Content Source → Display Engine → Output Adapter → Physical Display
                      ↑
              Layout Templates
```

## Integration Points

- **ForgeDeck**: Consume presentation decks as content
- **ForgeOrchestra**: Receive orchestration commands
- **ForgePipeline**: Status and health reporting
