# WP-CLI Commands

## Process SEO Queue

```bash
wp rankforge process-seo-queue --limit=20
```

## Process Image Queue

```bash
wp rankforge process-image-queue --limit=10
```

## Enqueue Missing Featured Images

```bash
wp rankforge enqueue-missing-images
```

## Recommended Usage Pattern
1. enqueue missing images
2. process in small batches
3. allow cron to take over

## Notes
- always start with small limits
- monitor server load
- scale gradually
