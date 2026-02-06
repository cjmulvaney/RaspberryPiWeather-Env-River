#!/bin/bash
# Install Homebrew and Python to fix Tkinter compatibility

echo "=================================================="
echo "Montana River Dashboard - Mac Setup"
echo "=================================================="
echo ""
echo "This script will:"
echo "1. Install Homebrew (if needed)"
echo "2. Install Python 3.11 with compatible Tkinter"
echo "3. Install required Python packages"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 1
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo ""
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "✓ Homebrew already installed"
fi

echo ""
echo "Installing Python 3.11 with Tkinter..."
brew install python@3.11 python-tk@3.11

echo ""
echo "Installing Python packages..."
/opt/homebrew/bin/pip3 install requests matplotlib

echo ""
echo "=================================================="
echo "Installation Complete!"
echo "=================================================="
echo ""
echo "To run the dashboard, use:"
echo ""
echo "  /opt/homebrew/bin/python3 main.py"
echo ""
echo "Or create an alias in ~/.zshrc:"
echo ""
echo "  alias dashboard='/opt/homebrew/bin/python3 ~/Desktop/Vibecoding/RPiTouchscreenProject/river-dashboard/main.py'"
echo ""
echo "Then run with: dashboard"
echo ""
echo "Testing Tkinter..."
/opt/homebrew/bin/python3 -c "import tkinter; print('✓ Tkinter version:', tkinter.TkVersion)"

echo ""
echo "Ready to launch dashboard!"
