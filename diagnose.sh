#!/bin/bash
# Complete diagnostic script for Raspberry Pi issues

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     MONTANA RIVER DASHBOARD - DIAGNOSTIC TOOL              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Save to file
LOGFILE="diagnostic_report.txt"
exec > >(tee "$LOGFILE") 2>&1

echo "Date: $(date)"
echo ""

# System Info
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. SYSTEM INFORMATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "OS: $(uname -a)"
if [ -f /etc/os-release ]; then
    source /etc/os-release
    echo "Distribution: $PRETTY_NAME"
fi
echo ""

# Python Info
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. PYTHON INFORMATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Python version: $(python3 --version)"
echo "Python location: $(which python3)"
echo "Pip version: $(pip3 --version)"
echo ""

# Display Info
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. DISPLAY INFORMATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DISPLAY variable: ${DISPLAY:-NOT SET}"
echo "X11 running: $(ps aux | grep -v grep | grep -q Xorg && echo 'YES' || echo 'NO')"
echo ""

# Tkinter Test
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. TKINTER TEST"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 -c "import tkinter; print('✓ Tkinter imported'); print('Tk version:', tkinter.TkVersion)" 2>&1 || echo "✗ Tkinter failed"
echo ""

# I2C Check
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. I2C HARDWARE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -e /dev/i2c-1 ]; then
    echo "✓ I2C device found: /dev/i2c-1"
    if command -v i2cdetect &> /dev/null; then
        echo "I2C devices detected:"
        sudo i2cdetect -y 1
    else
        echo "i2cdetect not installed (sudo apt-get install i2c-tools)"
    fi
else
    echo "✗ I2C device not found"
    echo "  Enable with: sudo raspi-config > Interface Options > I2C"
fi
echo ""

# Installed Packages
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. PYTHON PACKAGES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Required packages:"
for pkg in requests matplotlib adafruit-blinka adafruit-circuitpython-bme680 adafruit-circuitpython-pm25; do
    if pip3 show "$pkg" &>/dev/null; then
        version=$(pip3 show "$pkg" | grep Version | cut -d' ' -f2)
        echo "  ✓ $pkg ($version)"
    else
        echo "  ✗ $pkg NOT INSTALLED"
    fi
done
echo ""

# Module Import Test
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. MODULE IMPORT TEST"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cd "$(dirname "$0")"
python3 << 'PYEOF'
import sys
modules = [
    "tkinter",
    "requests",
    "matplotlib",
    "config.constants",
    "data.database",
    "data.sensors",
    "data.usgs_api",
    "data.nws_api",
]
for mod in modules:
    try:
        __import__(mod)
        print(f"  ✓ {mod}")
    except Exception as e:
        print(f"  ✗ {mod}: {e}")
PYEOF
echo ""

# Test Sensor Libraries
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "8. SENSOR LIBRARY TEST"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 << 'PYEOF'
try:
    import board
    print("  ✓ board")
except Exception as e:
    print(f"  ✗ board: {e}")

try:
    import adafruit_bme680
    print("  ✓ adafruit_bme680")
except Exception as e:
    print(f"  ✗ adafruit_bme680: {e}")

try:
    from adafruit_pm25.i2c import PM25_I2C
    print("  ✓ adafruit_pm25")
except Exception as e:
    print(f"  ✗ adafruit_pm25: {e}")
PYEOF
echo ""

# Try to run main.py
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "9. MAIN APPLICATION TEST"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Attempting to import main.py..."
python3 -c "import main; print('✓ main.py imported successfully')" 2>&1
if [ $? -eq 0 ]; then
    echo "✓ No import errors detected"
else
    echo "✗ Import failed - see error above"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "10. SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Diagnostic report saved to: $LOGFILE"
echo ""
echo "NEXT STEPS:"
echo ""

# Check for common issues
ISSUES=0

# Check DISPLAY
if [ -z "$DISPLAY" ]; then
    echo "⚠️  DISPLAY not set - are you running via SSH?"
    echo "   Solution: Run on Pi desktop directly, or:"
    echo "   export DISPLAY=:0"
    echo ""
    ISSUES=$((ISSUES+1))
fi

# Check Tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "⚠️  Tkinter not working"
    echo "   Solution: sudo apt-get install python3-tk"
    echo ""
    ISSUES=$((ISSUES+1))
fi

# Check requests
if ! pip3 show requests &>/dev/null; then
    echo "⚠️  requests package missing"
    echo "   Solution: pip3 install requests"
    echo ""
    ISSUES=$((ISSUES+1))
fi

# Check matplotlib
if ! pip3 show matplotlib &>/dev/null; then
    echo "⚠️  matplotlib package missing"
    echo "   Solution: pip3 install matplotlib"
    echo ""
    ISSUES=$((ISSUES+1))
fi

if [ $ISSUES -eq 0 ]; then
    echo "✓ No obvious issues detected!"
    echo ""
    echo "If the app still crashes, run:"
    echo "  python3 debug_pi.py"
    echo ""
    echo "Or capture the full error:"
    echo "  python3 main.py 2>&1 | tee error.log"
else
    echo "Found $ISSUES potential issue(s) - fix them and try again!"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Share $LOGFILE for help troubleshooting!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
