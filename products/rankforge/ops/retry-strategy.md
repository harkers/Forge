# Intelligent Retry Strategy

## Overview
RankForge uses a classification-based retry system with exponential backoff.

## Error Classes
- transient: network/timeouts → retry
- content: prompt/data issues → no retry
- configuration: missing model/endpoints → no retry
- unknown: retry with caution

## Backoff Strategy
Attempts → Delay
1 → 60s
2 → 120s
3 → 240s
4 → 480s
5 → 960s (capped at 1 hour)

## Dead Letter Queue (DLQ)
Items that:
- exceed max attempts
- are classified as non-retryable

are moved to a DLQ table for inspection.

## Operational Guidance
- monitor DLQ weekly
- fix root causes (model, prompt, endpoint)
- requeue manually if needed
