# DisplayForge Application

This directory contains the DisplayForge application code.

## Structure

```
display/
├── src/           # Source code
├── public/        # Static assets
├── layouts/       # Layout components
├── widgets/       # Widget components
├── sources/       # Source connectors
│   ├── rss/       # RSS connector
│   ├── calendar/  # Calendar connector
│   └── api/       # API connector
└── assets/        # Images, fonts, etc.
```

## Getting Started

```bash
# Install dependencies
pnpm install

# Development mode
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start
```

## Architecture

See [../architecture.md](../architecture.md) for the full architecture documentation.