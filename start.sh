#!/bin/bash
# Start script for Railpack deployment
# Changes to dashboard directory, installs Python dependencies, and starts the Node.js server

echo "Starting Quant-Kernel Dashboard..."
cd dashboard

# Install Python requirements if they exist
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Start the Node.js server
echo "Starting server..."
node server.js