# DisplayForge Strict Prompts

Constrained implementation prompts with explicit boundaries.

## RSS Source - Strict

```text
PROJECT: DisplayForge

TASK: Connect DisplayForge to RSS sources.

REQUIREMENTS:
- Support multiple feed URLs
- Parse RSS safely
- Normalise into internal item model
- Cache last-known-good feed data
- Mark stale data when refresh fails
- Do not allow one bad feed to break the display

CONSTRAINTS:
- No external dependencies beyond standard library
- Timeout after 5 seconds
- Maximum 100 items per feed
- No retry on malformed XML (use cache)

OUTPUT:
- RSS connector design
- Normalised source model
- Implementation scaffold
```

## Calendar Source - Strict

```text
PROJECT: DisplayForge

TASK: Connect DisplayForge to calendar sources.

REQUIREMENTS:
- Support calendar feed URLs or calendar APIs
- Parse events into internal item model
- Support today and upcoming agenda panels
- Handle timezone safely
- Cache last-known-good events
- Do not allow one bad source to break the display

CONSTRAINTS:
- iCal format support required
- Timezone conversion to local time
- Maximum 50 events loaded
- No retry on invalid iCal (use cache)

OUTPUT:
- Calendar connector design
- Event normalisation model
- Implementation scaffold
```

## Display Layer - Strict

```text
PROJECT: DisplayForge

TASK: Build the display layer for fullscreen 55-inch screens.

REQUIREMENTS:
- Fullscreen mode on launch
- Large typography (24px+ body, 48px+ headers)
- High contrast colour schemes
- Panel-based layout
- No scrollbars
- Graceful degradation

CONSTRAINTS:
- Target resolution: 1920x1080 minimum
- Refresh rate: 60fps
- No user interaction required (passive display)
- All panels must handle empty/error states

OUTPUT:
- Display layer architecture
- Panel component hierarchy
- Typography scale
```

## State Management - Strict

```text
PROJECT: DisplayForge

TASK: Implement state management for display data.

REQUIREMENTS:
- Track source health (fresh/stale/error)
- Track refresh cycles
- Track cached data
- Expose health status for display
- Isolate source failures

CONSTRAINTS:
- Single source of truth
- Immutable state updates
- No global state (component-scoped)
- State persists across source failures

OUTPUT:
- State manager design
- Health status interface
- State update flow
```

## Error Handling - Strict

```text
PROJECT: DisplayForge

TASK: Implement error handling for DisplayForge.

REQUIREMENTS:
- Per-source error isolation
- Stale cache fallback
- Visual error indicators
- Automatic retry with backoff
- Log all errors with context

CONSTRAINTS:
- Never crash on source failure
- Never show blank screen
- Always display cached data if available
- Maximum 3 retry attempts
- Retry backoff: 5s, 15s, 30s

OUTPUT:
- Error handling design
- Fallback flow diagram
- Logging specification
```

## Configuration - Strict

```text
PROJECT: DisplayForge

TASK: Create configuration system for DisplayForge.

REQUIREMENTS:
- YAML configuration files
- Environment variable override
- Validation on startup
- Default values for all settings
- Clear error messages for invalid config

CONSTRAINTS:
- No hot reload (restart required)
- Single config file path
- All paths relative to config directory
- No database for config (file-based)

OUTPUT:
- Configuration schema
- Validation rules
- Environment variable mapping
```

## Deployment - Strict

```text
PROJECT: DisplayForge

TASK: Create deployment setup for DisplayForge.

REQUIREMENTS:
- Linux target (Debian/Ubuntu)
- Auto-start on boot
- Automatic restart on failure
- Health monitoring endpoint
- Log rotation

CONSTRAINTS:
- No root required after installation
- Single user account (displayforge)
- systemd for process management
- Logs in /var/log/displayforge/

OUTPUT:
- systemd service unit
- Installation script
- Log rotation config
```