# OpenClaw Brief: DisplayForge

## Context

DisplayForge handles all visual output for the Forge ecosystem:
- Signage, dashboards, kiosks, control surfaces

## Agent Integration Points

### Status Reporting
- Report to ForgePipeline on startup/shutdown
- Health checks every 30 seconds
- Content status updates

### Orchestration Commands
- Accept commands from ForgeOrchestra
- Support display scheduling
- Handle emergency content override

### Skills Needed
- `display-forge-deploy` - Deploy to display targets
- `display-forge-content` - Manage content templates
- `display-forge-status` - Check display health
