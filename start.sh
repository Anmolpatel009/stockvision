#!/bin/bash

# ============================================================
# Quant-Kernel Dashboard - Production Startup Script
# ============================================================

echo "------------------------------------------------------------"
echo "[System] Initializing Quant-Kernel Environment..."
echo "------------------------------------------------------------"

# 1. Navigate to the dashboard directory 
# (Ensures relative paths for fetch_stocks.py and public/ work correctly)
if [ -d "dashboard" ]; then
    cd dashboard
    echo "[System] Moved to dashboard directory."
else
    echo "[Warning] dashboard directory not found, staying in root."
fi

# 2. Verify Python Installation
# This is a reality check to ensure Nixpacks did its job.
if command -v python3 &> /dev/null; then
    echo "[System] Python3 detected: $(python3 --version)"
else
    echo "[Error] Python3 NOT found. Ensure nixpacks.toml is correct."
    exit 1
fi

# 3. Start the Node.js server
# Using 'exec' makes Node the primary process (PID 1).
# If Node crashes, Railway will immediately know and restart the container.
echo "[System] Starting Node.js server..."
echo "------------------------------------------------------------"

exec node server.js