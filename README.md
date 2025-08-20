# Morgan Stanley Global Markets Analytics

A comprehensive analytics framework for Morgan Stanley's Global Markets Analytics team, providing portfolio analysis, risk management, compliance monitoring, and performance analytics capabilities.

## 🎯 Overview

This framework supports Morgan Stanley's Global Markets Analytics team in:
- **Portfolio Analysis**: Position analysis, exposure calculations, and concentration metrics
- **Risk Management**: VaR calculations, stress testing, and risk metrics
- **Compliance Monitoring**: Position limits, large trades, and regulatory reporting
- **Performance Analytics**: Attribution analysis, benchmarking, and risk-adjusted metrics
- **Professional Visualization**: Business-ready charts for traders, risk managers, and executives

## 🏗️ Architecture

```
Morgan Stanley Data Analyst Shit/
├── config.py                 # Configuration and Morgan Stanley settings
├── requirements.txt          # Python dependencies
├── main_analytics.py        # Main analytics execution script
├── database/                 # Database connectivity and queries
│   ├── __init__.py
│   ├── connections.py       # Database connection management
│   └── queries.py           # SQL query templates
├── analytics/               # Core analytics modules
│   ├── __init__.py
│   ├── portfolio_analytics.py    # Portfolio analysis
│   ├── risk_analytics.py         # Risk management
│   ├── compliance_analytics.py   # Compliance monitoring
│   └── performance_analytics.py  # Performance analytics
├── visualization/           # Charting and visualization
│   ├── __init__.py
│   └── charts.py           # Professional charting utilities
└── reports/                # Generated reports and charts
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd "Morgan Stanley Data Analyst Shit"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your database credentials:

```env
# Database Configuration
TRADING_DB_HOST=localhost
TRADING_DB_PORT=5432
TRADING_DB_NAME=trading_system
TRADING_DB_USER=analytics_user
TRADING_DB_PASSWORD=your_password

RISK_DB_HOST=localhost
RISK_DB_PORT=5432
RISK_DB_NAME=risk_management
RISK_DB_USER=risk_user
RISK_DB_PASSWORD=your_password

COMPLIANCE_DB_HOST=localhost
COMPLIANCE_DB_PORT=5432
COMPLIANCE_DB_NAME=compliance
COMPLIANCE_DB_USER=compliance_user
COMPLIANCE_DB_PASSWORD=your_password

# API Keys (optional)
BLOOMBERG_API_KEY=your_bloomberg_key
QUANDL_API_KEY=your_quandl_key
FRED_API_KEY=your_fred_key
```

### 3. Run Analytics

```bash
# Execute comprehensive analytics
python main_analytics.py
```

## 📊 Core Capabilities

### Portfolio Analytics

- **Position Analysis**: Comprehensive position breakdown with market values and P&L
- **Exposure Analysis**: Sector, region, and currency exposure calculations
- **Concentration Metrics**: Herfindahl-Hirschman Index (HHI) and diversification scoring
- **Compliance Monitoring**: Automatic flagging of limit breaches and concentration issues

```python
from analytics.portfolio_analytics import PortfolioAnalytics

portfolio_analytics = PortfolioAnalytics()
analysis = portfolio_analytics.analyze_portfolio_positions('PORTFOLIO_001')
```

### Risk Analytics

- **Value at Risk (VaR)**: Parametric, historical, and Monte Carlo methods
- **Expected Shortfall**: Conditional VaR calculations
- **Stress Testing**: Predefined and custom stress scenarios
- **Risk Metrics**: Volatility, beta exposure, and correlation analysis

```python
from analytics.risk_analytics import RiskAnalytics

risk_analytics = RiskAnalytics()
var_result = risk_analytics.calculate_portfolio_var('PORTFOLIO_001', method='parametric')
stress_result = risk_analytics.perform_stress_test('PORTFOLIO_001')
```

### Compliance Analytics

- **Position Limits**: Real-time monitoring of position size limits
- **Large Trade Detection**: Automated flagging of trades above thresholds
- **Wash Trade Detection**: Identification of potential wash trading patterns
- **Regulatory Reporting**: Form 13F, Form PF, and other regulatory requirements

```python
from analytics.compliance_analytics import ComplianceAnalytics

compliance_analytics = ComplianceAnalytics()
position_status = compliance_analytics.monitor_position_limits('PORTFOLIO_001')
large_trades = compliance_analytics.monitor_large_trades(threshold=1000000)
```

### Performance Analytics

- **Performance Metrics**: Total return, volatility, Sharpe ratio, and drawdown
- **Risk-Adjusted Metrics**: Sortino, Calmar, Treynor ratios, and Jensen's Alpha
- **Performance Attribution**: Factor-based return decomposition
- **Benchmark Comparison**: Relative performance vs. market indices

```python
from analytics.performance_analytics import PerformanceAnalytics

performance_analytics = PerformanceAnalytics()
metrics = performance_analytics.calculate_performance_metrics('PORTFOLIO_001', '2024-01-01', '2024-12-31')
report = performance_analytics.generate_performance_report('PORTFOLIO_001', '2024-01-01', '2024-12-31')
```

## 📈 Visualization

Professional, business-ready charts for all analytics outputs:

```python
from visualization.charts import PortfolioCharts, RiskCharts, ComplianceCharts, PerformanceCharts

