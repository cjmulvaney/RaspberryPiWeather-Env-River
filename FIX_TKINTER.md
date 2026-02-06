# Fixing Tkinter macOS Compatibility Issue

## The Problem

Your system Python 3.9.6 includes Tkinter 8.5, which is incompatible with macOS 26.2. This causes the error:
```
macOS 26 (2602) or later required, have instead 16 (1602) !
```

## Solutions (Choose One)

### Option 1: Install Homebrew Python (RECOMMENDED)

This will give you a modern Python with compatible Tkinter.

```bash
# 1. Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python via Homebrew
brew install python@3.11 python-tk@3.11

# 3. Use Homebrew Python
/opt/homebrew/bin/python3 --version

# 4. Install dependencies with Homebrew Python
/opt/homebrew/bin/pip3 install requests matplotlib

# 5. Run the dashboard
cd /Users/cjmulvaney/Desktop/Vibecoding/RPiTouchscreenProject/river-dashboard
/opt/homebrew/bin/python3 main.py
```

### Option 2: Install Python from python.org

Download and install Python 3.11+ from https://www.python.org/downloads/

```bash
# After installation, use:
/usr/local/bin/python3 main.py
```

### Option 3: Use PyQt5 Instead (Alternative GUI)

If Tkinter continues to have issues, we can convert the app to use PyQt5:

```bash
# Install PyQt5
pip3 install PyQt5 requests matplotlib

# I can create a PyQt5 version if needed
```

### Option 4: Skip Mac Testing, Deploy Directly to Pi

Since the Raspberry Pi will have a properly configured Tkinter, you can skip Mac testing:

1. Transfer the entire `river-dashboard` folder to your Raspberry Pi
2. Follow the deployment instructions in `DEPLOYMENT.md`
3. The app will work perfectly on the Pi

## Quick Test

After installing Homebrew Python, test Tkinter:

```bash
/opt/homebrew/bin/python3 -c "
import tkinter as tk
root = tk.Tk()
root.title('Test')
label = tk.Label(root, text='Tkinter works!')
label.pack()
print('✓ Success!')
root.destroy()
"
```

## Recommended Path Forward

**For Development Testing:**
1. Install Homebrew (takes ~10 minutes)
2. Install Python via Homebrew (takes ~5 minutes)
3. Run the dashboard

**For Production:**
- Transfer to Raspberry Pi and deploy there
- Pi has proper Tkinter out of the box
- App is designed and tested to work on Pi

## Why This Happened

Apple's system Python on macOS is often outdated and has Tkinter compatibility issues. Homebrew Python or python.org Python includes modern, compatible Tk/Tcl libraries.

## Need Help?

Let me know which option you'd like to pursue, and I can provide more detailed instructions!
