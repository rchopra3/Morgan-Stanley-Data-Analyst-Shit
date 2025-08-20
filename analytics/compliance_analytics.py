"""
Compliance Analytics for Morgan Stanley Global Markets
Comprehensive compliance monitoring and regulatory reporting.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import warnings

from config import COMPLIANCE_LIMITS, MS_CONFIG
from database.queries import ComplianceQueries
from database.connections import db_manager

logger = logging.getLogger(__name__)

class ComplianceAnalytics:
    """
    Comprehensive compliance analytics for Morgan Stanley Global Markets.
    Handles compliance monitoring, regulatory reporting, and audit trails.
    """
    
    def __init__(self):
        self.compliance_limits = COMPLIANCE_LIMITS
        self.ms_config = MS_CONFIG
        self.audit_trail = self.ms_config['audit_trail']
    
    def monitor_position_limits(self, portfolio_id: str = None) -> Dict:
        """
        Monitor position limits and identify breaches.
        
        Args:
            portfolio_id: Specific portfolio to monitor (None for all portfolios)
        
        Returns:
            Dictionary containing compliance status and violations
        """
        try:
            query = ComplianceQueries.get_position_limit_breaches(portfolio_id)
            breaches_df = db_manager.execute_query('compliance', query)
            
            if breaches_df.empty:
                return {
                    'status': 'COMPLIANT',
                    'breaches': [],
                    'warnings': [],
                    'monitoring_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # Categorize by severity
            breaches = breaches_df[breaches_df['compliance_status'] == 'BREACH'].to_dict('records')
            warnings = breaches_df[breaches_df['compliance_status'] == 'WARNING'].to_dict('records')
            
            # Calculate compliance metrics
            total_positions = len(breaches_df)
            breach_count = len(breaches)
            warning_count = len(warnings)
            
            compliance_score = max(0, 100 - (breach_count * 10) - (warning_count * 5))
            
            result = {
                'status': 'NON_COMPLIANT' if breach_count > 0 else 'WARNING' if warning_count > 0 else 'COMPLIANT',
                'compliance_score': compliance_score,
                'total_positions_monitored': total_positions,
                'breach_count': breach_count,
                'warning_count': warning_count,
                'breaches': breaches,
                'warnings': warnings,
                'monitoring_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'portfolio_id': portfolio_id
            }
            
            # Log compliance status
            if breach_count > 0:
                logger.warning(f"Position limit breaches detected: {breach_count} violations")
            elif warning_count > 0:
                logger.info(f"Position limit warnings: {warning_count} items require attention")
            else:
                logger.info("All position limits are within compliance")
            
            return result
            
        except Exception as e:
            logger.error(f"Position limit monitoring failed: {e}")
            raise
    
    def monitor_large_trades(self, threshold: float = None, start_date: str = None, 
                            end_date: str = None) -> Dict:
        """
        Monitor large trades for compliance review requirements.
        
        Args:
            threshold: Notional threshold for large trades
            start_date: Start date for monitoring period
            end_date: End date for monitoring period
        """
        try:
            threshold = threshold or 1000000  # Default $1M threshold
            start_date = start_date or (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            end_date = end_date or datetime.now().strftime('%Y-%m-%d')
            
            query = ComplianceQueries.get_large_trades(threshold, start_date, end_date)
            large_trades_df = db_manager.execute_query('compliance', query)
            
            if large_trades_df.empty:
                return {
                    'status': 'NO_LARGE_TRADES',
                    'threshold': threshold,
                    'period': f"{start_date} to {end_date}",
                    'trades': [],
                    'monitoring_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # Analyze large trades
            total_large_trades = len(large_trades_df)
            total_notional = large_trades_df['notional_value'].sum()
            avg_trade_size = large_trades_df['notional_value'].mean()
            
            # Identify trades requiring compliance review
            review_required = large_trades_df[large_trades_df['compliance_review_required'] == True]
            review_count = len(review_required)
            
            # Group by trader and execution venue
            trader_breakdown = large_trades_df.groupby('trader_id').agg({
                'notional_value': ['count', 'sum', 'mean']
            }).round(2)
            
            venue_breakdown = large_trades_df['execution_venue'].value_counts().to_dict()
            
            result = {
                'status': 'LARGE_TRADES_DETECTED',
                'threshold': threshold,
                'period': f"{start_date} to {end_date}",
                'total_large_trades': total_large_trades,
                'total_notional': total_notional,
                'average_trade_size': avg_trade_size,
                'compliance_review_required': review_count,
                'trader_breakdown': trader_breakdown.to_dict(),
                'venue_breakdown': venue_breakdown,
                'trades': large_trades_df.to_dict('records'),
                'monitoring_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            logger.info(f"Large trade monitoring completed: {total_large_trades} trades above {threshold:,.0f}")
            return result
            
        except Exception as e:
            logger.error(f"Large trade monitoring failed: {e}")
            raise
    
    def detect_wash_trades(self, start_date: str, end_date: str) -> Dict:
        """
        Detect potential wash trades (same day buy/sell of same security).
        
        Args:
            start_date: Start date for monitoring period
            end_date: End date for monitoring period
        """
        try:
            query = ComplianceQueries.get_wash_trades(start_date, end_date)
            wash_trades_df = db_manager.execute_query('compliance', query)
            
            if wash_trades_df.empty:
                return {
                    'status': 'NO_WASH_TRADES_DETECTED',
                    'period': f"{start_date} to {end_date}",
                    'potential_wash_trades': [],
                    'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # Analyze wash trade patterns
            total_potential_wash = len(wash_trades_df)
            
            # Group by symbol to identify patterns
            symbol_analysis = wash_trades_df.groupby('symbol').agg({
                'portfolio_1': 'count',
                'price_diff': ['mean', 'min', 'max']
            }).round(4)
            
            # Identify high-risk patterns
            high_risk_trades = wash_trades_df[
                (wash_trades_df['price_diff'] < 0.01) &  # Very small price difference
                (wash_trades_df['qty_1'] == wash_trades_df['qty_2'])  # Same quantity
            ]
            
            result = {
                'status': 'WASH_TRADES_DETECTED',
                'period': f"{start_date} to {end_date}",
                'total_potential_wash': total_potential_wash,
                'high_risk_count': len(high_risk_trades),
                'symbol_analysis': symbol_analysis.to_dict(),
                'high_risk_trades': high_risk_trades.to_dict('records'),
                'all_potential_wash': wash_trades_df.to_dict('records'),
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if total_potential_wash > 0:
                logger.warning(f"Potential wash trades detected: {total_potential_wash} instances")
            
            return result
            
        except Exception as e:
            logger.error(f"Wash trade detection failed: {e}")
            raise
    
    def generate_regulatory_report(self, report_date: str, report_type: str = '13F') -> Dict:
        """
        Generate regulatory reporting data (Form 13F, Form PF, etc.).
        
        Args:
            report_date: Date for regulatory report
            report_type: Type of regulatory report
        """
        try:
            query = ComplianceQueries.get_regulatory_reporting_data(report_date)
            reporting_data = db_manager.execute_query('compliance', query)
            
            if reporting_data.empty:
                return {
                    'status': 'NO_DATA_AVAILABLE',
                    'report_type': report_type,
                    'report_date': report_date,
                    'data': [],
                    'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # Calculate reporting metrics
            total_portfolios = reporting_data['portfolio_id'].nunique()
            total_positions = len(reporting_data)
            total_market_value = reporting_data['market_value'].sum()
            
            # Security type breakdown
            security_breakdown = reporting_data['security_type'].value_counts().to_dict()
            
            # Currency breakdown
            currency_breakdown = reporting_data['currency'].value_counts().to_dict()
            
            # Sector breakdown (if available)
            sector_breakdown = {}
            if 'sector' in reporting_data.columns:
                sector_breakdown = reporting_data['sector'].value_counts().to_dict()
            
            result = {
                'status': 'REPORT_GENERATED',
                'report_type': report_type,
                'report_date': report_date,
                'total_portfolios': total_portfolios,
                'total_positions': total_positions,
                'total_market_value': total_market_value,
                'security_breakdown': security_breakdown,
                'currency_breakdown': currency_breakdown,
                'sector_breakdown': sector_breakdown,
                'data': reporting_data.to_dict('records'),
                'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'compliance_contact': self.ms_config['compliance_contact']
            }
            
            logger.info(f"Regulatory report generated: {report_type} for {report_date}")
            return result
            
        except Exception as e:
            logger.error(f"Regulatory report generation failed: {e}")
            raise
    
    def calculate_compliance_metrics(self, portfolio_id: str = None) -> Dict:
        """Calculate comprehensive compliance metrics and scores."""
        try:
            # Get position limit status
            position_status = self.monitor_position_limits(portfolio_id)
            
            # Get large trade status (last 30 days)
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            large_trade_status = self.monitor_large_trades(start_date=start_date, end_date=end_date)
            
            # Calculate overall compliance score
            position_score = position_status.get('compliance_score', 100)
            
            # Large trade compliance score (penalty for trades requiring review)
            large_trade_score = 100
            if large_trade_status.get('status') == 'LARGE_TRADES_DETECTED':
                review_required = large_trade_status.get('compliance_review_required', 0)
                large_trade_score = max(0, 100 - (review_required * 5))
            
            # Overall compliance score (weighted average)
            overall_score = (position_score * 0.7) + (large_trade_score * 0.3)
            
            result = {
                'portfolio_id': portfolio_id,
                'overall_compliance_score': round(overall_score, 2),
                'position_limit_score': position_score,
                'large_trade_score': large_trade_score,
                'position_limits': position_status,
                'large_trades': large_trade_status,
                'compliance_level': self._classify_compliance_level(overall_score),
                'calculation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'next_review_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Compliance metrics calculation failed: {e}")
            raise
    
    def _classify_compliance_level(self, score: float) -> str:
        """Classify compliance level based on score."""
        if score >= 95:
            return "EXCELLENT"
        elif score >= 85:
            return "GOOD"
        elif score >= 75:
            return "SATISFACTORY"
        elif score >= 65:
            return "NEEDS_IMPROVEMENT"
        else:
            return "NON_COMPLIANT"
    
    def generate_compliance_summary(self, portfolio_ids: List[str] = None) -> Dict:
        """Generate compliance summary across multiple portfolios."""
        try:
            if portfolio_ids is None:
                # Get all portfolios (this would require additional query)
                portfolio_ids = ['PORTFOLIO_001', 'PORTFOLIO_002']  # Placeholder
            
            compliance_summary = {}
            overall_scores = []
            
            for portfolio_id in portfolio_ids:
                portfolio_compliance = self.calculate_compliance_metrics(portfolio_id)
                compliance_summary[portfolio_id] = portfolio_compliance
                overall_scores.append(portfolio_compliance['overall_compliance_score'])
            
            # Calculate aggregate metrics
            avg_compliance_score = np.mean(overall_scores)
            portfolios_at_risk = len([s for s in overall_scores if s < 75])
            
            summary = {
                'total_portfolios': len(portfolio_ids),
                'average_compliance_score': round(avg_compliance_score, 2),
                'portfolios_at_risk': portfolios_at_risk,
                'overall_compliance_level': self._classify_compliance_level(avg_compliance_score),
                'portfolio_details': compliance_summary,
                'summary_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'next_escalation_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Compliance summary generation failed: {e}")
            raise
