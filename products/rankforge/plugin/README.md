# RankForge Plugin Scaffold

This directory contains the initial WordPress plugin scaffold for RankForge.

## Modules

- `rankforge.php` — plugin bootstrap
- `includes/core/` — core bootstrapping and settings
- `includes/ai/` — Ollama and Stable Diffusion clients
- `includes/queue/` — SEO and image queue handlers
- `includes/admin/` — admin UI and settings pages
- `includes/cli/` — WP-CLI commands

## Initial Principles

- modular classes
- safe defaults
- queue-first design for scale
- no hard overwrite of live content unless explicitly enabled
