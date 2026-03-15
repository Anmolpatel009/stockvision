#!/bin/bash
# Start script for Railpack deployment
# Installs Python3 and dependencies, then starts the Node.js server

echo "Starting Quant-Kernel Dashboard..."

# Determine package manager and install python3 and pip
if command -v apt-get &> /dev/null; then
    echo "Using apt-get to install Python3..."
    apt-get update && apt-get install -y python3 python3-pip
elif command -v apk &> /dev/null; then
    echo "Using apk to install Python3..."
    apk add --no-cache python3 py3-pip
else
    echo "Unknown package manager. Attempting to install python3 and pip via generic method..."
    # This is a fallback and may not work in all environments
    # We'll try to install using the system's package manager if possible
    exit 1
fi

# Change to dashboard directory and install Python dependencies
cd dashboard
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies from requirements.txt..."
    pip3 install -r requirements.txt
else
    echo "No requirements.txt found in dashboard directory."
fi

# Start the Node.js server
echo "Starting Node.js server..."
node server.js