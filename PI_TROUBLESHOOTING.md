# Raspberry Pi Troubleshooting Guide

## "Program Exited" Error - Quick Fix

### Step 1: Run Debug Script

```bash
cd /home/pi/montana-river-dashboard  # or wherever you put it
python3 debug_pi.py
```

This will show exactly what's failing. **Copy all the output and share it with me.**

### Step 2: Check Common Issues

#### Issue A: Missing Dependencies

```bash
# Install Pi-specific libraries if missing
pip3 install adafruit-circuitpython-bme680
pip3 install adafruit-circuitpython-pm25
pip3 install adafruit-blinka

# Install base dependencies
pip3 install requests matplotlib
```

#### Issue B: Display/X11 Error

If error mentions "DISPLAY" or "X11":

```bash
# Make sure you're on the Pi's desktop (not SSH)
# Or if using SSH, enable X forwarding:
export DISPLAY=:0

# Then run:
python3 main.py
```

#### Issue C: Permissions Error

```bash
# Add user to required groups
sudo usermod -a -G i2c,gpio,video pi

# Logout and login again
```

#### Issue D: I2C Not Enabled

```bash
# Enable I2C
sudo raspi-config
# Interface Options > I2C > Enable

# Reboot
sudo reboot
```

### Step 3: Run with Error Logging

```bash
./run_with_errors.sh
```

This creates `dashboard_error.log` with full error details.

### Step 4: Check Python Version

```bash
python3 --version
# Should be 3.9 or newer
```

If Python is too old:
```bash
sudo apt-get update
sudo apt-get upgrade python3
```

### Step 5: Test Individual Components

```bash
# Test sensors (will use mock data if sensors not connected)
python3 test_sensors.py

# Test APIs
python3 test_api.py

# Test without GUI
python3 test_without_gui.py
```

## Most Common Causes

### 1. Running via SSH without DISPLAY

**Problem:** Tkinter needs a display to work

**Solution:**
- Run directly on Pi (keyboard/mouse/monitor)
- OR use VNC instead of SSH
- OR export DISPLAY=:0 before running

### 2. Missing Virtual Environment

**Problem:** Dependencies installed in venv, but not activated

**Solution:**
```bash
cd /home/pi/montana-river-dashboard
source venv/bin/activate  # Activate venv
python3 main.py
```

### 3. Matplotlib Backend Issue

**Problem:** Matplotlib can't find backend for Pi

**Solution:**
```bash
# Edit main.py and add at the top, before other imports:
import matplotlib
matplotlib.use('TkAgg')
```

### 4. Sensor Libraries Not Installed

**Problem:** adafruit libraries missing

**Solution:**
```bash
pip3 install adafruit-circuitpython-bme680
pip3 install adafruit-circuitpython-pm25
pip3 install adafruit-blinka
```

## Quick Diagnostic Commands

Run these and share the output:

```bash
# 1. Python version
python3 --version

# 2. Check if in virtual environment
which python3

# 3. Check installed packages
pip3 list | grep -E "(tkinter|matplotlib|requests|adafruit)"

# 4. Check display
echo $DISPLAY

# 5. Test Tkinter
python3 -c "import tkinter; print('Tkinter OK')"

# 6. Check I2C
ls /dev/i2c-* 2>/dev/null || echo "I2C not found"

# 7. Platform detection
python3 -c "from utils.platform_detect import *; print(get_platform_name(), is_raspberry_pi())"
```

## Get Full Error Message

Instead of just seeing "Program Exited", capture the actual error:

### Method 1: Run in terminal
```bash
cd /home/pi/montana-river-dashboard
python3 main.py 2>&1 | tee error.log
```

### Method 2: Check system logs
```bash
journalctl -xe | tail -50
```

### Method 3: Use debug script
```bash
python3 debug_pi.py > debug_output.txt 2>&1
cat debug_output.txt
```

## Share With Me

To help debug, run this and share the output:

```bash
cd /home/pi/montana-river-dashboard
cat > get_debug_info.sh << 'EOF'
#!/bin/bash
echo "=== System Info ==="
uname -a
cat /etc/os-release | grep PRETTY_NAME

echo ""
echo "=== Python Info ==="
python3 --version
which python3

echo ""
echo "=== Display Info ==="
echo "DISPLAY=$DISPLAY"

echo ""
echo "=== Installed Packages ==="
pip3 list

echo ""
echo "=== I2C Check ==="
ls -la /dev/i2c-* 2>/dev/null || echo "No I2C devices"

echo ""
echo "=== Running Debug Script ==="
python3 debug_pi.py
EOF

chmod +x get_debug_info.sh
./get_debug_info.sh > full_debug.txt 2>&1
cat full_debug.txt
```

Then share the `full_debug.txt` file contents with me!

## Emergency: Run Without Sensors

If sensors are causing the crash, you can force mock mode:

Edit `data/sensors.py` and change line ~15:
```python
# Force mock mode for testing
self.is_pi = False  # Add this line
```

This will run with mocked sensor data to test the rest of the app.

## Still Stuck?

1. Run `python3 debug_pi.py` and share output
2. Run `./run_with_errors.sh` and share `dashboard_error.log`
3. Share output of the diagnostic commands above

I'll help you fix it!
