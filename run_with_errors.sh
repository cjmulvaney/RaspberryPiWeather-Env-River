#!/bin/bash
# Run dashboard with full error output

echo "Starting Montana River Dashboard with debug output..."
echo "========================================================"

cd "$(dirname "$0")"

# Capture all output
python3 main.py 2>&1 | tee dashboard_error.log

echo ""
echo "========================================================"
echo "Program exited. Check dashboard_error.log for details"
echo ""
echo "Last 20 lines of error log:"
tail -20 dashboard_error.log
