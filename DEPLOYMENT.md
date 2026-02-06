# Deployment Guide

## Quick Start (macOS Development)

```bash
# Install dependencies
pip3 install requests matplotlib

# Run the application
python3 main.py
```

The app will open in a window at 800x480 resolution with mocked sensor data. All river and weather data is real from USGS and NWS APIs.

## Testing Before Deployment

### 1. Test Sensor Mocking
```bash
python3 test_sensors.py
```
Should show 5 readings with random but realistic sensor values.

### 2. Test API Connections
```bash
python3 test_api.py
```
Should fetch real river and weather data from USGS and NWS APIs.

### 3. Test Full Application
```bash
python3 main.py
```
The application window should open showing all four tabs. Navigate through tabs to verify UI works correctly.

## Raspberry Pi Deployment

### Prerequisites

1. **Hardware Setup**
   - Raspberry Pi 5 or Pi 4
   - Official 7" Touchscreen Display connected
   - BME680 sensor wired to I2C (address 0x77)
   - PMSA003I sensor wired to I2C (address 0x12)
   - Internet connection via WiFi or Ethernet

2. **System Requirements**
   - Raspberry Pi OS (64-bit recommended)
   - Python 3.9 or newer
   - I2C enabled

### Installation Steps

#### 1. Prepare Raspberry Pi

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install required system packages
sudo apt-get install -y python3-pip python3-venv i2c-tools

# Enable I2C
sudo raspi-config
# Navigate to: Interface Options > I2C > Enable
# Reboot when prompted

# Verify I2C devices are detected
sudo i2cdetect -y 1
# Should show devices at 0x12 (PMSA003I) and 0x77 (BME680)
```

#### 2. Transfer Application Files

```bash
# Option A: Copy from Mac via USB drive
# Copy entire river-dashboard folder to /home/pi/

# Option B: Use git (if repository exists)
cd /home/pi
git clone <repository-url>
cd river-dashboard

# Option C: Use scp from Mac
# From Mac, in the RPiTouchscreenProject directory:
scp -r river-dashboard pi@raspberrypi.local:/home/pi/
```

#### 3. Install Python Dependencies

```bash
cd /home/pi/river-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install base dependencies
pip install -r requirements.txt

# Install Raspberry Pi specific libraries
pip install adafruit-circuitpython-bme680
pip install adafruit-circuitpython-pm25
pip install adafruit-blinka
```

#### 4. Test Sensors

```bash
# With venv activated
python3 test_sensors.py
```

Expected output should show real sensor readings (not mocked data). If sensors fail, verify wiring and I2C addresses.

#### 5. Test API Connections

```bash
python3 test_api.py
```

Should successfully fetch river and weather data. If it fails, check internet connection.

#### 6. Run Application

```bash
python3 main.py
```

Application should launch fullscreen on the 7" display.

### Auto-Start on Boot

To make the dashboard start automatically when the Pi boots:

#### Method 1: Desktop Autostart (Recommended for touchscreen)

```bash
# Create autostart directory if it doesn't exist
mkdir -p ~/.config/autostart

# Create desktop entry
cat > ~/.config/autostart/river-dashboard.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=River Dashboard
Exec=/home/pi/river-dashboard/venv/bin/python3 /home/pi/river-dashboard/main.py
Path=/home/pi/river-dashboard
Terminal=false
EOF
```

#### Method 2: Systemd Service (Headless)

```bash
# Create service file
sudo nano /etc/systemd/system/river-dashboard.service
```

Paste this content:
```ini
[Unit]
Description=Montana River Dashboard
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/river-dashboard
ExecStart=/home/pi/river-dashboard/venv/bin/python3 /home/pi/river-dashboard/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable river-dashboard
sudo systemctl start river-dashboard

# Check status
sudo systemctl status river-dashboard
```

### Troubleshooting

#### Sensors Not Detected

```bash
# Check I2C is enabled
ls /dev/i2c-*
# Should show /dev/i2c-1

# Check for devices
sudo i2cdetect -y 1
# Should show devices at addresses

# Check Python I2C access
sudo usermod -a -G i2c,gpio pi
# Logout and login again

# Test with Python
python3 -c "import board; import busio; i2c = board.I2C(); print('I2C OK')"
```

#### Display Issues

```bash
# If display not detected, check config
sudo nano /boot/config.txt

