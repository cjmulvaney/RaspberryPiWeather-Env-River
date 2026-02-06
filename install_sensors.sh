#!/bin/bash
# Install sensor libraries on Raspberry Pi

echo "=" * 60
echo "Installing Sensor Libraries for Raspberry Pi"
echo "="* 60
echo ""

# Check if running on Raspberry Pi
if [[ $(uname -m) != "aarch64" ]] && [[ $(uname -m) != "armv7l" ]]; then
    echo "⚠️  Warning: This doesn't appear to be a Raspberry Pi"
    echo "   Detected architecture: $(uname -m)"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Installing Adafruit sensor libraries..."
echo ""

# Install Blinka (Adafruit CircuitPython support)
echo "1/3: Installing adafruit-blinka..."
pip3 install adafruit-blinka

# Install BME680 library
echo ""
echo "2/3: Installing adafruit-circuitpython-bme680..."
pip3 install adafruit-circuitpython-bme680

# Install PMSA003I library
echo ""
echo "3/3: Installing adafruit-circuitpython-pm25..."
pip3 install adafruit-circuitpython-pm25

echo ""
echo "=" * 60
echo "Installation Complete!"
echo "=" * 60
echo ""
echo "Next steps:"
echo "1. Ensure I2C is enabled:"
echo "   sudo raspi-config > Interface Options > I2C > Enable"
echo ""
echo "2. Check I2C devices are detected:"
echo "   sudo i2cdetect -y 1"
echo "   (Should show 0x12 for PMSA003I and 0x77 for BME680)"
echo ""
echo "3. Verify wiring:"
echo "   BME680:   SDA→GPIO2, SCL→GPIO3, VCC→3.3V, GND→GND"
echo "   PMSA003I: SDA→GPIO2, SCL→GPIO3, VCC→5V, GND→GND"
echo ""
echo "4. Test sensors:"
echo "   python3 test_sensors.py"
echo ""
echo "5. Run dashboard:"
echo "   python3 main.py"
echo ""
echo "=" * 60
