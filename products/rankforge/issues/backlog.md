# RankForge Backlog

This backlog is the canonical planning list for GitHub issue creation and milestone setup.

## Milestones

1. Core Stability
2. Image Automation
3. Queue Architecture
4. SEO Intelligence
5. Internal Linking
6. Feedback Loop
7. Optimisation & Scale

## Issues

### Core Stability
- Fix Ollama request handling
- Implement robust JSON parsing layer
- Validate model configuration
- Add connection test action for Ollama and Stable Diffusion

### Image Automation
- Integrate Stable Diffusion WebUI API
- Generate image prompt from SEO data
- Save generated images to Media Library
- Populate image SEO metadata
- Add Open Graph and Twitter image tags

### Queue Architecture
- Create SEO queue table
- Create image queue table
- Implement SEO queue worker
- Implement image queue worker
- Add queue locking mechanism
- Add retry logic for failed jobs
- Add WP-CLI commands

### SEO Intelligence
- Implement SEO scoring system
- Build content gap analysis engine
- Implement entity extraction
- Generate JSON-LD schema

### Internal Linking
- Create internal linking table
- Implement semantic similarity engine
- Generate anchor text suggestions
- Auto-insert internal links

### Feedback Loop
- Integrate Google Search Console API
- Store CTR, clicks, impressions
- Implement title/meta A/B testing
- Trigger re-optimisation for low CTR posts

### Optimisation & Scale
- Implement async processing
- Add rate limiting for AI requests
- Implement embedding-based similarity
- Add caching layer for AI responses
