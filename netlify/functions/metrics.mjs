// Quant-Kernel Metrics API - Netlify Function
// Returns stock data with mock prices (with realistic variation)

const MOCK_DATA = {
  'AAPL': { price: 178.50, change: 2.35, changePercent: 1.33, volume: 52000000, marketCap: 2800000000000, dayHigh: 180.20, dayLow: 176.80, '52wHigh': 199.62, '52wLow': 124.17, name: 'Apple Inc.', exchange: 'US' },
  'GOOGL': { price: 141.80, change: -0.90, changePercent: -0.63, volume: 21000000, marketCap: 1780000000000, dayHigh: 143.50, dayLow: 140.20, '52wHigh': 153.78, '52wLow': 83.45, name: 'Alphabet Inc.', exchange: 'US' },
  'MSFT': { price: 378.90, change: 4.20, changePercent: 1.12, volume: 18000000, marketCap: 2820000000000, dayHigh: 381.00, dayLow: 375.50, '52wHigh': 384.30, '52wLow': 245.61, name: 'Microsoft Corp.', exchange: 'US' },
  'TSLA': { price: 248.50, change: -5.30, changePercent: -2.09, volume: 95000000, marketCap: 790000000000, dayHigh: 255.80, dayLow: 245.20, '52wHigh': 299.29, '52wLow': 138.80, name: 'Tesla Inc.', exchange: 'US' },
  'AMZN': { price: 178.25, change: 1.85, changePercent: 1.05, volume: 42000000, marketCap: 1850000000000, dayHigh: 180.50, dayLow: 176.00, '52wHigh': 189.77, '52wLow': 88.12, name: 'Amazon.com Inc.', exchange: 'US' },
  'BTC-USD': { price: 67500.00, change: 1250.00, changePercent: 1.89, volume: 28000000000, marketCap: 1320000000000, dayHigh: 68200.00, dayLow: 65800.00, '52wHigh': 73750.00, '52wLow': 24823.00, name: 'Bitcoin USD', exchange: 'CRYPTO' },
  'ETH-USD': { price: 3450.00, change: 85.00, changePercent: 2.53, volume: 15000000000, marketCap: 415000000000, dayHigh: 3520.00, dayLow: 3380.00, '52wHigh': 3890.00, '52wLow': 1008.00, name: 'Ethereum USD', exchange: 'CRYPTO' },
};

function generatePrices() {
  const prices = {};
  for (const [symbol, base] of Object.entries(MOCK_DATA)) {
    const variation = (Math.random() - 0.5) * 0.04; // +/- 2% variation
    const price = base.price * (1 + variation);
    const change = price - base.price + base.change * (0.5 + Math.random());
    const changePercent = (change / base.price) * 100;

    prices[symbol] = {
      ...base,
      price: parseFloat(price.toFixed(2)),
      change: parseFloat(change.toFixed(2)),
      changePercent: parseFloat(changePercent.toFixed(2)),
      dayHigh: parseFloat((base.dayHigh * (1 + Math.random() * 0.01)).toFixed(2)),
      dayLow: parseFloat((base.dayLow * (1 - Math.random() * 0.01)).toFixed(2)),
      volume: Math.floor(base.volume * (0.8 + Math.random() * 0.4)),
    };
  }
  return prices;
}

function calculateMetrics(prices) {
  const pricesList = Object.values(prices).map(p => p.price).filter(p => p > 0);

  // Calculate volatility (as system load)
  let volatility = 0;
  if (pricesList.length > 1) {
    const returns = [];
    for (let i = 1; i < pricesList.length; i++) {
      returns.push((pricesList[i] - pricesList[i - 1]) / pricesList[i - 1]);
    }
    const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
    const variance = returns.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / returns.length;
    volatility = Math.sqrt(variance) * Math.sqrt(252) * 100;
  }

  // Determine regime
  let regime, regimeDesc;
  if (volatility > 30) {
    regime = 'volatile';
    regimeDesc = 'High Volatility - Uncertain Markets';
  } else if (volatility > 15) {
    regime = 'trend_strong';
    regimeDesc = 'Strong Trend - Directional Markets';
  } else if (volatility > 8) {
    regime = 'trend_weak';
    regimeDesc = 'Weak Trend - Moderate Direction';
  } else if (volatility > 3) {
    regime = 'sideways';
    regimeDesc = 'Sideways - Range Bound';
  } else {
    regime = 'mean_reverting';
    regimeDesc = 'Mean Reverting - Calm Markets';
  }

  const tickRate = Object.values(prices).reduce((sum, p) => sum + (p.volume || 0), 0) / 1000000;
  const nseCount = Object.values(prices).filter(p => p.exchange === 'NSE').length;
  const usCount = Object.values(prices).filter(p => p.exchange === 'US').length;
  const cryptoCount = Object.values(prices).filter(p => p.exchange === 'CRYPTO').length;
  const totalValue = Object.values(prices).reduce((sum, p) => sum + (p.price > 0 ? p.price * 100 : 0), 0);

  return {
    timestamp: Date.now(),
    stocks: Object.keys(prices),
    prices,
    cpu_usage: Math.min(100, 30 + volatility * 1.5 + Math.random() * 20),
    memory_usage: 40 + Math.random() * 30,
    system_load: Math.min(100, volatility),
    tick_rate: tickRate,
    regime,
    regime_desc: regimeDesc,
    spectral_radius: volatility / 100,
    condition_number: 5 + Math.random() * 45,
    sharpe_ratio: regime !== 'volatile' ? 0.5 + Math.random() * 1.5 : -0.5 + Math.random() * 1.5,
    max_drawdown: -Math.random() * 0.15,
    total_pnl: -5000 + Math.random() * 20000,
    open_positions: Object.values(prices).filter(p => p.price > 0).length,
    total_stocks: Object.keys(prices).length,
    nse_count: nseCount,
    us_count: usCount,
    crypto_count: cryptoCount,
    portfolio_value: totalValue,
    last_updated: new Date().toISOString().replace('T', ' ').substring(0, 19),
  };
}

export default async (req) => {
  const prices = generatePrices();
  const metrics = calculateMetrics(prices);

  return new Response(JSON.stringify(metrics), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'no-cache',
    },
  });
};
