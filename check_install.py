#!/usr/bin/env python3
"""Quick installation checker for Raspberry Pi"""

import sys

print("=" * 60)
print("INSTALLATION CHECKER")
print("=" * 60)
print()

errors = []
warnings = []

# Check Python version
print("1. Checking Python version...")
if sys.version_info < (3, 9):
    errors.append("Python 3.9+ required, found " + sys.version)
    print(f"   ✗ Python {sys.version_info.major}.{sys.version_info.minor} (need 3.9+)")
else:
    print(f"   ✓ Python {sys.version_info.major}.{sys.version_info.minor}")

# Check required packages
print("\n2. Checking required packages...")
required = {
    'tkinter': 'python3-tk',
    'requests': 'requests',
    'matplotlib': 'matplotlib',
}

for module, package in required.items():
    try:
        __import__(module)
        print(f"   ✓ {module}")
    except ImportError:
        print(f"   ✗ {module} - install with: pip3 install {package}")
        errors.append(f"Missing package: {module}")

# Check Pi-specific packages (warnings only)
print("\n3. Checking Raspberry Pi sensor packages...")
pi_packages = {
    'board': 'adafruit-blinka',
    'adafruit_bme680': 'adafruit-circuitpython-bme680',
    'adafruit_pm25': 'adafruit-circuitpython-pm25',
}

for module, package in pi_packages.items():
    try:
        __import__(module)
        print(f"   ✓ {module}")
    except ImportError:
        print(f"   ⚠ {module} - install with: pip3 install {package}")
        warnings.append(f"Missing Pi package: {module} (OK on Mac)")

# Check display
print("\n4. Checking display...")
import os
display = os.environ.get('DISPLAY')
if display:
    print(f"   ✓ DISPLAY={display}")
else:
    print(f"   ⚠ DISPLAY not set (might fail if running via SSH)")
    warnings.append("DISPLAY not set")

# Check I2C (Pi only)
print("\n5. Checking I2C...")
if os.path.exists('/dev/i2c-1'):
    print(f"   ✓ I2C device found")
else:
    print(f"   ⚠ I2C not found (enable with raspi-config if on Pi)")
    warnings.append("I2C not enabled")

# Try to import main modules
print("\n6. Checking dashboard modules...")
sys.path.insert(0, '.')
modules_to_check = [
    'config.constants',
    'data.database',
    'data.sensors',
    'utils.platform_detect',
]

for module in modules_to_check:
    try:
        __import__(module)
        print(f"   ✓ {module}")
    except Exception as e:
        print(f"   ✗ {module}: {e}")
        errors.append(f"Module error: {module}")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if errors:
    print(f"\n❌ {len(errors)} ERROR(S) - Must fix before running:")
    for error in errors:
        print(f"   • {error}")
else:
    print("\n✅ No critical errors!")

if warnings:
    print(f"\n⚠️  {len(warnings)} WARNING(S) - May cause issues:")
    for warning in warnings:
        print(f"   • {warning}")

if not errors and not warnings:
    print("\n🎉 Everything looks good! Ready to run!")
    print("\nStart the dashboard with:")
    print("   python3 main.py")
elif not errors:
    print("\n✓ Should work, but warnings may cause issues.")
    print("  Try running: python3 main.py")
else:
    print("\n❌ Fix errors above before running.")
    print("\nQuick fixes:")
    print("  pip3 install requests matplotlib")
    if any('tkinter' in e for e in errors):
        print("  sudo apt-get install python3-tk")

print("\nFor more help, see:")
print("  - PI_TROUBLESHOOTING.md")
print("  - Run: ./diagnose.sh")
print("=" * 60)
