"""
Portfolio Analytics for Morgan Stanley Global Markets
Comprehensive portfolio analysis including positions, exposure, and performance metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import warnings
import os

from config import COMPLIANCE_LIMITS, REPORTING_CONFIG

logger = logging.getLogger(__name__)

class PortfolioAnalytics:
    """
    Comprehensive portfolio analytics for Morgan Stanley Global Markets.
    Handles position analysis, exposure calculations, and performance metrics.
    """
    
    def __init__(self):
        self.compliance_limits = COMPLIANCE_LIMITS
        self.reporting_config = REPORTING_CONFIG
        self.sample_data_path = 'sample_data'
    
    def load_portfolio_data(self, portfolio_id: str = 'PORTFOLIO_001') -> pd.DataFrame:
        """Load portfolio data from sample datasets."""
        try:
            # Load portfolio positions
            portfolio_file = os.path.join(self.sample_data_path, 'portfolio_positions.csv')
            if os.path.exists(portfolio_file):
                portfolio_data = pd.read_csv(portfolio_file)
                # Filter by portfolio if needed
                if portfolio_id:
                    portfolio_data = portfolio_data[portfolio_data['portfolio_id'] == portfolio_id]
                return portfolio_data
            else:
                logger.warning("Portfolio data file not found. Run sample_data.py first.")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading portfolio data: {e}")
            return pd.DataFrame()
    
    def load_trade_history(self, portfolio_id: str = 'PORTFOLIO_001', 
                          start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Load trade history from sample datasets."""
        try:
            trade_file = os.path.join(self.sample_data_path, 'trade_history.csv')
            if os.path.exists(trade_file):
                trades_data = pd.read_csv(trade_file)
                
                # Filter by portfolio
                if portfolio_id:
                    trades_data = trades_data[trades_data['portfolio_id'] == portfolio_id]
                
                # Filter by date range if provided
                if start_date and end_date:
                    trades_data['trade_date'] = pd.to_datetime(trades_data['trade_date'])
                    trades_data = trades_data[
                        (trades_data['trade_date'] >= start_date) & 
                        (trades_data['trade_date'] <= end_date)
                    ]
                
                return trades_data
            else:
                logger.warning("Trade history file not found. Run sample_data.py first.")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading trade history: {e}")
            return pd.DataFrame()
    
    def analyze_portfolio_positions(self, portfolio_id: str = 'PORTFOLIO_001', 
                                  as_of_date: str = None) -> Dict:
        """
        Comprehensive portfolio position analysis using real sample data.
        
        Args:
            portfolio_id: Portfolio identifier
            as_of_date: Date for analysis (default: current date)
        
        Returns:
            Dictionary containing position analysis results
        """
        try:
            # Load portfolio data
            portfolio_data = self.load_portfolio_data(portfolio_id)
            
            if portfolio_data.empty:
                logger.warning(f"No portfolio data found for {portfolio_id}")
                return {}
            
            # Calculate key metrics
            analysis = {
                'portfolio_id': portfolio_id,
                'as_of_date': as_of_date or datetime.now().strftime('%Y-%m-%d'),
                'total_positions': len(portfolio_data),
                'total_market_value': portfolio_data['market_value'].sum(),
                'total_cost_basis': portfolio_data['cost_basis'].sum(),
                'total_unrealized_pnl': portfolio_data['unrealized_pnl'].sum(),
                'total_realized_pnl': portfolio_data['realized_pnl'].sum(),
                'position_analysis': self._analyze_position_details(portfolio_data),
                'exposure_analysis': self._analyze_exposures(portfolio_data),
                'concentration_analysis': self._analyze_concentration(portfolio_data),
                'compliance_flags': self._check_compliance_flags(portfolio_data),
                'positions': portfolio_data.to_dict('records')
            }
            
            logger.info(f"Portfolio analysis completed for {portfolio_id}: {len(portfolio_data)} positions")
            return analysis
            
        except Exception as e:
            logger.error(f"Portfolio analysis failed for {portfolio_id}: {e}")
            raise
    
    def _analyze_position_details(self, portfolio_data: pd.DataFrame) -> Dict:
        """Analyze individual position details and characteristics."""
        analysis = {
            'largest_positions': portfolio_data.nlargest(10, 'market_value')[['symbol', 'market_value', 'unrealized_pnl']].to_dict('records'),
            'best_performers': portfolio_data.nlargest(10, 'unrealized_pnl')[['symbol', 'market_value', 'unrealized_pnl']].to_dict('records'),
            'worst_performers': portfolio_data.nsmallest(10, 'unrealized_pnl')[['symbol', 'market_value', 'unrealized_pnl']].to_dict('records'),
            'position_size_distribution': {
                'large': len(portfolio_data[portfolio_data['market_value'] > 1000000]),
                'medium': len(portfolio_data[(portfolio_data['market_value'] > 100000) & (portfolio_data['market_value'] <= 1000000)]),
                'small': len(portfolio_data[portfolio_data['market_value'] <= 100000])
            }
        }
        return analysis
    
    def _analyze_exposures(self, portfolio_data: pd.DataFrame) -> Dict:
        """Analyze portfolio exposures by sector, region, and currency."""
        exposures = {}
        
        # Sector exposure
        if 'sector' in portfolio_data.columns and portfolio_data['sector'].notna().any():
            sector_exposure = portfolio_data.groupby('sector').agg({
                'market_value': 'sum',
                'unrealized_pnl': 'sum'
            }).reset_index()
            sector_exposure['weight'] = sector_exposure['market_value'] / sector_exposure['market_value'].sum()
            exposures['sector'] = sector_exposure.to_dict('records')
        
        # Region exposure
        if 'region' in portfolio_data.columns and portfolio_data['region'].notna().any():
            region_exposure = portfolio_data.groupby('region').agg({
                'market_value': 'sum',
                'unrealized_pnl': 'sum'
            }).reset_index()
            region_exposure['weight'] = region_exposure['market_value'] / region_exposure['market_value'].sum()
            exposures['region'] = region_exposure.to_dict('records')
        
        # Currency exposure
        if 'currency' in portfolio_data.columns:
            currency_exposure = portfolio_data.groupby('currency').agg({
                'market_value': 'sum'
            }).reset_index()
            currency_exposure['weight'] = currency_exposure['market_value'] / currency_exposure['market_value'].sum()
            exposures['currency'] = currency_exposure.to_dict('records')
        
        return exposures
    
    def _analyze_concentration(self, portfolio_data: pd.DataFrame) -> Dict:
        """Analyze portfolio concentration and diversification metrics."""
        total_value = portfolio_data['market_value'].sum()
        
        # Herfindahl-Hirschman Index (HHI) for concentration
        weights = portfolio_data['market_value'] / total_value
        hhi = (weights ** 2).sum()
        
        # Top 5 positions concentration
        top_5_concentration = portfolio_data.nlargest(5, 'market_value')['market_value'].sum() / total_value
        
        # Top 10 positions concentration
        top_10_concentration = portfolio_data.nlargest(10, 'market_value')['market_value'].sum() / total_value
        
        analysis = {
            'herfindahl_index': hhi,
            'concentration_level': self._classify_concentration(hhi),
            'top_5_concentration': top_5_concentration,
            'top_10_concentration': top_10_concentration,
            'effective_number_of_positions': 1 / hhi if hhi > 0 else 0,
            'diversification_score': self._calculate_diversification_score(hhi)
        }
        
        return analysis
    
    def _classify_concentration(self, hhi: float) -> str:
        """Classify portfolio concentration level based on HHI."""
        if hhi < 0.15:
            return "Well Diversified"
        elif hhi < 0.25:
            return "Moderately Diversified"
        elif hhi < 0.50:
            return "Concentrated"
        else:
            return "Highly Concentrated"
    
    def _calculate_diversification_score(self, hhi: float) -> float:
        """Calculate diversification score (0-100, higher is better)."""
        # Normalize HHI to 0-100 scale where 0 is highly concentrated
        score = max(0, 100 * (1 - hhi))
        return round(score, 2)
    
    def _check_compliance_flags(self, portfolio_data: pd.DataFrame) -> List[Dict]:
        """Check for compliance flags and violations."""
        flags = []
        
        # Check for large positions
        large_positions = portfolio_data[portfolio_data['market_value'] > self.compliance_limits['max_position_size']]
        for _, pos in large_positions.iterrows():
            flags.append({
                'type': 'LARGE_POSITION',
                'symbol': pos['symbol'],
                'market_value': pos['market_value'],
                'limit': self.compliance_limits['max_position_size'],
                'severity': 'HIGH',
                'description': f"Position size {pos['market_value']:,.0f} exceeds limit of {self.compliance_limits['max_position_size']:,.0f}"
            })
        
        # Check sector concentration
        if 'sector' in portfolio_data.columns:
            sector_exposure = portfolio_data.groupby('sector')['market_value'].sum()
            for sector, exposure in sector_exposure.items():
                weight = exposure / portfolio_data['market_value'].sum()
                if weight > self.compliance_limits['max_sector_exposure']:
                    flags.append({
                        'type': 'SECTOR_CONCENTRATION',
                        'sector': sector,
                        'exposure': weight,
                        'limit': self.compliance_limits['max_sector_exposure'],
                        'severity': 'MEDIUM',
                        'description': f"Sector {sector} exposure {weight:.1%} exceeds limit of {self.compliance_limits['max_sector_exposure']:.1%}"
                    })
        
        return flags
    
    def get_sector_exposure_analysis(self, portfolio_id: str = 'PORTFOLIO_001') -> pd.DataFrame:
        """Get detailed sector exposure analysis."""
        portfolio_data = self.load_portfolio_data(portfolio_id)
        if portfolio_data.empty:
            return pd.DataFrame()
        
        sector_exposure = portfolio_data.groupby('sector').agg({
            'market_value': 'sum',
            'unrealized_pnl': 'sum',
            'symbol': 'count'
        }).reset_index()
        sector_exposure['weight'] = sector_exposure['market_value'] / sector_exposure['market_value'].sum()
        sector_exposure['position_count'] = sector_exposure['symbol']
        sector_exposure = sector_exposure.drop('symbol', axis=1)
        
        return sector_exposure
    
    def calculate_portfolio_metrics(self, portfolio_id: str = 'PORTFOLIO_001', 
                                  start_date: str = None, end_date: str = None) -> Dict:
        """Calculate comprehensive portfolio performance metrics."""
        try:
            # Load trade history
            trades_df = self.load_trade_history(portfolio_id, start_date, end_date)
            
            if trades_df.empty:
                return {'error': 'No trade data available for the specified period'}
            
            # Calculate trading metrics
            metrics = {
                'total_trades': len(trades_df),
                'buy_trades': len(trades_df[trades_df['side'] == 'BUY']),
                'sell_trades': len(trades_df[trades_df['side'] == 'SELL']),
                'total_notional': trades_df['notional_value'].sum(),
                'total_commission': trades_df['commission'].sum(),
                'average_trade_size': trades_df['notional_value'].mean(),
                'trading_activity_by_day': trades_df.groupby('trade_date').size().to_dict(),
                'execution_venue_breakdown': trades_df['execution_venue'].value_counts().to_dict(),
                'strategy_breakdown': trades_df['strategy'].value_counts().to_dict(),
                'trader_breakdown': trades_df['trader_id'].value_counts().to_dict()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Portfolio metrics calculation failed: {e}")
            raise
    
    def generate_portfolio_summary_report(self, portfolio_id: str = 'PORTFOLIO_001') -> Dict:
        """Generate comprehensive portfolio summary report."""
        try:
            # Get portfolio analysis
            portfolio_analysis = self.analyze_portfolio_positions(portfolio_id)
            
            # Get trading metrics (last 30 days)
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            trading_metrics = self.calculate_portfolio_metrics(portfolio_id, start_date, end_date)
            
            # Compile report
            report = {
                'portfolio_id': portfolio_id,
                'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'portfolio_summary': {
                    'total_positions': portfolio_analysis.get('total_positions', 0),
                    'total_market_value': portfolio_analysis.get('total_market_value', 0),
                    'total_unrealized_pnl': portfolio_analysis.get('total_unrealized_pnl', 0),
                    'total_realized_pnl': portfolio_analysis.get('total_realized_pnl', 0)
                },
                'concentration_analysis': portfolio_analysis.get('concentration_analysis', {}),
                'exposure_analysis': portfolio_analysis.get('exposure_analysis', {}),
                'compliance_status': {
                    'flags_count': len(portfolio_analysis.get('compliance_flags', [])),
                    'flags': portfolio_analysis.get('compliance_flags', [])
                },
                'trading_activity': trading_metrics,
                'key_insights': self._generate_key_insights(portfolio_analysis, trading_metrics)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Portfolio summary report generation failed: {e}")
            raise
    
    def _generate_key_insights(self, portfolio_analysis: Dict, trading_metrics: Dict) -> List[str]:
        """Generate key insights from portfolio and trading analysis."""
        insights = []
        
        # Portfolio insights
        total_value = portfolio_analysis.get('total_market_value', 0)
        total_pnl = portfolio_analysis.get('total_unrealized_pnl', 0)
        
        if total_value > 0:
            pnl_percentage = (total_pnl / total_value) * 100
            if pnl_percentage > 5:
                insights.append(f"Portfolio showing strong performance with {pnl_percentage:.1f}% unrealized P&L")
            elif pnl_percentage < -5:
                insights.append(f"Portfolio underperforming with {pnl_percentage:.1f}% unrealized P&L")
        
        # Concentration insights
        concentration = portfolio_analysis.get('concentration_analysis', {})
        hhi = concentration.get('herfindahl_index', 0)
        if hhi > 0.25:
            insights.append("Portfolio shows high concentration - consider diversification strategies")
        elif hhi < 0.15:
            insights.append("Portfolio is well diversified - good risk management")
        
        # Trading insights
        if trading_metrics.get('total_trades', 0) > 50:
            insights.append("High trading activity detected - review trading costs and strategy")
        
        # Compliance insights
        flags_count = len(portfolio_analysis.get('compliance_flags', []))
        if flags_count > 0:
            insights.append(f"{flags_count} compliance flags detected - immediate attention required")
        else:
            insights.append("All compliance checks passed - portfolio within limits")
        
        return insights
