#!/bin/bash

# Cookie Run: Kingdom Team Optimizer - Web UI Launcher

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "======================================================================"
echo "🍪 Cookie Run: Kingdom Team Optimizer - Web UI"
echo "======================================================================"
echo ""
echo "Starting Flask web server..."
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask not found. Installing..."
    pip3 install flask --break-system-packages
    echo ""
fi

# Change to the web_ui directory and start the application
cd "$DIR"
python3 app.py
