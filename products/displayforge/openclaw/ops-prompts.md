# DisplayForge Operations Prompts

Prompts for deployment and operations.

## Deployment

```text
PROJECT: DisplayForge

TASK: Create deployment documentation and scripts for DisplayForge.

REQUIREMENTS:
- Linux target (Debian/Ubuntu)
- Node.js 18+ runtime
- PM2 or systemd for process management
- Auto-start on boot
- Health endpoint monitoring

OUTPUT:
- deployment.md documentation
- systemd service unit
- PM2 ecosystem file
- Installation script
```

## Configuration

```text
PROJECT: DisplayForge

TASK: Create configuration system for DisplayForge.

REQUIREMENTS:
- YAML configuration files
- Environment variable support
- Validation on startup
- Hot reload (optional)
- Default values for all settings

OUTPUT:
- config/runtime.yaml schema
- Environment variable mapping
- Validation functions
- Configuration loader
```

## Auto-start

```text
PROJECT: DisplayForge

TASK: Configure DisplayForge to auto-start on boot.

REQUIREMENTS:
- Start after network and display
- Restart on failure
- Browser kiosk mode configuration
- Timeout handling

OUTPUT:
- systemd service configuration
- Browser kiosk script
- autostart documentation
```

## Monitoring

```text
PROJECT: DisplayForge

TASK: Set up monitoring for DisplayForge.

REQUIREMENTS:
- Health endpoint (/health)
- Prometheus metrics
- Source status tracking
- Alerting rules for failures

OUTPUT:
- Health endpoint implementation
- Prometheus metrics
- monitoring.md documentation
- Alerting rules
```

## Troubleshooting

```text
PROJECT: DisplayForge

TASK: Create troubleshooting guide for DisplayForge.

REQUIREMENTS:
- Common issues and fixes
- Diagnostic commands
- Log analysis guides
- Recovery procedures

OUTPUT:
- troubleshooting.md documentation
- Diagnostic script
- Log format specification
- Recovery runbook
```

## Source Configuration

```text
PROJECT: DisplayForge

TASK: Create source configuration guide for DisplayForge.

REQUIREMENTS:
- RSS source configuration
- Calendar source configuration
- API source configuration
- Per-source settings
- Auth handling

OUTPUT:
- source-config.md documentation
- Configuration examples
- Validation schema
```