# Skill: Kiosk UI

## Scope
- Fullscreen display development
- Large-format layout design
- Touch-free (passive) display
- Unattended runtime stability

## Capability

Build and maintain fullscreen display interfaces for 55-inch screens.

## Key Requirements
- Fullscreen mode on launch
- No scrollbars or window chrome
- Large typography (24px+ body, 48px+ headers)
- High contrast colour schemes
- Auto-restart on error
- Graceful degradation when sources fail

## Implementation Notes

### Viewport
- Target: 1920x1080 minimum (55" display)
- Support: 3840x2160 (4K)
- Aspect: 16:9 landscape

### Typography Scale
- Title: 72px
- Section: 48px
- Item: 32px
- Body: 24px
- Timestamp: 18px

### Touch Support
- Primary: Passive display (no touch)
- Secondary: Basic touch for configuration
- Long-press to exit fullscreen

## Output
- Fullscreen React/Vue components
- Layout templates
- Typography system