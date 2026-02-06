#!/usr/bin/env python3
"""Test script to verify sensor reading works correctly."""

from data.sensors import SensorReader
from utils.platform_detect import get_platform_name, is_raspberry_pi

print("=" * 50)
print("Sensor Reading Test")
print("=" * 50)
print(f"Platform: {get_platform_name()}")
print(f"Is Raspberry Pi: {is_raspberry_pi()}")
print()

# Initialize sensor reader
reader = SensorReader()

# Read sensors 5 times
for i in range(5):
    data = reader.read()
    print(f"\nReading {i+1}:")
    print(f"  Temperature: {data['temperature']}°F")
    print(f"  Humidity: {data['humidity']}%")
    print(f"  Pressure: {data['pressure']} inHg")
    print(f"  Gas Resistance: {data['gas_resistance']} Ω")
    print(f"  PM1.0: {data['pm1']} µg/m³")
    print(f"  PM2.5: {data['pm25']} µg/m³")
    print(f"  PM10: {data['pm10']} µg/m³")

    # Get air quality status
    status, color = reader.get_air_quality_status(data['pm25'])
    print(f"  Air Quality: {status}")

print("\n✓ Sensor reading test complete!")
