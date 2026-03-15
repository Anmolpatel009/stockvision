#!/bin/bash
# Start script for Railpack deployment
# Changes to dashboard directory and starts the Node.js server

echo "Starting Quant-Kernel Dashboard..."
cd dashboard

# Install Node.js dependencies if needed
echo "Checking Node.js dependencies..."
npm install

# Start the server
echo "Starting server..."
npm start