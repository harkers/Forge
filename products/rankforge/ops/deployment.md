# RankForge Deployment

## Workspace Path
`products/rankforge/`

## Deployment Model
RankForge is deployed as a dedicated product workspace inside the Forge umbrella repository.

## Key Directories
- `plugin/` — WordPress plugin source
- `ops/` — deployment and runbook docs
- `tests/` — payloads, prompts, and validation checklists

## WordPress Plugin Location
The plugin source lives under:

`products/rankforge/plugin/`

## Runtime Dependencies
- WordPress 6+
- PHP 8.1+
- WP-CLI
- Ollama endpoint
- Stable Diffusion WebUI endpoint

## Recommended Runtime Endpoints
- Ollama: `http://192.168.10.80:11434/api/generate`
- Stable Diffusion: `http://localhost:7860/sdapi/v1/txt2img`

## Operational Notes
- use WP-CLI for large batch jobs
- keep queues independent
- prefer real cron over pseudo-cron for production reliability
