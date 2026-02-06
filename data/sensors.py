"""Sensor reading logic with platform-specific implementations."""
import random
import time
from typing import Dict, Optional
from utils.platform_detect import is_raspberry_pi


class SensorReader:
    """Reads environmental sensors with automatic platform detection."""

    def __init__(self):
        """Initialize sensor reader based on platform."""
        self.is_pi = is_raspberry_pi()
        self.bme680 = None
        self.pmsa003i = None

        if self.is_pi:
            self._init_real_sensors()
        else:
            print("Running on non-Pi platform - using mocked sensor data")

    def _init_real_sensors(self):
        """Initialize real I2C sensors on Raspberry Pi."""
        try:
            import board
            import adafruit_bme680
            from adafruit_pm25.i2c import PM25_I2C

            # Initialize BME680
            i2c = board.I2C()
            self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

            # Sea level pressure for altitude compensation
            self.bme680.sea_level_pressure = 1013.25

            # Initialize PMSA003I
            reset_pin = None  # Using default I2C address
            self.pmsa003i = PM25_I2C(i2c, reset_pin)

            print("Real sensors initialized successfully")

        except Exception as e:
            print(f"Error initializing sensors: {e}")
            print("Falling back to mocked data")
            self.is_pi = False

    def read(self) -> Dict[str, float]:
        """
        Read all sensor values.
        Returns dict with keys: temperature, humidity, pressure, gas_resistance,
                                pm1, pm25, pm10
        """
        if self.is_pi and self.bme680 and self.pmsa003i:
            return self._read_real_sensors()
        else:
            return self._read_mock_sensors()

    def _read_real_sensors(self) -> Dict[str, float]:
        """Read data from real I2C sensors."""
        try:
            # Read BME680
            temp_c = self.bme680.temperature
            temp_f = (temp_c * 9/5) + 32
            humidity = self.bme680.humidity
            pressure_hpa = self.bme680.pressure
            pressure_inhg = pressure_hpa * 0.02953
            gas_resistance = self.bme680.gas

            # Read PMSA003I
            pm_data = self.pmsa003i.read()
            pm1 = pm_data["pm10 standard"]
            pm25 = pm_data["pm25 standard"]
            pm10 = pm_data["pm100 standard"]

            return {
                'temperature': round(temp_f, 1),
                'humidity': round(humidity, 1),
                'pressure': round(pressure_inhg, 2),
                'gas_resistance': round(gas_resistance, 0),
                'pm1': pm1,
                'pm25': pm25,
                'pm10': pm10
            }

        except Exception as e:
            print(f"Error reading sensors: {e}")
            # Fall back to mock data on error
            return self._read_mock_sensors()

    def _read_mock_sensors(self) -> Dict[str, float]:
        """Generate mock sensor data for testing on Mac."""
        return {
            'temperature': round(random.uniform(68, 74), 1),
            'humidity': round(random.uniform(35, 45), 1),
            'pressure': round(random.uniform(29.8, 30.2), 2),
            'gas_resistance': round(random.uniform(50000, 200000), 0),
            'pm1': round(random.uniform(3, 10), 1),
            'pm25': round(random.uniform(5, 15), 1),
            'pm10': round(random.uniform(8, 20), 1)
        }

    def get_air_quality_status(self, pm25: float) -> tuple:
        """
        Determine air quality status based on PM2.5.
        Returns (status_text, color)
        """
        if pm25 <= 12:
            return ("Good", "#44ff44")
        elif pm25 <= 35:
            return ("Moderate", "#ffa500")
        elif pm25 <= 55:
            return ("Unhealthy for Sensitive", "#ff8c00")
        elif pm25 <= 150:
            return ("Unhealthy", "#ff4444")
        else:
            return ("Very Unhealthy", "#8b0000")
