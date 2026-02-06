# Montana River Dashboard

A cross-platform touchscreen dashboard application for monitoring Montana river conditions, weather forecasts, and indoor environmental sensors. Designed for Raspberry Pi 5 with 7" touchscreen display (800x480), but works on macOS for development.

## Features

### Overview Tab
- Quick glance at all data sources
- Pinned river conditions with 24hr changes
- Default weather location summary
- Indoor air quality status

### River Conditions Tab
- 40+ Western Montana USGS river monitoring stations
- Current flow (CFS) and water temperature
- 24-hour change tracking
- Paginated display (5 rivers per page)
- Pin favorite river for Overview tab

### Weather Forecast Tab
- Multi-location weather from National Weather Service
- 6 pre-configured locations (customizable)
- Current conditions and 7-day forecast
- Temperature, precipitation, wind, humidity
- Quick location switching

### Indoor Air Quality Tab
- Real-time sensor monitoring (Raspberry Pi)
- Temperature, humidity, pressure
- PM2.5 air quality with EPA standards
- Historical data graphs (24/48/72 hours)
- Automatic air quality alerts

## Platform Support

**macOS (Development)**
- Full UI testing with mocked sensor data
- Real API calls for river/weather data
- Same codebase as Pi deployment

**Raspberry Pi (Production)**
- Real I2C sensor integration
- BME680: Temperature, humidity, pressure, gas
- PMSA003I: PM1.0, PM2.5, PM10
- Touch-optimized interface

## Installation

### macOS Development Setup

```bash
cd river-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Raspberry Pi Setup

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv

# Create virtual environment
cd river-dashboard
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Pi-specific sensor libraries
pip install adafruit-circuitpython-bme680
pip install adafruit-circuitpython-pm25
pip install adafruit-blinka

# Enable I2C
sudo raspi-config
# Navigate to: Interface Options > I2C > Enable

# Run application
python main.py
```

## Hardware Requirements

**Raspberry Pi Setup**
- Raspberry Pi 5 (or Pi 4)
- Official 7" Touchscreen Display (800x480)
- BME680 sensor (I2C address 0x77)
- PMSA003I sensor (I2C address 0x12)
- Power supply (5V 3A recommended)

**Sensor Wiring**
- BME680: SDA → GPIO 2, SCL → GPIO 3, VCC → 3.3V, GND → GND
- PMSA003I: SDA → GPIO 2, SCL → GPIO 3, VCC → 5V, GND → GND

## Configuration

### Adding/Removing Rivers
Edit `config/rivers.py`:
```python
RIVER_STATIONS = [
    ("River Name", "USGS_SITE_ID", True),  # True if has temperature
    ...
]
```

### Changing Weather Locations
Edit `config/towns.py`:
```python
WEATHER_LOCATIONS = [
    ("City", "State", latitude, longitude),
    ...
]
```

### Customizing Display
Edit `config/constants.py` for colors, fonts, update intervals, etc.

## Data Sources

- **Rivers**: USGS Water Services API (https://waterservices.usgs.gov/)
- **Weather**: National Weather Service API (https://www.weather.gov/documentation/services-web-api)
- **Sensors**: I2C via Adafruit CircuitPython libraries

## Data Management

- **API Updates**: Every 60 minutes
- **Sensor Logging**: Every 60 seconds to SQLite
- **Display Updates**: Sensors every 5 seconds
- **Caching**: API responses cached locally for offline viewing
- **Manual Refresh**: Click 🔄 button to force immediate update

## Touch Interaction

- Minimum 50x50px touch targets
- 0.2 second visual feedback on button press
- Scrollable content areas with smooth scrolling
- Tab persistence (selected weather location, river page, etc.)

## Air Quality Alerts

- Automatic alerts when PM2.5 > 35 µg/m³
- Modal overlay on any tab
- Dismissible for 20 minutes
- Quick navigation to Indoor Air tab

## Database

SQLite database (`sensor_data.db`) stores:
- Sensor readings with timestamps
- Unlimited retention (no auto-cleanup)
- Used for historical graphs

Schema:
```sql
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature REAL,
    humidity REAL,
    pressure REAL,
    gas_resistance REAL,
    pm1 REAL,
    pm25 REAL,
    pm10 REAL
);
```

## File Structure

```
river-dashboard/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── sensor_data.db         # SQLite database (auto-created)
├── cache/                 # Cached API responses
├── config/
│   ├── constants.py       # UI and app constants
│   ├── rivers.py         # River station configs
│   └── towns.py          # Weather location configs
├── data/
│   ├── database.py       # SQLite operations
│   ├── sensors.py        # Sensor reading (with mocking)
│   ├── usgs_api.py       # USGS river data
│   └── nws_api.py        # NWS weather data
├── ui/
│   ├── components.py     # Reusable UI components
│   ├── overview_tab.py   # Overview tab
│   ├── river_tab.py      # River conditions tab
│   ├── weather_tab.py    # Weather forecast tab
│   └── indoor_tab.py     # Indoor air quality tab
└── utils/
    └── platform_detect.py # Platform detection
```

## Troubleshooting

**Sensors Not Working on Pi**
- Check I2C is enabled: `sudo i2cdetect -y 1`
- Verify sensor addresses: BME680 at 0x77, PMSA003I at 0x12
- Check wiring connections
- Ensure libraries installed: `pip list | grep adafruit`

**API Errors**
- Check internet connection
- USGS API may rate limit - wait a few minutes
- NWS API requires valid coordinates
- Cached data will display if API fails

**Display Issues**
- Window size: 800x480 for Pi touchscreen
- On Mac: Manually resize window if needed
- Font rendering: Ensure Helvetica font available

**Performance**
- Background threads handle API calls
- UI remains responsive during updates
- Reduce update frequency in `config/constants.py` if needed

## Future Enhancements

Documented but not yet implemented:
- User settings panel (brightness, sleep mode)
- Historical river data averages
- River selection toggle (hide/show specific stations)
- Customizable alert thresholds
- Screen sleep mode with tap-to-wake

## License

MIT License - See LICENSE file for details

## Author

Built for Raspberry Pi 5 with 7" touchscreen display
Designed for Western Montana river monitoring

## Support

For issues, questions, or contributions, please open an issue on GitHub.
