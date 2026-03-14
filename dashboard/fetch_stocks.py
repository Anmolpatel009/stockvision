#!/usr/bin/env python3
"""
Yahoo Finance Data Fetcher for Quant-Kernel Dashboard
Fetches real-time stock data from NSE (India) and US markets
"""

import yfinance as yf
import json
import time
import numpy as np
import requests
import sys

# NSE (India) and US Stock symbols
STOCKS = [
    # NSE India Stocks (use .NS suffix for Yahoo Finance)
    'RELIANCE.NS',  # Reliance Industries
    'TCS.NS',       # Tata Consultancy Services
    'INFY.NS',      # Infosys
    'HDFCBANK.NS',  # HDFC Bank
    'SBIN.NS',      # State Bank of India
    'ITC.NS',       # ITC Limited
    'WIPRO.NS',     # Wipro
    'ADANIPORTS.NS', # Adani Ports
    
    # US Stocks
    'AAPL',         # Apple
    'GOOGL',        # Google
    'MSFT',         # Microsoft
    'TSLA',         # Tesla
    
    # Crypto
    'BTC-USD',      # Bitcoin
    'ETH-USD',      # Ethereum
]

# API endpoint
API_URL = 'http://localhost:3000/api/metrics'

def fetch_stock_data():
    """Fetch real-time stock data from Yahoo Finance."""
    prices = {}
    
    for symbol in STOCKS:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get current price
            price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            if price is None:
                price = info.get('previousClose', 0)
                
            # Get other metrics
            volume = info.get('volume', 0)
            market_cap = info.get('marketCap', 0)
            change = info.get('regularMarketChange', 0)
            change_percent = info.get('regularMarketChangePercent', 0)
            day_high = info.get('dayHigh', 0)
            day_low = info.get('dayLow', 0)
            fifty_two_week_high = info.get('fiftyTwoWeekHigh', 0)
            fifty_two_week_low = info.get('fiftyTwoWeekLow', 0)
            
            # Get company name
            short_name = info.get('shortName', info.get('longName', symbol))
            
            prices[symbol] = {
                'price': float(price) if price else 0,
                'volume': int(volume) if volume else 0,
                'marketCap': int(market_cap) if market_cap else 0,
                'change': float(change) if change else 0,
                'changePercent': float(change_percent) if change_percent else 0,
                'dayHigh': float(day_high) if day_high else 0,
                'dayLow': float(day_low) if day_low else 0,
                '52wHigh': float(fifty_two_week_high) if fifty_two_week_high else 0,
                '52wLow': float(fifty_two_week_low) if fifty_two_week_low else 0,
                'name': short_name[:30] if short_name else symbol,
                'exchange': 'NSE' if '.NS' in symbol else ('CRYPTO' if '-' in symbol else 'US')
            }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            prices[symbol] = {
                'price': 0, 'volume': 0, 'marketCap': 0,
                'change': 0, 'changePercent': 0, 'dayHigh': 0, 'dayLow': 0,
                '52wHigh': 0, '52wLow': 0, 'name': symbol,
                'exchange': 'NSE' if '.NS' in symbol else 'US'
            }
    
    return prices

def calculate_metrics(prices):
    """Calculate portfolio metrics from stock prices."""
    prices_list = [p.get('price', 0) for p in prices.values() if p.get('price', 0) > 0]
    
    # Calculate volatility (as system load)
    if len(prices_list) > 1:
        returns = np.diff(prices_list) / prices_list[:-1]
        volatility = float(np.std(returns) * np.sqrt(252)) * 100
    else:
        volatility = 0
    
    # Determine regime
    if volatility > 30:
        regime = 'volatile'
        regime_desc = 'High Volatility - Uncertain Markets'
    elif volatility > 15:
        regime = 'trend_strong'
        regime_desc = 'Strong Trend - Directional Markets'
    elif volatility > 8:
        regime = 'trend_weak'
        regime_desc = 'Weak Trend - Moderate Direction'
    elif volatility > 3:
        regime = 'sideways'
        regime_desc = 'Sideways - Range Bound'
    else:
        regime = 'mean_reverting'
        regime_desc = 'Mean Reverting - Calm Markets'
    
    # Calculate tick rate
    tick_rate = sum(p.get('volume', 0) for p in prices.values()) / 1000000
    
    # Count exchanges
    nse_count = sum(1 for p in prices.values() if p.get('exchange') == 'NSE')
    us_count = sum(1 for p in prices.values() if p.get('exchange') == 'US')
    crypto_count = sum(1 for p in prices.values() if p.get('exchange') == 'CRYPTO')
    
    # Calculate total portfolio value
    total_value = sum(p.get('price', 0) * 100 for p in prices.values() if p.get('price', 0) > 0)
    
    import random
    metrics = {
        'timestamp': int(time.time() * 1000),
        'stocks': STOCKS,
        'prices': prices,
        'cpu_usage': min(100, 30 + volatility * 1.5 + random.random() * 20),
        'memory_usage': 40 + random.random() * 30,
        'system_load': min(100, volatility),
        'tick_rate': tick_rate,
        'regime': regime,
        'regime_desc': regime_desc,
        'spectral_radius': volatility / 100,
        'condition_number': random.uniform(5, 50),
        'sharpe_ratio': random.uniform(0.5, 2.0) if regime != 'volatile' else random.uniform(-0.5, 1.0),
        'max_drawdown': random.uniform(-0.15, 0),
        'total_pnl': random.uniform(-5000, 15000),
        'open_positions': len([s for s in prices.values() if s.get('price', 0) > 0]),
        
        # Additional info
        'total_stocks': len(prices),
        'nse_count': nse_count,
        'us_count': us_count,
        'crypto_count': crypto_count,
        'portfolio_value': total_value,
        'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return metrics

def send_metrics(metrics):
    """Send metrics to the web server."""
    try:
        requests.post(API_URL, json=metrics, timeout=5)
    except Exception as e:
        print(f"Error sending metrics: {e}")

def main():
    print("=" * 60)
    print("QUANT-KERNEL - Real-Time Stock Data Fetcher")
    print("=" * 60)
    print(f"Tracking {len(STOCKS)} stocks:")
    print(f"  NSE India: {', '.join([s for s in STOCKS if '.NS' in s])}")
    print(f"  US: {', '.join([s for s in STOCKS if s in ['AAPL','GOOGL','MSFT','TSLA']])}")
    print(f"  Crypto: BTC-USD, ETH-USD")
    print("=" * 60)
    print("Press Ctrl+C to stop\n")
    
    while True:
        try:
            prices = fetch_stock_data()
            metrics = calculate_metrics(prices)
            
            # Print summary
            print(f"[{time.strftime('%H:%M:%S')}] ")
            print(f"  Market Regime: {metrics['regime_desc']}")
            print(f"  System Load (Volatility): {metrics['system_load']:.1f}%")
            print(f"  Stocks: {metrics['total_stocks']} | NSE: {metrics['nse_count']} | US: {metrics['us_count']} | Crypto: {metrics['crypto_count']}")
            print()
            
            # Send to server
            send_metrics(metrics)
            
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\nStopping...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
