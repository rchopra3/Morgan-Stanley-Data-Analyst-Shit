"""
SQL Query Templates for Morgan Stanley Global Markets Analytics
Pre-built queries for common trading, risk, and compliance data extraction needs.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd

class TradingQueries:
    """SQL queries for trading system data extraction."""
    
    @staticmethod
    def get_portfolio_positions(portfolio_id: str, as_of_date: str = None) -> str:
        """
        Get current portfolio positions with market data.
        
        Args:
            portfolio_id: Portfolio identifier
            as_of_date: Date for position snapshot (default: current date)
        """
        if not as_of_date:
            as_of_date = datetime.now().strftime('%Y-%m-%d')
            
        return f"""
        SELECT 
            p.symbol,
            p.quantity,
            p.cost_basis,
            p.market_value,
            p.unrealized_pnl,
            p.realized_pnl,
            p.sector,
            p.region,
            p.currency,
            p.last_updated,
            m.current_price,
            m.daily_return,
            m.volatility_30d
        FROM positions p
        LEFT JOIN market_data m ON p.symbol = m.symbol
        WHERE p.portfolio_id = '{portfolio_id}'
        AND p.as_of_date = '{as_of_date}'
        AND p.quantity != 0
        ORDER BY p.market_value DESC
        """
    
    @staticmethod
    def get_trade_history(portfolio_id: str, start_date: str, end_date: str) -> str:
        """Get trade history for portfolio over date range."""
        return f"""
        SELECT 
            t.trade_id,
            t.symbol,
            t.trade_date,
            t.side,
            t.quantity,
            t.price,
            t.notional_value,
            t.commission,
            t.trader_id,
            t.strategy,
            t.execution_venue
        FROM trades t
        WHERE t.portfolio_id = '{portfolio_id}'
        AND t.trade_date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY t.trade_date DESC, t.trade_id
        """
    
    @staticmethod
 def get_client_exposure(client_id: str) -> str:
        """Get total exposure by client across all portfolios."""
        return f"""
        SELECT 
            p.portfolio_id,
            p.portfolio_name,
            SUM(p.market_value) as total_market_value,
            COUNT(DISTINCT p.symbol) as unique_positions,
            p.currency
        FROM positions p
        JOIN portfolios pf ON p.portfolio_id = pf.portfolio_id
        WHERE pf.client_id = '{client_id}'
        AND p.quantity != 0
        GROUP BY p.portfolio_id, p.portfolio_name, p.currency
        ORDER BY total_market_value DESC
        """
    
    @staticmethod
    def get_sector_exposure(portfolio_id: str) -> str:
        """Get sector exposure breakdown for portfolio."""
        return f"""
        SELECT 
            p.sector,
            SUM(p.market_value) as sector_value,
            SUM(p.market_value) / SUM(SUM(p.market_value)) OVER () as sector_weight,
            COUNT(DISTINCT p.symbol) as position_count
        FROM positions p
        WHERE p.portfolio_id = '{portfolio_id}'
        AND p.quantity != 0
        AND p.sector IS NOT NULL
        GROUP BY p.sector
        ORDER BY sector_value DESC
        """

class RiskQueries:
    """SQL queries for risk management data extraction."""
    
    @staticmethod
    def get_var_calculation(portfolio_id: str, confidence_level: float = 0.99, 
                           time_horizon: int = 1) -> str:
        """Get VaR calculation data for portfolio."""
        return f"""
        SELECT 
            p.symbol,
            p.market_value,
            p.quantity,
            m.volatility_30d,
            m.beta_to_sp500,
            m.correlation_to_portfolio,
            p.sector,
            p.region
        FROM positions p
        LEFT JOIN market_data m ON p.symbol = m.symbol
        WHERE p.portfolio_id = '{portfolio_id}'
        AND p.quantity != 0
        AND m.volatility_30d IS NOT NULL
        ORDER BY p.market_value DESC
        """
    
    @staticmethod
    def get_stress_test_scenarios() -> str:
        """Get predefined stress test scenarios."""
        return """
        SELECT 
            scenario_id,
            scenario_name,
            description,
            equity_shock,
            interest_rate_shock,
            credit_spread_shock,
            currency_shock,
            volatility_shock
        FROM stress_test_scenarios
        WHERE is_active = true
        ORDER BY scenario_id
        """
    
    @staticmethod
    def get_risk_limits(portfolio_id: str) -> str:
        """Get risk limits and current utilization for portfolio."""
        return f"""
        SELECT 
            rl.limit_type,
            rl.limit_value,
            rl.currency,
            rl.warning_threshold,
            rl.breach_threshold,
            COALESCE(cu.current_utilization, 0) as current_utilization,
            CASE 
                WHEN cu.current_utilization > rl.breach_threshold THEN 'BREACH'
                WHEN cu.current_utilization > rl.warning_threshold THEN 'WARNING'
                ELSE 'OK'
            END as status
        FROM risk_limits rl
        LEFT JOIN current_utilization cu ON rl.limit_id = cu.limit_id
        WHERE rl.portfolio_id = '{portfolio_id}'
        ORDER BY rl.limit_type
        """

class ComplianceQueries:
    """SQL queries for compliance monitoring and reporting."""
    
    @staticmethod
    def get_position_limit_breaches(portfolio_id: str = None) -> str:
        """Get all position limit breaches across portfolios."""
        portfolio_filter = f"AND p.portfolio_id = '{portfolio_id}'" if portfolio_id else ""
        
        return f"""
        SELECT 
            p.portfolio_id,
            p.symbol,
            p.quantity,
            p.market_value,
            pl.limit_value,
            pl.limit_type,
            p.last_updated,
            CASE 
                WHEN p.market_value > pl.limit_value THEN 'BREACH'
                WHEN p.market_value > pl.limit_value * 0.8 THEN 'WARNING'
                ELSE 'OK'
            END as compliance_status
        FROM positions p
        JOIN position_limits pl ON p.symbol = pl.symbol
        WHERE p.quantity != 0
        {portfolio_filter}
        AND p.market_value > pl.limit_value * 0.8
        ORDER BY p.market_value DESC
        """
    
    @staticmethod
    def get_large_trades(threshold: float = 1000000, start_date: str = None, 
                         end_date: str = None) -> str:
        """Get trades above specified notional threshold."""
        date_filter = ""
        if start_date and end_date:
            date_filter = f"AND t.trade_date BETWEEN '{start_date}' AND '{end_date}'"
        elif start_date:
            date_filter = f"AND t.trade_date >= '{start_date}'"
        
        return f"""
        SELECT 
            t.trade_id,
            t.portfolio_id,
            t.symbol,
            t.trade_date,
            t.side,
            t.quantity,
            t.price,
            t.notional_value,
            t.trader_id,
            t.execution_venue,
            t.compliance_review_required
        FROM trades t
        WHERE t.notional_value >= {threshold}
        {date_filter}
        ORDER BY t.notional_value DESC, t.trade_date DESC
        """
    
    @staticmethod
    def get_wash_trades(start_date: str, end_date: str) -> str:
        """Identify potential wash trades (same day buy/sell of same security)."""
        return f"""
        SELECT 
            t1.symbol,
            t1.portfolio_id as portfolio_1,
            t2.portfolio_id as portfolio_2,
            t1.trade_date,
            t1.side as side_1,
            t2.side as side_2,
            t1.quantity as qty_1,
            t2.quantity as qty_2,
            t1.price as price_1,
            t2.price as price_2,
            ABS(t1.price - t2.price) as price_diff
        FROM trades t1
        JOIN trades t2 ON t1.symbol = t2.symbol 
            AND t1.trade_date = t2.trade_date
            AND t1.portfolio_id != t2.portfolio_id
            AND t1.side != t2.side
        WHERE t1.trade_date BETWEEN '{start_date}' AND '{end_date}'
        AND t1.portfolio_id < t2.portfolio_id  -- Avoid duplicates
        ORDER BY t1.trade_date, t1.symbol
        """
    
    @staticmethod
    def get_regulatory_reporting_data(report_date: str) -> str:
        """Get data required for regulatory reporting (e.g., Form PF, 13F)."""
        return f"""
        SELECT 
            p.portfolio_id,
            p.symbol,
            p.quantity,
            p.market_value,
            p.cost_basis,
            p.sector,
            p.region,
            p.currency,
            p.last_updated,
            s.security_type,
            s.cusip,
            s.isin
        FROM positions p
        JOIN securities s ON p.symbol = s.symbol
        WHERE p.as_of_date = '{report_date}'
        AND p.quantity != 0
        ORDER BY p.portfolio_id, p.market_value DESC
        """

class AnalyticsQueries:
    """SQL queries for advanced analytics and reporting."""
    
    @staticmethod
    def get_performance_attribution(portfolio_id: str, start_date: str, end_date: str) -> str:
        """Get performance attribution breakdown by factor."""
        return f"""
        SELECT 
            pa.factor_name,
            pa.factor_return,
            pa.factor_weight,
            pa.contribution,
            pa.attribution_date
        FROM performance_attribution pa
        WHERE pa.portfolio_id = '{portfolio_id}'
        AND pa.attribution_date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY pa.attribution_date DESC, ABS(pa.contribution) DESC
        """
    
    @staticmethod
    def get_correlation_matrix(portfolio_id: str, lookback_days: int = 252) -> str:
        """Get correlation matrix data for portfolio positions."""
        return f"""
        SELECT 
            p1.symbol as symbol_1,
            p2.symbol as symbol_2,
            cm.correlation_value,
            cm.correlation_date,
            cm.lookback_period
        FROM correlation_matrix cm
        JOIN positions p1 ON cm.symbol_1 = p1.symbol
        JOIN positions p2 ON cm.symbol_2 = p2.symbol
        WHERE p1.portfolio_id = '{portfolio_id}'
        AND p2.portfolio_id = '{portfolio_id}'
        AND cm.lookback_period = {lookback_days}
        AND cm.correlation_date = (
            SELECT MAX(correlation_date) 
            FROM correlation_matrix 
            WHERE lookback_period = {lookback_days}
        )
        ORDER BY ABS(cm.correlation_value) DESC
        """
