#!/bin/bash
# Script to run Tkinter app in a headless environment using Xvfb

# Start Xvfb if not already running

if ! pgrep Xvfb > /dev/null; then
    Xvfb :99 -screen 0 1280x1024x24 -nolisten tcp -ac &
    sleep 2 # Give Xvfb time to start
fi

export DISPLAY=:99

python "final code.py"
