# Real Sensor Setup Guide

## Current Status
Your dashboard is currently using **mock sensor data**. This is perfectly fine for testing and works great! But when you're ready to connect real sensors, follow this guide.

## Sensors Required

1. **BME680** - Temperature, Humidity, Pressure, Gas Resistance
   - I2C address: `0x77` (default) or `0x76`
   - Measures: Temperature (°F), Humidity (%), Pressure (inHg), Gas Resistance (Ohms)

2. **PMSA003I** - Particulate Matter Sensor
   - I2C address: `0x12`
   - Measures: PM1.0, PM2.5, PM10 (µg/m³)

## Hardware Connection

Both sensors use I2C interface on Raspberry Pi:

```
Raspberry Pi 5 GPIO Pins:
- Pin 1  (3.3V)  → Sensor VCC
- Pin 3  (SDA)   → Sensor SDA
- Pin 5  (SCL)   → Sensor SCL
- Pin 6  (GND)   → Sensor GND
```

**Connection Diagram:**
```
Pi GPIO        BME680       PMSA003I
────────       ──────       ────────
3.3V   ────────  VCC   ───── VCC
SDA    ────┬───  SDA   ───── SDA
SCL    ────┼───  SCL   ───── SCL
GND    ────┴───  GND   ───── GND
```

Both sensors share the same I2C bus (SDA/SCL) but have different addresses.

## Software Setup

### Step 1: Enable I2C on Raspberry Pi

```bash
sudo raspi-config
```

Navigate to:
- **Interface Options** → **I2C** → **Enable**

Reboot:
```bash
sudo reboot
```

### Step 2: Install Sensor Libraries

Run the installation script:

```bash
cd ~/montana-river-dashboard
./install_sensors.sh
```

Or manually install:

```bash
pip3 install adafruit-circuitpython-bme680
pip3 install adafruit-circuitpython-pm25
pip3 install adafruit-blinka
```

### Step 3: Verify Sensor Detection

Check that I2C devices are detected:

```bash
sudo i2cdetect -y 1
```

You should see:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- 12 -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- 77
```

- `12` = PMSA003I (PM2.5 sensor)
- `77` = BME680 (temp/humidity/pressure)

### Step 4: Test Sensors

Run the app:

```bash
cd ~/montana-river-dashboard
python3 main.py
```

Check the terminal output. You should see:
```
Running on: Raspberry Pi 5
✓ Initialized BME680 sensor
✓ Initialized PM2.5 sensor
Reading real sensor data...
```

Instead of:
```
⚠️  SENSOR LIBRARIES NOT INSTALLED
Falling back to mocked sensor data for now...
```

### Step 5: Verify Data

Go to the **Indoor Air** tab and check:
- Temperature reading (should be room temperature ~65-75°F)
- Humidity reading (should be ~30-60%)
- PM2.5 reading (should be ~5-20 µg/m³ in clean air)

## Troubleshooting

### Problem: Sensors Not Detected

**Check I2C is enabled:**
```bash
lsmod | grep i2c
```
Should show `i2c_dev` and `i2c_bcm2835`

**If not, enable I2C:**
```bash
sudo raspi-config
# Interface Options → I2C → Enable
sudo reboot
```

### Problem: Wrong I2C Addresses

If `i2cdetect` shows different addresses:

**BME680 at 0x76 instead of 0x77:**
Edit `data/sensors.py` line ~25:
```python
self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76)  # Changed from 0x77
```

### Problem: Libraries Not Installing

Try upgrading pip first:
```bash
pip3 install --upgrade pip
pip3 install --upgrade setuptools
```

Then reinstall:
```bash
pip3 install --force-reinstall adafruit-circuitpython-bme680
pip3 install --force-reinstall adafruit-circuitpython-pm25
pip3 install --force-reinstall adafruit-blinka
```

### Problem: Permission Denied on I2C

Add your user to the i2c group:
```bash
sudo usermod -a -G i2c $USER
sudo reboot
```

### Problem: Sensor Reading Errors

Check wiring:
- Make sure connections are solid
- Verify 3.3V (NOT 5V!) is used for power
- Check SDA/SCL are not swapped
- Try shorter wires (< 6 inches)

Check sensor initialization in terminal:
```bash
python3 main.py 2>&1 | grep -i sensor
```

## Mock Data vs Real Data

### Mock Data (Current):
- Temperature: Random 68-74°F
- Humidity: Random 35-45%
- PM2.5: Random 5-15 µg/m³
- Updates every 5 seconds with new random values

### Real Data (After Setup):
- Temperature: Actual room temperature
- Humidity: Actual room humidity
- PM2.5: Actual particulate matter in air
- Updates every 5 seconds with real measurements
- Gets logged to database every 60 seconds
- Historical graphs show real trends

## Data Logging

Once real sensors are working:

**View database:**
```bash
sqlite3 sensor_data.db
sqlite> SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 10;
```

**Export to CSV:**
```bash
sqlite3 -header -csv sensor_data.db "SELECT * FROM sensor_readings;" > sensor_data.csv
```

## Sensor Calibration

### BME680
- Temperature: Usually accurate within ±1°F
- Humidity: Usually accurate within ±3%
- No calibration typically needed

### PMSA003I
- Should read 0-5 µg/m³ in very clean air
- If consistently high indoors, sensor may need cleaning
- Laser sensors can drift over time (months/years)

## Maintenance

- **Clean sensors monthly** - Gently blow compressed air to remove dust
- **Check wiring** - Ensure connections stay solid
- **Monitor readings** - Watch for sensor failures (stuck values, extreme readings)

## Next Steps

After sensors are working:
1. ✅ Navigate to Indoor Air tab to see real readings
2. ✅ Click "View Graphs" to see historical data
3. ✅ Air quality alerts will now trigger on real PM2.5 levels
4. ✅ Data gets logged to database for long-term tracking

## Need Help?

If sensors still aren't working:
1. Run diagnostic: `python3 debug_pi.py`
2. Check full error output: `python3 main.py 2>&1 | tee sensor_debug.log`
3. Verify I2C: `sudo i2cdetect -y 1`
4. Check connections match wiring diagram above

Your app works great with mock data, so take your time with the hardware setup! 🚀
