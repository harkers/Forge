# Image Prompts

## Generate Featured Image via Stable Diffusion

```
PROJECT: RankForge

TASK: Generate a featured image for a WordPress post using Stable Diffusion.

INPUT:
- post title
- focus keyword

REQUIREMENTS:
- build prompt from title + keyword
- call local SD API (localhost:7860)
- use configured defaults (1024x512, dreamshaperXL10)
- return base64 image
- ensure no text, watermark, or logos

OUTPUT:
- base64 PNG image
```