# Ensure these lines are present:
dtoverlay=vc4-kms-v3d
max_framebuffers=2

# For 7" official display:
lcd_rotate=2  # If display is upside down
```

#### Performance Issues

```bash
# Increase GPU memory
sudo raspi-config
# Performance Options > GPU Memory > Set to 256

# If still slow, reduce update frequencies in config/constants.py:
# API_UPDATE_INTERVAL = 7200  # 2 hours instead of 1
```

#### API Connection Issues

```bash
# Test network
ping -c 3 waterservices.usgs.gov
ping -c 3 api.weather.gov

# Check DNS
cat /etc/resolv.conf

# If fails, try manual DNS
echo "nameserver 8.8.8.8" | sudo tee -a /etc/resolv.conf
```

### Updating the Application

```bash
cd /home/pi/river-dashboard

# Stop service if running
sudo systemctl stop river-dashboard

# Pull updates (if using git)
git pull

# Or copy new files from Mac via scp

# Activate venv and update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl start river-dashboard
```

### Maintenance

#### View Logs

```bash
# If using systemd
sudo journalctl -u river-dashboard -f

# Check application output
tail -f /home/pi/river-dashboard/dashboard.log  # if logging to file
```

#### Database Management

```bash
cd /home/pi/river-dashboard

# Check database size
ls -lh sensor_data.db

# Query data
sqlite3 sensor_data.db "SELECT COUNT(*) FROM sensor_readings;"

# Backup database
cp sensor_data.db sensor_data.db.backup
```

#### Clear Cache

```bash
# Remove cached API responses
rm -rf cache/*.json

# Application will fetch fresh data on next update
```

## Customization

### Change River Stations

Edit `config/rivers.py`:
```python
RIVER_STATIONS = [
    ("River Name", "USGS_SITE_ID", True),
    # Add more stations
]
```

Find USGS site IDs at: https://waterdata.usgs.gov/nwis

### Change Weather Locations

Edit `config/towns.py`:
```python
WEATHER_LOCATIONS = [
    ("City", "State", latitude, longitude),
    # Add more locations
]
```

### Adjust Update Intervals

Edit `config/constants.py`:
```python
API_UPDATE_INTERVAL = 3600      # API updates (seconds)
SENSOR_DISPLAY_INTERVAL = 5     # Display refresh (seconds)
SENSOR_LOG_INTERVAL = 60        # Database logging (seconds)
```

### Change Colors/Fonts

Edit `config/constants.py`:
```python
BG_COLOR = "#1a1a1a"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#4a9eff"
# etc.
```

## Performance Optimization

### For Slower Pi Models (Pi 3, Pi Zero 2)

1. Reduce API update frequency to 2-4 hours
2. Increase sensor display interval to 10 seconds
3. Lower graph resolution in matplotlib
4. Consider disabling graphs on slower models

### For Battery Operation

1. Reduce brightness (add to future settings)
2. Increase all update intervals
3. Implement sleep mode (future feature)

## Security Considerations

1. **Network**: The app makes outbound API calls to USGS and NWS only
2. **Data**: All data is read-only from public APIs
3. **Storage**: SQLite database only stores local sensor readings
4. **Updates**: Keep Raspberry Pi OS and Python packages updated

## Backup Strategy

```bash
# Backup everything
cd /home/pi
tar -czf river-dashboard-backup-$(date +%Y%m%d).tar.gz river-dashboard/

# Restore from backup
tar -xzf river-dashboard-backup-YYYYMMDD.tar.gz
```

## Support

For issues:
1. Check troubleshooting section above
2. Review logs: `sudo journalctl -u river-dashboard`
3. Test sensors: `python3 test_sensors.py`
4. Test APIs: `python3 test_api.py`
5. Open GitHub issue with error details

## Hardware Purchasing

**Recommended Components:**
- Raspberry Pi 5 (4GB or 8GB)
- Official 7" Touchscreen Display
- BME680 Environmental Sensor (Adafruit #3660)
- PMSA003I Air Quality Sensor (Adafruit #4632)
- Raspberry Pi Case with touchscreen mount
- 5V 3A USB-C Power Supply
- 32GB+ microSD card (Class 10)

**Optional:**
- SmartiPi Touch 2 case (good touchscreen enclosure)
- Cooling fan for Pi 5
- Ethernet cable for reliable connectivity
