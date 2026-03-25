# OpenClaw Brief — RankForge

## Project
RankForge

## Objective
Build RankForge as a DevForge-family product that automates SEO, metadata generation, image generation, and search optimisation workflows for WordPress at scale.

## Scope
RankForge should support:

- AI-assisted title and meta description generation
- JSON-LD schema generation
- Open Graph and Twitter metadata output
- featured image generation using Stable Diffusion WebUI
- SEO-safe image filenames and attachment metadata
- separate SEO and image queues for large sites
- WP-CLI support for bulk processing
- future internal linking and search-feedback loops

## Execution Model
RankForge work is organised into phased delivery:

1. Core Stability
2. Image Automation
3. Queue Architecture
4. SEO Intelligence
5. Internal Linking
6. Feedback Loop
7. Optimisation & Scale

## Current Priorities

### 1. SEO queue
- generate title, description, keywords, schema
- store SEO metadata safely
- support bulk processing without blocking WordPress

### 2. Image queue
- detect posts missing featured images
- generate image prompts from SEO fields
- call Stable Diffusion WebUI
- attach image and set as featured image
- populate OG and Twitter image fields

### 3. Image metadata
- filename based on slug and primary keyword
- attachment title, alt, caption, description
- embedded PNG text metadata where possible

## Stable Diffusion Configuration
Default target:

`http://localhost:7860/sdapi/v1/txt2img`

Default payload:

```json
{
  "prompt": "YOUR PROMPT HERE",
  "negative_prompt": "blurry, low quality, noise, watermark, text, logo, ugly, deformed",
  "steps": 25,
  "width": 1024,
  "height": 512,
  "cfg_scale": 7,
  "sampler_name": "DPM++ 2M Karras",
  "override_settings": {
    "sd_model_checkpoint": "dreamshaperXL10.safetensors",
    "sd_vae": "Automatic"
  }
}
```

## Ollama Configuration
Default target:

`http://192.168.10.80:11434/api/generate`

Recommended starting model:

`hermes3:8b`

All requests must include:

```json
{
  "stream": false
}
```

## Working Rules
- keep text and image pipelines independent
- prefer CLI and queues for large-site backfills
- do not overwrite live content without explicit setting
- prioritise safe defaults and reversible actions
- keep outputs SEO-friendly and structured

## Output Expectations
OpenClaw tasks for RankForge should produce:
- markdown briefs
- implementation plans
- issue breakdowns
- file scaffolding
- plugin module recommendations
- phased delivery aligned to the roadmap
