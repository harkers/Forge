# RankForge Recommended Skills

This file captures the recommended skill areas for RankForge within the OpenClaw / DevForge operating model.

## 1. WordPress / plugin scaffolding skill

### For
- plugin structure
- hooks
- admin pages
- settings
- WP-CLI
- media handling

### Why
RankForge is fundamentally a WordPress product, so this is core.

---

## 2. Queue / worker / cron skill

### For
- queue tables
- batch processing
- locking
- retries
- cron scheduling
- CLI batch runs

### Why
The whole scale strategy depends on queues.

---

## 3. API integration skill

### For
- Ollama calls
- Stable Diffusion WebUI calls
- response validation
- timeout handling
- structured request/response patterns

### Why
RankForge lives or dies on local AI integrations.

---

## 4. Prompt engineering / structured output skill

### For
- SEO prompt shaping
- JSON-only responses
- image prompt templates
- fallback parsing

### Why
This matters directly for reliable Ollama response handling and image prompt quality.

---

## 5. Error handling / resilience skill

### For
- retry/backoff
- dead-letter queue
- error classification
- operational fault tolerance

### Why
This is what turns the system from a cool demo into a production tool.
