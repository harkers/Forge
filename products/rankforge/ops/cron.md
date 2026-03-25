# Cron Setup

## WordPress Cron (Default)
RankForge schedules jobs every 5 minutes.

## Recommended: System Cron

Edit crontab:

```bash
crontab -e
```

Add:

```bash
*/5 * * * * wp cron event run --due-now --path=/var/www/wordpress
```

## Benefits
- reliable scheduling
- avoids traffic-based triggers
- consistent queue processing

## Tuning
Adjust batch sizes in Worker:
- SEO: 5–20
- Images: 3–10