# Portfolio charts
portfolio_charts = PortfolioCharts()
fig = portfolio_charts.create_portfolio_overview(portfolio_data)
fig.savefig('portfolio_overview.png', dpi=300, bbox_inches='tight')

# Risk charts
risk_charts = RiskCharts()
fig = risk_charts.create_var_analysis(var_data)
fig.savefig('var_analysis.png', dpi=300, bbox_inches='tight')
```

## 🗄️ Database Integration

The framework supports multiple database systems:

- **Trading System**: Portfolio positions, trades, and market data
- **Risk Management**: VaR calculations, stress test scenarios, and risk limits
- **Compliance**: Position limits, trade monitoring, and regulatory data

### SQL Query Templates

Pre-built SQL queries for common analytics needs:

```python
from database.queries import TradingQueries, RiskQueries, ComplianceQueries

# Get portfolio positions
query = TradingQueries.get_portfolio_positions('PORTFOLIO_001')
positions_df = db_manager.execute_query('trading_system', query)

# Get VaR calculation data
query = RiskQueries.get_var_calculation('PORTFOLIO_001')
var_data = db_manager.execute_query('risk_management', query)
```

## 🔧 Configuration

### Compliance Limits

Configurable risk and compliance thresholds:

```python
COMPLIANCE_LIMITS = {
    'max_position_size': 10000000,      # $10M max position
    'max_sector_exposure': 0.25,        # 25% max sector exposure
    'max_region_exposure': 0.40,        # 40% max region exposure
    'var_confidence_level': 0.99,       # 99% VaR confidence
    'var_time_horizon': 1,              # 1-day VaR
    'max_drawdown': 0.15,               # 15% max drawdown
}
```

### Reporting Configuration

Professional chart styling and output settings:

```python
REPORTING_CONFIG = {
    'output_directory': 'reports/',
    'chart_style': 'seaborn-v0_8',
    'default_figsize': (12, 8),
    'dpi': 300,
    'date_format': '%Y-%m-%d',
    'currency_format': '${:,.2f}',
    'percentage_format': '{:.2%}'
}
```

## 📋 Usage Examples

### Daily Portfolio Review

```python
# Run daily portfolio analysis
portfolio_analysis = run_portfolio_analysis()

# Check for compliance issues
if portfolio_analysis.get('compliance_flags'):
    logger.warning(f"Compliance issues detected: {len(portfolio_analysis['compliance_flags'])}")
    
# Generate daily report
generate_visualizations(portfolio_analysis)
```

### Risk Monitoring

```python
# Calculate daily VaR
var_result = risk_analytics.calculate_portfolio_var('PORTFOLIO_001')

# Check against limits
if var_result['var_percentage'] > 0.05:  # 5% VaR limit
    logger.warning("VaR exceeds daily limit!")
    
# Run stress tests
stress_result = risk_analytics.perform_stress_test('PORTFOLIO_001')
```

### Compliance Reporting

```python
# Generate regulatory report
regulatory_report = compliance_analytics.generate_regulatory_report(
    report_date='2024-12-31',
    report_type='13F'
)

# Monitor position limits
compliance_status = compliance_analytics.monitor_position_limits('PORTFOLIO_001')
if compliance_status['status'] != 'COMPLIANT':
    # Escalate to compliance team
    escalate_compliance_issue(compliance_status)
```

## 🚨 Compliance & Audit

- **Audit Trail**: All analytics operations are logged with timestamps
- **Data Retention**: 7-year data retention for regulatory compliance
- **Documentation**: Comprehensive code documentation for audit reviews
- **Validation**: Built-in data validation and error handling

## 🔒 Security Features

- **Environment Variables**: Sensitive credentials stored in `.env` files
- **Database Security**: Secure database connections with connection pooling
- **Access Control**: Role-based access to different database systems
- **Logging**: Comprehensive logging for security monitoring

## 📚 Dependencies

Core dependencies include:
- **Data Science**: pandas, numpy, scipy
- **Financial Analytics**: yfinance, empyrical, pyfolio
- **Risk Management**: scikit-learn, cvxpy
- **Visualization**: matplotlib, seaborn, plotly
- **Database**: sqlalchemy, psycopg2-binary
- **Compliance**: openpyxl, xlsxwriter, reportlab

## 🤝 Contributing

1. Follow Morgan Stanley coding standards
2. Ensure all changes are documented
3. Run compliance checks before committing
4. Update audit trail for any changes
5. Test with sample data before production

## 📞 Support

- **Team**: Global Markets Analytics
- **Division**: Global Markets
- **Compliance**: compliance@morganstanley.com
- **Risk**: risk@morganstanley.com

## 📄 License

Internal Morgan Stanley tool - not for external distribution.

---

**Note**: This framework is designed for Morgan Stanley's internal use and includes compliance monitoring, risk management, and regulatory reporting capabilities required for institutional trading operations.
