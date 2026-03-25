# Resilience Prompts

## Retry and Backoff

```
PROJECT: RankForge

TASK: Implement retry and backoff for failed jobs.

REQUIREMENTS:
- classify errors (transient, config, content)
- retry transient errors with exponential backoff
- move permanent failures to dead-letter queue
- track retry count

OUTPUT:
- resilient queue processing system
```
