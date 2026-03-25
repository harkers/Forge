# DisplayForge Deployment

## System Requirements

- **OS:** Linux (Debian/Ubuntu recommended)
- **Node:** v18+ or v20+
- **RAM:** 2GB minimum
- **Display:** 55-inch, 1920x1080 minimum resolution
- **Network:** Stable connection for source polling

## Installation

### 1. Clone and Install
```bash
cd /opt
git clone https://github.com/harkers/Forge.git
cd Forge/products/displayforge/display
pnpm install
```

### 2. Build
```bash
pnpm build
```

### 3. Configure Sources
Edit `config/sources.yaml` with your RSS, calendar, and API sources.

### 4. Run
```bash
pnpm start
```

## Production Deployment

### Using PM2
```bash
pm2 start pnpm --name displayforge -- start
pm2 save
pm2 startup
```

### Using systemd
Create `/etc/systemd/system/displayforge.service`:
```ini
[Unit]
Description=DisplayForge Display System
After=network.target

[Service]
Type=simple
User=displayforge
WorkingDirectory=/opt/Forge/products/displayforge/display
ExecStart=/usr/bin/pnpm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable displayforge
sudo systemctl start displayforge
```

## Browser Kiosk Mode

For fullscreen browser display:
```bash
chromium-browser \
  --kiosk \
  --no-first-run \
  --disable-restore-session-state \
  http://localhost:3000
```