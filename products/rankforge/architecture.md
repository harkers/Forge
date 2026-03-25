# RankForge Architecture

## Core Components

### 1. SEO Engine
- Ollama integration
- prompt-based metadata generation

### 2. Image Engine
- Stable Diffusion WebUI API
- prompt generation from SEO data

### 3. Queue System
- SEO queue
- image queue
- retry + failure tracking

### 4. WordPress Integration
- hooks into post lifecycle
- WP-CLI support
- admin dashboard

### 5. Metadata Layer
- title
- meta description
- schema
- OG + Twitter metadata

### 6. Future Modules
- LinkForge (internal linking)
- RankPulse (feedback loop)
