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

from config import COMPLIANCE_LIMITS, REPORTING_CONFIG
from database.queries import TradingQueries
from database.connections import db_manager

logger = logging.getLogger(__name__)

class PortfolioAnalytics:
    """
    Comprehensive portfolio analytics for Morgan Stanley Global Markets.
    Handles position analysis, exposure calculations, and performance metrics.
    """
    
    def __init__(self):
        self.compliance_limits = COMPLIANCE_LIMITS
        self.reporting_config = REPORTING_CONFIG
    
    def analyze_portfolio_positions(self, portfolio_id: str, as_of_date: str = None) -> Dict:
        """
        Comprehensive portfolio position analysis.
        
        Args:
            portfolio_id: Portfolio identifier
            as_of_date: Date for analysis (default: current date)
        
        Returns:
            Dictionary containing position analysis results
        """
        try:
            # Get portfolio positions
            query = TradingQueries.get_portfolio_positions(portfolio_id, as_of_date)
            positions_df = db_manager.execute_query('trading_system', query)
            
            if positions_df.empty:
                logger.warning(f"No positions found for portfolio {portfolio_id}")
                return {}
            
            # Calculate key metrics
            analysis = {
                'portfolio_id': portfolio_id,
                'as_of_date': as_of_date or datetime.now().strftime('%Y-%m-%d'),
                'total_positions': len(positions_df),
                'total_market_value': positions_df['market_value'].sum(),
                'total_cost_basis': positions_df['cost_basis'].sum(),
                'total_unrealized_pnl': positions_df['unrealized_pnl'].sum(),
                'total_realized_pnl': positions_df['realized_pnl'].sum(),
                'position_analysis': self._analyze_position_details(positions_df),
                'exposure_analysis': self._analyze_exposures(positions_df),
                'concentration_analysis': self._analyze_concentration(positions_df),
                'compliance_flags': self._check_compliance_flags(positions_df)
            }
            
            logger.info(f"Portfolio analysis completed for {portfolio_id}: {len(positions_df)} positions")
            return analysis
            
        except Exception as e:
            logger.error(f"Portfolio analysis failed for {portfolio_id}: {e}")
            raise
    
    def _analyze_position_details(self, positions_df: pd.DataFrame) -> Dict:
        """Analyze individual position details and characteristics."""
        analysis = {
            'largest_positions': positions_df.nlargest(10, 'market_value')[['symbol', 'market_value', 'unrealized_pnl']].to_dict('records'),
            'best_performers': positions_df.nlargest(10, 'unrealized_pnl')[['symbol', 'market_value', 'unrealized_pnl']].to_dict('records'),
            'worst_performers': positions_df.nsmallest(10, 'unrealized_pnl')[['symbol', 'market_value', 'unrealized_pnl']].to_dict('records'),
            'position_size_distribution': {
                'large': len(positions_df[positions_df['market_value'] > 1000000]),
                'medium': len(positions_df[(positions_df['market_value'] > 100000) & (positions_df['market_value'] <= 1000000)]),
                'small': len(positions_df[positions_df['market_value'] <= 100000])
            }
        }
        return analysis
    
    def _analyze_exposures(self, positions_df: pd.DataFrame) -> Dict:
        """Analyze portfolio exposures by sector, region, and currency."""
        exposures = {}
        
        # Sector exposure
        if 'sector' in positions_df.columns and positions_df['sector'].notna().any():
            sector_exposure = positions_df.groupby('sector').agg({
                'market_value': 'sum',
                'unrealized_pnl': 'sum'
            }).reset_index()
            sector_exposure['weight'] = sector_exposure['market_value'] / sector_exposure['market_value'].sum()
            exposures['sector'] = sector_exposure.to_dict('records')
        
        # Region exposure
        if 'region' in positions_df.columns and positions_df['region'].notna().any():
            region_exposure = positions_df.groupby('region').agg({
                'market_value': 'sum',
                'unrealized_pnl': 'sum'
            }).reset_index()
            region_exposure['weight'] = region_exposure['market_value'] / region_exposure['market_value'].sum()
            exposures['region'] = region_exposure.to_dict('records')
        
        # Currency exposure
        if 'currency' in positions_df.columns:
            currency_exposure = positions_df.groupby('currency').agg({
                'market_value': 'sum'
            }).reset_index()
            currency_exposure['weight'] = currency_exposure['market_value'] / currency_exposure['market_value'].sum()
            exposures['currency'] = currency_exposure.to_dict('records')
        
        return exposures
    
    def _analyze_concentration(self, positions_df: pd.DataFrame) -> Dict:
        """Analyze portfolio concentration and diversification metrics."""
        total_value = positions_df['market_value'].sum()
        
        # Herfindahl-Hirschman Index (HHI) for concentration
        weights = positions_df['market_value'] / total_value
        hhi = (weights ** 2).sum()
        
        # Top 5 positions concentration
        top_5_concentration = positions_df.nlargest(5, 'market_value')['market_value'].sum() / total_value
        
        # Top 10 positions concentration
        top_10_concentration = positions_df.nlargest(10, 'market_value')['market_value'].sum() / total_value
        
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
    
    def _check_compliance_flags(self, positions_df: pd.DataFrame) -> List[Dict]:
        """Check for compliance flags and violations."""
        flags = []
        
        # Check for large positions
        large_positions = positions_df[positions_df['market_value'] > self.compliance_limits['max_position_size']]
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
        if 'sector' in positions_df.columns:
            sector_exposure = positions_df.groupby('sector')['market_value'].sum()
            for sector, exposure in sector_exposure.items():
                weight = exposure / positions_df['market_value'].sum()
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
    
    def get_sector_exposure_analysis(self, portfolio_id: str) -> pd.DataFrame:
        """Get detailed sector exposure analysis."""
        query = TradingQueries.get_sector_exposure(portfolio_id)
        return db_manager.execute_query('trading_system', query)
    
    def get_client_exposure_summary(self, client_id: str) -> pd.DataFrame:
        """Get client exposure summary across all portfolios."""
        query = TradingQueries.get_client_exposure(client_id)
        return db_manager.execute_query('trading_system', query)
    
    def calculate_portfolio_metrics(self, portfolio_id: str, start_date: str, end_date: str) -> Dict:
        """Calculate comprehensive portfolio performance metrics."""
        try:
            # Get trade history
            query = TradingQueries.get_trade_history(portfolio_id, start_date, end_date)
            trades_df = db_manager.execute_query('trading_system', query)
            
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
                'execution_venue_breakdown': trades_df['execution_venue'].value_counts().to_dict()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Portfolio metrics calculation failed: {e}")
            raise
