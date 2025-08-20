"""
Sample Data Generator for Morgan Stanley Analytics
Creates realistic datasets for portfolio analysis, risk management, and compliance monitoring.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_portfolio_data():
    """Generate realistic portfolio positions data."""
    
    # Sample portfolio positions
    positions_data = {
        'portfolio_id': ['PORTFOLIO_001'] * 50,
        'symbol': [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'ADBE', 'CRM',
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'PNC', 'TFC', 'COF',
            'JNJ', 'PFE', 'UNH', 'ABT', 'TMO', 'DHR', 'BMY', 'ABBV', 'AMGN', 'GILD',
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'PSX', 'VLO', 'MPC', 'HAL', 'BKR',
            'SPY', 'QQQ', 'IWM', 'EFA', 'EEM', 'AGG', 'TLT', 'GLD', 'VNQ', 'XLE'
        ],
        'quantity': [random.randint(100, 5000) for _ in range(50)],
        'cost_basis': [round(random.uniform(50, 500), 2) for _ in range(50)],
        'market_value': [round(random.uniform(10000, 500000), 2) for _ in range(50)],
        'unrealized_pnl': [round(random.uniform(-50000, 100000), 2) for _ in range(50)],
        'realized_pnl': [round(random.uniform(-10000, 20000), 2) for _ in range(50)],
        'sector': [
            'Technology', 'Technology', 'Technology', 'Technology', 'Technology', 'Technology', 'Technology', 'Technology', 'Technology', 'Technology',
            'Financial', 'Financial', 'Financial', 'Financial', 'Financial', 'Financial', 'Financial', 'Financial', 'Financial', 'Financial',
            'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare',
            'Energy', 'Energy', 'Energy', 'Energy', 'Energy', 'Energy', 'Energy', 'Energy', 'Energy', 'Energy',
            'ETF', 'ETF', 'ETF', 'ETF', 'ETF', 'ETF', 'ETF', 'ETF', 'ETF', 'ETF'
        ],
        'region': ['US'] * 50,
        'currency': ['USD'] * 50,
        'last_updated': [datetime.now().strftime('%Y-%m-%d')] * 50
    }
    
    # Add market data
    positions_data.update({
        'current_price': [round(random.uniform(50, 500), 2) for _ in range(50)],
        'daily_return': [round(random.uniform(-0.05, 0.05), 4) for _ in range(50)],
        'volatility_30d': [round(random.uniform(0.15, 0.45), 4) for _ in range(50)],
        'beta_to_sp500': [round(random.uniform(0.5, 2.0), 2) for _ in range(50)]
    })
    
    return pd.DataFrame(positions_data)

def generate_trade_history():
    """Generate realistic trade history data."""
    
    # Generate dates for last 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    trades = []
    for date in dates:
        # Generate 1-5 trades per day
        num_trades = random.randint(1, 5)
        for _ in range(num_trades):
            trade = {
                'trade_id': f"TRADE_{len(trades):06d}",
                'portfolio_id': 'PORTFOLIO_001',
                'symbol': random.choice(['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'BAC', 'JNJ', 'XOM']),
                'trade_date': date.strftime('%Y-%m-%d'),
                'side': random.choice(['BUY', 'SELL']),
                'quantity': random.randint(100, 2000),
                'price': round(random.uniform(50, 500), 2),
                'notional_value': 0,  # Will calculate below
                'commission': round(random.uniform(5, 50), 2),
                'trader_id': f"TRADER_{random.randint(1, 5):03d}",
                'strategy': random.choice(['Momentum', 'Value', 'Growth', 'Arbitrage', 'Hedging']),
                'execution_venue': random.choice(['NYSE', 'NASDAQ', 'ARCA', 'BATS', 'Direct'])
            }
            trade['notional_value'] = trade['quantity'] * trade['price']
            trades.append(trade)
    
    return pd.DataFrame(trades)

def generate_market_data():
    """Generate realistic market data for risk calculations."""
    
    # Generate 252 trading days (1 year)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, freq='B')  # Business days
    
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'BAC', 'JNJ', 'XOM', 'SPY']
    
    market_data = []
    for date in dates:
        for symbol in symbols:
            # Generate realistic price movements
            base_price = 100 if symbol == 'SPY' else random.uniform(50, 500)
            daily_return = np.random.normal(0.001, 0.02)  # 0.1% mean, 2% std
            price = base_price * (1 + daily_return)
            
            market_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'symbol': symbol,
                'price': round(price, 2),
                'daily_return': round(daily_return, 4),
                'volume': random.randint(1000000, 10000000),
                'volatility_30d': round(random.uniform(0.15, 0.45), 4)
            })
    
    return pd.DataFrame(market_data)

def generate_performance_attribution():
    """Generate performance attribution data."""
    
    # Generate monthly attribution data for last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    
    attribution_data = []
    for date in dates:
        # Factor returns
        factors = [
            {'factor_name': 'Stock Selection', 'factor_return': random.uniform(-0.02, 0.04), 'factor_weight': 0.6},
            {'factor_name': 'Sector Allocation', 'factor_return': random.uniform(-0.01, 0.02), 'factor_weight': 0.3},
            {'factor_name': 'Market Timing', 'factor_return': random.uniform(-0.005, 0.01), 'factor_weight': 0.1}
        ]
        
        for factor in factors:
            contribution = factor['factor_return'] * factor['factor_weight']
            attribution_data.append({
                'portfolio_id': 'PORTFOLIO_001',
                'factor_name': factor['factor_name'],
                'factor_return': round(factor['factor_return'], 4),
                'factor_weight': factor['factor_weight'],
                'contribution': round(contribution, 4),
                'attribution_date': date.strftime('%Y-%m-%d')
            })
    
    return pd.DataFrame(attribution_data)

def generate_compliance_data():
    """Generate compliance monitoring data."""
    
    # Position limits
    position_limits = []
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'BAC', 'JNJ', 'XOM']
    
    for symbol in symbols:
        limit_value = random.uniform(100000, 1000000)
        position_limits.append({
            'symbol': symbol,
            'limit_value': round(limit_value, 2),
            'limit_type': 'POSITION_SIZE',
            'currency': 'USD'
        })
    
    # Large trades (above $1M threshold)
    large_trades = []
    for i in range(15):
        trade = {
            'trade_id': f"LARGE_TRADE_{i:03d}",
            'portfolio_id': 'PORTFOLIO_001',
            'symbol': random.choice(symbols),
            'trade_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            'side': random.choice(['BUY', 'SELL']),
            'quantity': random.randint(5000, 20000),
            'price': round(random.uniform(100, 400), 2),
            'notional_value': 0,
            'trader_id': f"TRADER_{random.randint(1, 5):03d}",
            'execution_venue': random.choice(['NYSE', 'NASDAQ']),
            'compliance_review_required': random.choice([True, False])
        }
        trade['notional_value'] = trade['quantity'] * trade['price']
        large_trades.append(trade)
    
    return {
        'position_limits': pd.DataFrame(position_limits),
        'large_trades': pd.DataFrame(large_trades)
    }

def generate_stress_test_scenarios():
    """Generate stress test scenarios."""
    
    scenarios = [
        {
            'scenario_id': 'SCENARIO_001',
            'scenario_name': '2008 Financial Crisis',
            'description': 'Severe market downturn similar to 2008 financial crisis',
            'equity_shock': -0.40,
            'interest_rate_shock': 0.02,
            'credit_spread_shock': 0.05,
            'currency_shock': -0.15,
            'volatility_shock': 0.30,
            'is_active': True
        },
        {
            'scenario_id': 'SCENARIO_002',
            'scenario_name': 'COVID-19 Market Crash',
            'description': 'Rapid market decline similar to March 2020',
            'equity_shock': -0.30,
            'interest_rate_shock': -0.01,
            'credit_spread_shock': 0.03,
            'currency_shock': -0.10,
            'volatility_shock': 0.25,
            'is_active': True
        },
        {
            'scenario_id': 'SCENARIO_003',
            'scenario_name': 'Interest Rate Spike',
            'description': 'Sharp increase in interest rates',
            'equity_shock': -0.15,
            'interest_rate_shock': 0.05,
            'credit_spread_shock': 0.02,
            'currency_shock': 0.05,
            'volatility_shock': 0.20,
            'is_active': True
        }
    ]
    
    return pd.DataFrame(scenarios)

def create_sample_datasets():
    """Create all sample datasets and save them."""
    
    print("🚀 Generating Morgan Stanley Analytics Sample Datasets...")
    
    # Generate datasets
    portfolio_data = generate_portfolio_data()
    trade_history = generate_trade_history()
    market_data = generate_market_data()
    performance_attribution = generate_performance_attribution()
    compliance_data = generate_compliance_data()
    stress_scenarios = generate_stress_test_scenarios()
    
    # Save datasets
    portfolio_data.to_csv('sample_data/portfolio_positions.csv', index=False)
    trade_history.to_csv('sample_data/trade_history.csv', index=False)
    market_data.to_csv('sample_data/market_data.csv', index=False)
    performance_attribution.to_csv('sample_data/performance_attribution.csv', index=False)
    compliance_data['position_limits'].to_csv('sample_data/position_limits.csv', index=False)
    compliance_data['large_trades'].to_csv('sample_data/large_trades.csv', index=False)
    stress_scenarios.to_csv('sample_data/stress_test_scenarios.csv', index=False)
    
    print("✅ Sample datasets generated successfully!")
    print(f"📊 Portfolio Positions: {len(portfolio_data)} positions")
    print(f"📈 Trade History: {len(trade_history)} trades")
    print(f"📉 Market Data: {len(market_data)} data points")
    print(f"🎯 Performance Attribution: {len(performance_attribution)} records")
    print(f"🔒 Compliance Data: {len(compliance_data['position_limits'])} limits, {len(compliance_data['large_trades'])} large trades")
    print(f"⚡ Stress Test Scenarios: {len(stress_scenarios)} scenarios")
    
    return {
        'portfolio_data': portfolio_data,
        'trade_history': trade_history,
        'market_data': market_data,
        'performance_attribution': performance_attribution,
        'compliance_data': compliance_data,
        'stress_scenarios': stress_scenarios
    }

if __name__ == "__main__":
    # Create sample_data directory
    import os
    os.makedirs('sample_data', exist_ok=True)
    
    # Generate all datasets
    datasets = create_sample_datasets()
    
    print("\n🎉 All sample datasets are ready for Morgan Stanley Analytics!")
    print("📁 Check the 'sample_data/' directory for CSV files")
    print("🚀 You can now run the analytics with real sample data!")
