const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Store latest metrics
let latestMetrics = {
  timestamp: Date.now(),
  stocks: ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'BTC-USD', 'ETH-USD'],
  prices: {},
  cpu_usage: 0,
  memory_usage: 0,
  system_load: 0,
  tick_rate: 0,
  regime: 'unknown',
  spectral_radius: 0,
  condition_number: 1,
  sharpe_ratio: 0,
  max_drawdown: 0,
  total_pnl: 0,
  open_positions: 0
};

// Start Python fetcher
let pythonProcess = null;

function startPythonFetcher() {
  pythonProcess = spawn('nix-shell', [
    '-p', 'python3', 'python3Packages.yfinance', 'python3Packages.numpy', 'python3Packages.requests',
    '--run', 'python3 dashboard/fetch_stocks.py'
  ], {
    cwd: __dirname + '/..',
    stdio: ['pipe', 'pipe', 'pipe']
  });

  pythonProcess.stdout.on('data', (data) => {
    // Parse the printed metrics
    const lines = data.toString().trim().split('\n');
    for (const line of lines) {
      if (line.includes('Prices:')) {
        // Extract JSON from console output - skip for now
      }
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    console.log(`Python: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python fetcher exited with code ${code}`);
  });
}

// API endpoint for metrics (called by Python fetcher)
app.post('/api/metrics', (req, res) => {
  latestMetrics = { ...latestMetrics, ...req.body, timestamp: Date.now() };
  io.emit('metrics', latestMetrics);
  res.json({ success: true });
});

// API endpoint for metrics (GET)
app.get('/api/metrics', (req, res) => {
  res.json(latestMetrics);
});

// API endpoint for stock prices
app.get('/api/stocks', (req, res) => {
  res.json(latestMetrics.prices || {});
});

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
  console.log(`Quant-Kernel Dashboard running on http://localhost:${PORT}`);
  console.log(`Fetching real stock data from Yahoo Finance...`);
  
  // Start Python fetcher
  try {
    startPythonFetcher();
  } catch (e) {
    console.log('Note: Python fetcher not available. Using simulation mode.');
  }
});
