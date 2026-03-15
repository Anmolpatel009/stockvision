const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const os = require('os'); // Add this at the top of your file

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
  // 1. Detect Environment: Windows uses 'python', Linux/Mac uses 'python3'
  const pythonCommand = os.platform() === 'win32' ? 'python' : 'python3';
  console.log(`[System] Script Path Check: ${path.join(__dirname, 'fetch_stocks.py')}`);
  console.log(`[System] Attempting to start kernel using: ${pythonCommand}`);

  pythonProcess = spawn(pythonCommand, [
    path.join(__dirname, 'fetch_stocks.py')
  ], {
    cwd: __dirname,
    stdio: ['pipe', 'pipe', 'pipe'],
    // Use an unbuffered environment so logs show up immediately
    env: { ...process.env, PYTHONUNBUFFERED: '1' }
  });

  let stdoutBuffer = '';
  pythonProcess.stdout.on('data', (data) => {
    stdoutBuffer += data.toString();
    const lines = stdoutBuffer.split('\n');
    stdoutBuffer = lines.pop() || '';
    for (const line of lines) {
      if (line.trim()) console.log(`[Python] ${line}`);
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    // If it's just a warning (like yfinance deprecation), use console.warn
    console.error(`[Python Error] ${data}`);
  });

  pythonProcess.on('error', (err) => {
    console.error(`[CRITICAL] Failed to spawn ${pythonCommand}:`, err.message);
    
    if (err.code === 'ENOENT') {
      console.log('------------------------------------------------------------');
      console.log(`REALITY CHECK: The command "${pythonCommand}" was not found.`);
      console.log('1. If on Windows, ensure Python is in your PATH.');
      console.log('2. If on Linux/Oracle, run: sudo apt install python3');
      console.log('3. Try changing "python3" to "python" in server.js.');
      console.log('------------------------------------------------------------');
    }
  });

  pythonProcess.on('close', (code) => {
    console.log(`[Kernel] Process exited with code ${code}`);
    
    // Only restart if it wasn't a clean exit (code 0)
    if (code !== 0 && code !== null) {
      console.log('[Kernel] Restarting in 5s due to abnormal exit...');
      setTimeout(() => startPythonFetcher(), 5000);
    }
  });
}

// API endpoint for metrics (called by Python fetcher)
app.post('/api/metrics', (req, res) => {
  latestMetrics = { ...latestMetrics, ...req.body, timestamp: Date.now() };
  console.log(`[Server] Received metrics update - Stocks: ${Object.keys(latestMetrics.prices || {}).length}, Regime: ${latestMetrics.regime}`);
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
  startPythonFetcher();
});
