"""
Morgan Stanley Global Markets Analytics - Configuration
Centralized configuration for database connections, API endpoints, and compliance settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DATABASE_CONFIG = {
    'trading_system': {
        'host': os.getenv('TRADING_DB_HOST', 'localhost'),
        'port': os.getenv('TRADING_DB_PORT', '5432'),
        'database': os.getenv('TRADING_DB_NAME', 'trading_system'),
        'user': os.getenv('TRADING_DB_USER', 'analytics_user'),
        'password': os.getenv('TRADING_DB_PASSWORD', ''),
    },
    'risk_management': {
        'host': os.getenv('RISK_DB_HOST', 'localhost'),
        'port': os.getenv('RISK_DB_PORT', '5432'),
        'database': os.getenv('RISK_DB_NAME', 'risk_management'),
        'user': os.getenv('RISK_DB_USER', 'risk_user'),
        'password': os.getenv('RISK_DB_PASSWORD', ''),
    },
    'compliance': {
        'host': os.getenv('COMPLIANCE_DB_HOST', 'localhost'),
        'port': os.getenv('COMPLIANCE_DB_PORT', '5432'),
        'database': os.getenv('COMPLIANCE_DB_NAME', 'compliance'),
        'user': os.getenv('COMPLIANCE_DB_USER', 'compliance_user'),
        'password': os.getenv('COMPLIANCE_DB_PASSWORD', ''),
    }
}

# API Configuration
API_CONFIG = {
    'bloomberg': {
        'api_key': os.getenv('BLOOMBERG_API_KEY', ''),
        'base_url': os.getenv('BLOOMBERG_BASE_URL', 'https://api.bloomberg.com'),
    },
    'quandl': {
        'api_key': os.getenv('QUANDL_API_KEY', ''),
    },
    'fred': {
        'api_key': os.getenv('FRED_API_KEY', ''),
    }
}

# Compliance & Risk Limits
COMPLIANCE_LIMITS = {
    'max_position_size': 10000000,  # $10M max position
    'max_sector_exposure': 0.25,    # 25% max sector exposure
    'max_region_exposure': 0.40,    # 40% max region exposure
    'var_confidence_level': 0.99,   # 99% VaR confidence
    'var_time_horizon': 1,          # 1-day VaR
    'max_drawdown': 0.15,           # 15% max drawdown
}

# Trading Parameters
TRADING_PARAMS = {
    'default_currency': 'USD',
    'trading_hours': {
        'start': '09:30',
        'end': '16:00',
        'timezone': 'America/New_York'
    },
    'benchmark_indices': ['SPY', 'QQQ', 'IWM', 'EFA', 'EEM']
}

# Reporting Configuration
REPORTING_CONFIG = {
    'output_directory': 'reports/',
    'chart_style': 'seaborn-v0_8',
    'default_figsize': (12, 8),
    'dpi': 300,
    'date_format': '%Y-%m-%d',
    'currency_format': '${:,.2f}',
    'percentage_format': '{:.2%}'
}

# Morgan Stanley Specific
MS_CONFIG = {
    'firm_name': 'Morgan Stanley',
    'division': 'Global Markets',
    'team': 'Analytics',
    'compliance_contact': 'compliance@morganstanley.com',
    'risk_contact': 'risk@morganstanley.com',
    'audit_trail': True,
    'data_retention_days': 2555,  # 7 years for regulatory compliance
}
