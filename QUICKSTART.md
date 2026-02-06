# Quick Start Guide

## Mac Development (5 minutes)

```bash
# 1. Navigate to project
cd river-dashboard

# 2. Install dependencies (one time)
pip3 install requests matplotlib

# 3. Run application
python3 main.py
```

**What to expect:**
- Window opens at 800x480 resolution
- Mocked sensor data (random but realistic)
- Real river data from USGS
- Real weather data from NWS
- All features work except real sensors

**Testing the interface:**
1. Click through all 4 tabs
2. Try pinning a river (click ☆ in River Conditions)
3. Switch weather locations
4. View sensor graphs
5. Test the refresh button (🔄)

## Raspberry Pi Setup (30 minutes)

### One-time Setup

```bash
# 1. Enable I2C
sudo raspi-config
# Interface Options > I2C > Enable > Reboot

# 2. Install dependencies
cd /home/pi/river-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install adafruit-circuitpython-bme680 adafruit-circuitpython-pm25 adafruit-blinka

# 3. Test sensors
python3 test_sensors.py

# 4. Run application
python3 main.py
```

### Auto-start on Boot

```bash
# Create autostart entry
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/river-dashboard.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=River Dashboard
Exec=/home/pi/river-dashboard/venv/bin/python3 /home/pi/river-dashboard/main.py
Path=/home/pi/river-dashboard
Terminal=false
EOF

# Reboot to test
sudo reboot
```

## Common Tasks

### Update River Stations

```bash
# Edit rivers configuration
nano config/rivers.py

# Add stations in this format:
# ("River Name", "USGS_SITE_ID", True),
```

Find USGS IDs: https://waterdata.usgs.gov/nwis/rt

### Update Weather Locations

```bash
# Edit towns configuration
nano config/towns.py

# Add locations in this format:
# ("City", "State", latitude, longitude),
```

Find coordinates: https://www.latlong.net/

### Change Update Frequency

```bash
# Edit constants
nano config/constants.py

# Change these values (in seconds):
API_UPDATE_INTERVAL = 3600      # 1 hour
SENSOR_DISPLAY_INTERVAL = 5     # 5 seconds
SENSOR_LOG_INTERVAL = 60        # 1 minute
```

### View Database

```bash
# Open SQLite
sqlite3 sensor_data.db

# Count readings
SELECT COUNT(*) FROM sensor_readings;

# View recent readings
SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 10;

# Exit
.quit
```

### Clear Cache

```bash
# Remove cached API data
rm cache/*.json

# App will fetch fresh data on next update
```

## Troubleshooting

### Sensors Not Working

```bash
# Check I2C devices
sudo i2cdetect -y 1

# Should show:
# - 0x12 (PMSA003I)
# - 0x77 (BME680)

# If not showing, check wiring
```

### No Internet Connection

App will continue to work with cached data. Last successful data will display with a ⚠️ icon.

### Display Upside Down

```bash
# Rotate display
sudo nano /boot/config.txt

# Add or change:
lcd_rotate=2  # (0, 2, or 4 for different rotations)

# Reboot
sudo reboot
```

### App Won't Start

```bash
# Check Python version (need 3.9+)
python3 --version

# Reinstall dependencies
cd /home/pi/river-dashboard
source venv/bin/activate
pip install --force-reinstall -r requirements.txt
```

## Features Overview

### Overview Tab
- Summary of pinned river
- Default weather location
- Current indoor conditions
- Updates automatically

### River Conditions Tab
- 40+ Montana river stations
- Flow (CFS) and water temperature
- 24-hour change tracking
- Click ☆ to pin favorite river
- Pagination: 5 rivers per page

### Weather Forecast Tab
- 6 preset locations
- Current conditions
- 7-day detailed forecast
- Click location to view details
- Selected location persists

### Indoor Air Tab
- Real-time sensor readings
- Air quality status
- Click "View Graphs" for history
- 24/48/72 hour data views
- Automatic alerts when PM2.5 > 35

## Keyboard Shortcuts

Application runs in GUI mode only (no keyboard shortcuts currently).

## Touch Gestures

- **Tap**: Select buttons, switch tabs
- **Scroll**: Swipe up/down on long content
- All buttons provide 0.2s visual feedback

## Data Updates

| Data Source | Update Frequency | Manual Refresh |
|-------------|------------------|----------------|
| Sensors | 5 seconds | N/A |
| River Data | 60 minutes | Yes (🔄) |
| Weather Data | 60 minutes | Yes (🔄) |

## System Resources

**Typical Usage:**
- CPU: 5-15% on Pi 5
- RAM: 100-200 MB
- Disk: <10 MB (plus database growth)
- Network: ~1 MB per API update

**Database Growth:**
- ~1 KB per sensor reading
- 60 readings/hour = ~60 KB/hour
- Daily: ~1.4 MB
- Monthly: ~42 MB
- Yearly: ~500 MB

## Getting Help

1. **Check logs**: `sudo journalctl -u river-dashboard -f`
2. **Test components**: `python3 test_sensors.py` or `python3 test_api.py`
3. **Review README**: Full documentation in README.md
4. **Deployment guide**: Complete setup in DEPLOYMENT.md

## Quick Links

- USGS Water Data: https://waterdata.usgs.gov/nwis
- NWS API Docs: https://www.weather.gov/documentation/services-web-api
- Adafruit Learn: https://learn.adafruit.com/
- Raspberry Pi Docs: https://www.raspberrypi.com/documentation/

## Version Info

Check current version:
```bash
head -20 main.py | grep -A 3 '"""'
```

## Support

For issues or questions:
1. Check this guide first
2. Review full README.md
3. Test individual components
4. Check GitHub issues
