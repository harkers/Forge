# RankForge OpenClaw Prompt Pack

This directory contains product-specific OpenClaw prompts for RankForge.

## Purpose
These prompts are treated as versioned product assets. They are designed to support implementation, operations, testing, dashboard work, and resilience improvements specific to RankForge.

## Files
- `seo-prompts.md` — SEO generation and metadata tasks
- `image-prompts.md` — image generation and featured image workflows
- `queue-prompts.md` — queue processing and worker logic
- `ops-prompts.md` — deployment, WP-CLI, cron, and runtime operations
- `dashboard-prompts.md` — admin UI and operational visibility
- `resilience-prompts.md` — retry, backoff, DLQ, and fault tolerance

## Working Rule
Use the prompt file that matches the product task area. Do not reuse one generic prompt set across all DevForge products.
