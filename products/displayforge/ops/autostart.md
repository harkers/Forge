# DisplayForge Auto-start

## Configure Auto-start on Boot

### Option 1: systemd (Recommended)

```bash
# Create service file
sudo nano /etc/systemd/system/displayforge.service
```

```ini
[Unit]
Description=DisplayForge Display System
After=network.target display-manager.target

[Service]
Type=simple
User=displayforge
WorkingDirectory=/opt/Forge/products/displayforge/display
ExecStart=/usr/bin/pnpm start
Restart=always
RestartSec=10
Environment=DISPLAY=:0
Environment=NODE_ENV=production

[Install]
WantedBy=graphical.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable displayforge
sudo systemctl start displayforge
```

### Option 2: PM2

```bash
pm2 start pnpm --name displayforge -- start
pm2 save
pm2 startup
```

### Option 3: Cron @reboot

```bash
crontab -e
```

Add:
```
@reboot sleep 30 && cd /opt/Forge/products/displayforge/display && pnpm start
```

## Browser Kiosk Auto-start

### Create kiosk script
`/opt/scripts/start-kiosk.sh`:
```bash
#!/bin/bash
sleep 30
chromium-browser \
  --kiosk \
  --no-first-run \
  --disable-restore-session-state \
  --start-maximized \
  --disable-infobars \
  --noerrdialogs \
  http://localhost:3000
```

### Add to autostart
```bash
chmod +x /opt/scripts/start-kiosk.sh
echo "@/opt/scripts/start-kiosk.sh" >> ~/.config/lxsession/LXDE/autostart
```

## Verify Auto-start

```bash
# Check if enabled
sudo systemctl is-enabled displayforge

# Check status
sudo systemctl status displayforge

# View logs
journalctl -u displayforge -f
```