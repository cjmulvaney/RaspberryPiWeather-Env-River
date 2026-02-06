#!/usr/bin/env python3
"""
Debug script for Raspberry Pi
Captures detailed error information
"""

import sys
import traceback

print("=" * 60)
print("RASPBERRY PI DEBUG SCRIPT")
print("=" * 60)

# Test 1: Python version
print("\n1. Python Version:")
print(f"   {sys.version}")

# Test 2: Platform detection
print("\n2. Platform Detection:")
try:
    from utils.platform_detect import is_raspberry_pi, get_platform_name
    print(f"   Platform: {get_platform_name()}")
    print(f"   Is Pi: {is_raspberry_pi()}")
except Exception as e:
    print(f"   ERROR: {e}")
    traceback.print_exc()

# Test 3: Import all modules
print("\n3. Module Imports:")
modules = [
    "tkinter",
    "config.constants",
    "config.rivers",
    "config.towns",
    "data.database",
    "data.sensors",
    "data.usgs_api",
    "data.nws_api",
    "ui.components",
    "ui.overview_tab",
    "ui.river_tab",
    "ui.weather_tab",
    "ui.indoor_tab",
]

for module in modules:
    try:
        __import__(module)
        print(f"   ✓ {module}")
    except Exception as e:
        print(f"   ✗ {module}: {e}")
        traceback.print_exc()

# Test 4: Tkinter specifically
print("\n4. Tkinter Test:")
try:
    import tkinter as tk
    print(f"   ✓ Tkinter imported")
    print(f"   Tk version: {tk.TkVersion}")
    print(f"   Tcl version: {tk.TclVersion}")

    # Try to create a window
    root = tk.Tk()
    print(f"   ✓ Window created")
    root.destroy()
    print(f"   ✓ Window destroyed")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    traceback.print_exc()

# Test 5: Sensor libraries
print("\n5. Sensor Libraries:")
try:
    import board
    print("   ✓ board")
except ImportError:
    print("   ✗ board not installed (run: pip install adafruit-blinka)")
except Exception as e:
    print(f"   ✗ board error: {e}")

try:
    import adafruit_bme680
    print("   ✓ adafruit_bme680")
except ImportError:
    print("   ✗ adafruit_bme680 not installed (run: pip install adafruit-circuitpython-bme680)")
except Exception as e:
    print(f"   ✗ adafruit_bme680 error: {e}")

try:
    from adafruit_pm25.i2c import PM25_I2C
    print("   ✓ adafruit_pm25")
except ImportError:
    print("   ✗ adafruit_pm25 not installed (run: pip install adafruit-circuitpython-pm25)")
except Exception as e:
    print(f"   ✗ adafruit_pm25 error: {e}")

# Test 6: Try to import main app
print("\n6. Main Application Import:")
try:
    import main
    print("   ✓ main.py imported successfully")
except Exception as e:
    print(f"   ✗ ERROR importing main: {e}")
    traceback.print_exc()

# Test 7: Database creation
print("\n7. Database Test:")
try:
    from data.database import SensorDatabase
    db = SensorDatabase("test_debug.db")
    print("   ✓ Database created")
    import os
    if os.path.exists("test_debug.db"):
        os.remove("test_debug.db")
        print("   ✓ Database test file removed")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    traceback.print_exc()

# Test 8: Try to run the app
print("\n8. Attempting to Run Main Application:")
print("   (This is where the crash might occur)")
try:
    from main import RiverDashboard
    print("   ✓ RiverDashboard class imported")
    print("   Creating application instance...")
    app = RiverDashboard()
    print("   ✓ Application instance created!")
    print("   Note: Not calling mainloop() - use python3 main.py for full app")
except Exception as e:
    print(f"   ✗ CRASH DETECTED: {e}")
    print("\n   FULL TRACEBACK:")
    traceback.print_exc()

print("\n" + "=" * 60)
print("DEBUG COMPLETE")
print("=" * 60)
