# DisplayForge Screen Test Scenarios

## Physical Display Testing

Test DisplayForge on a 55-inch display to validate readability and layout.

### Equipment Needed
- 55-inch display (or target size)
- Connected display system
- Fullscreen browser

### Test Scenarios

#### Scenario 1: Readability
- **Distance:** 2-3 meters
- **Check:** All text readable
- **Check:** Timestamps visible
- **Check:** Status indicators clear

#### Scenario 2: Brightness
- **Condition:** Normal office lighting
- **Check:** Dark theme readable
- **Check:** Light theme readable
- **Check:** Status colours distinguishable

#### Scenario 3: Content Density
- **Layout:** 2x3 grid
- **Check:** Each panel legible
- **Check:** No overflow clipping
- **Check:** Balanced whitespace

#### Scenario 4: Scrolling Content
- **Content:** RSS ticker active
- **Check:** Smooth scroll
- **Check:** Readable speed
- **Check:** No jitter

#### Scenario 5: Long Content
- **Content:** Long title/description
- **Check:** Truncation correct
- **Check:** Ellipsis shown
- **Check:** No overlap

#### Scenario 6: Error States
- **Condition:** Source failure
- **Check:** Error placeholder visible
- **Check:** Stale badge readable
- **Check:** Other panels unaffected

#### Scenario 7: Time Transitions
- **Duration:** 24 hours
- **Check:** Time updates correctly
- **Check:** Date changes at midnight
- **Check:** Events appear/disappear correctly

#### Scenario 8: Refresh Visuals
- **Action:** Source refresh
- **Check:** No flicker
- **Check:** Smooth transition
- **Check:** No layout shift

### Measurements

| Metric | Target | Actual |
|--------|--------|--------|
| Title readability distance | 3m | |
| Body readability distance | 2m | |
| Status colour visibility | 3m | |
| Max refresh latency | 100ms | |
| Animation smoothness | 60fps | |

### Pass Criteria
- All text readable from 2m
- All colours visible in normal lighting
- No visible flicker or jitter
- Smooth animations at 60fps
- Error states clearly visible