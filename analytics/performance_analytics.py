"""
Performance Analytics for Morgan Stanley Global Markets
Comprehensive performance analysis including attribution, benchmarking, and metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import warnings

from config import REPORTING_CONFIG, TRADING_PARAMS
from database.queries import AnalyticsQueries
from database.connections import db_manager

logger = logging.getLogger(__name__)

class PerformanceAnalytics:
    """
    Comprehensive performance analytics for Morgan Stanley Global Markets.
    Handles performance attribution, benchmarking, and key metrics calculation.
    """
    
    def __init__(self):
        self.reporting_config = REPORTING_CONFIG
        self.benchmark_indices = TRADING_PARAMS['benchmark_indices']
    
    def calculate_performance_metrics(self, portfolio_id: str, start_date: str, end_date: str) -> Dict:
        """
        Calculate comprehensive performance metrics for portfolio.
        
        Args:
            portfolio_id: Portfolio identifier
            start_date: Start date for performance period
            end_date: End date for performance period
        
        Returns:
            Dictionary containing performance metrics
        """
        try:
            # Get performance attribution data
            attribution_query = AnalyticsQueries.get_performance_attribution(portfolio_id, start_date, end_date)
            attribution_df = db_manager.execute_query('trading_system', attribution_query)
            
            # Calculate basic performance metrics
            metrics = {
                'portfolio_id': portfolio_id,
                'period': f"{start_date} to {end_date}",
                'total_return': self._calculate_total_return(attribution_df),
                'annualized_return': self._calculate_annualized_return(start_date, end_date, attribution_df),
                'volatility': self._calculate_volatility(attribution_df),
                'sharpe_ratio': self._calculate_sharpe_ratio(attribution_df),
                'max_drawdown': self._calculate_max_drawdown(attribution_df),
                'information_ratio': self._calculate_information_ratio(attribution_df),
                'tracking_error': self._calculate_tracking_error(attribution_df),
                'attribution_analysis': self._analyze_performance_attribution(attribution_df),
                'calculation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            logger.info(f"Performance metrics calculated for portfolio {portfolio_id}")
            return metrics
            
        except Exception as e:
            logger.error(f"Performance metrics calculation failed: {e}")
            raise
    
    def _calculate_total_return(self, attribution_df: pd.DataFrame) -> float:
        """Calculate total return from attribution data."""
        if attribution_df.empty:
            return 0.0
        
        # Sum all factor returns
        total_return = attribution_df['factor_return'].sum()
        return round(total_return, 4)
    
    def _calculate_annualized_return(self, start_date: str, end_date: str, attribution_df: pd.DataFrame) -> float:
        """Calculate annualized return."""
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            days = (end_dt - start_dt).days
            
            if days <= 0:
                return 0.0
            
            total_return = self._calculate_total_return(attribution_df)
            annualized_return = ((1 + total_return) ** (365 / days)) - 1
            
            return round(annualized_return, 4)
            
        except Exception:
            return 0.0
    
    def _calculate_volatility(self, attribution_df: pd.DataFrame) -> float:
        """Calculate portfolio volatility."""
        if attribution_df.empty:
            return 0.0
        
        # For simplicity, using factor returns to estimate volatility
        # In practice, this would use actual return time series
        returns = attribution_df['factor_return'].values
        volatility = np.std(returns) * np.sqrt(252)  # Annualized
        
        return round(volatility, 4)
    
    def _calculate_sharpe_ratio(self, attribution_df: pd.DataFrame, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio."""
        try:
            total_return = self._calculate_total_return(attribution_df)
            volatility = self._calculate_volatility(attribution_df)
            
            if volatility == 0:
                return 0.0
            
            sharpe_ratio = (total_return - risk_free_rate) / volatility
            return round(sharpe_ratio, 4)
            
        except Exception:
            return 0.0
    
    def _calculate_max_drawdown(self, attribution_df: pd.DataFrame) -> float:
        """Calculate maximum drawdown."""
        if attribution_df.empty:
            return 0.0
        
        # For simplicity, using cumulative returns to estimate drawdown
        # In practice, this would use actual NAV time series
        cumulative_returns = (1 + attribution_df['factor_return']).cumprod()
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - running_max) / running_max
        
        max_drawdown = drawdown.min()
        return round(max_drawdown, 4)
    
    def _calculate_information_ratio(self, attribution_df: pd.DataFrame) -> float:
        """Calculate information ratio (excess return / tracking error)."""
        try:
            # For simplicity, assuming benchmark return of 0
            # In practice, this would compare against actual benchmark
            excess_return = self._calculate_total_return(attribution_df)
            tracking_error = self._calculate_tracking_error(attribution_df)
            
            if tracking_error == 0:
                return 0.0
            
            information_ratio = excess_return / tracking_error
            return round(information_ratio, 4)
            
        except Exception:
            return 0.0
    
    def _calculate_tracking_error(self, attribution_df: pd.DataFrame) -> float:
        """Calculate tracking error."""
        if attribution_df.empty:
            return 0.0
        
        # For simplicity, using factor returns to estimate tracking error
        # In practice, this would compare against benchmark returns
        returns = attribution_df['factor_return'].values
        tracking_error = np.std(returns) * np.sqrt(252)  # Annualized
        
        return round(tracking_error, 4)
    
    def _analyze_performance_attribution(self, attribution_df: pd.DataFrame) -> Dict:
        """Analyze performance attribution by factor."""
        if attribution_df.empty:
            return {}
        
        # Factor contribution analysis
        factor_contributions = attribution_df.groupby('factor_name').agg({
            'factor_return': 'sum',
            'contribution': 'sum'
        }).reset_index()
        
        # Sort by absolute contribution
        factor_contributions['abs_contribution'] = abs(factor_contributions['contribution'])
        factor_contributions = factor_contributions.sort_values('abs_contribution', ascending=False)
        
        # Top contributors
        top_contributors = factor_contributions.head(5).to_dict('records')
        
        # Factor breakdown
        factor_breakdown = factor_contributions.to_dict('records')
        
        return {
            'total_factors': len(factor_contributions),
            'top_contributors': top_contributors,
            'factor_breakdown': factor_breakdown,
            'positive_contributors': len(factor_contributions[factor_contributions['contribution'] > 0]),
            'negative_contributors': len(factor_contributions[factor_contributions['contribution'] < 0])
        }
    
    def calculate_risk_adjusted_metrics(self, portfolio_id: str, start_date: str, end_date: str) -> Dict:
        """Calculate comprehensive risk-adjusted performance metrics."""
        try:
            # Get basic performance metrics
            performance_metrics = self.calculate_performance_metrics(portfolio_id, start_date, end_date)
            
            # Calculate additional risk-adjusted metrics
            total_return = performance_metrics['total_return']
            volatility = performance_metrics['volatility']
            
            # Sortino Ratio (using downside deviation)
            sortino_ratio = self._calculate_sortino_ratio(total_return, volatility)
            
            # Calmar Ratio (return / max drawdown)
            max_drawdown = performance_metrics['max_drawdown']
            calmar_ratio = self._calculate_calmar_ratio(total_return, max_drawdown)
            
            # Treynor Ratio (return / beta)
            treynor_ratio = self._calculate_treynor_ratio(total_return, 1.0)  # Assuming beta = 1.0
            
            # Jensen's Alpha (simplified)
            jensen_alpha = self._calculate_jensen_alpha(total_return, 1.0, 0.02)  # Assuming market return = 2%
            
            risk_adjusted_metrics = {
                'portfolio_id': portfolio_id,
                'period': f"{start_date} to {end_date}",
                'sharpe_ratio': performance_metrics['sharpe_ratio'],
                'sortino_ratio': sortino_ratio,
                'calmar_ratio': calmar_ratio,
                'treynor_ratio': treynor_ratio,
                'jensen_alpha': jensen_alpha,
                'information_ratio': performance_metrics['information_ratio'],
                'tracking_error': performance_metrics['tracking_error'],
                'volatility': volatility,
                'max_drawdown': max_drawdown,
                'calculation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return risk_adjusted_metrics
            
        except Exception as e:
            logger.error(f"Risk-adjusted metrics calculation failed: {e}")
            raise
    
    def _calculate_sortino_ratio(self, total_return: float, volatility: float, risk_free_rate: float = 0.02) -> float:
        """Calculate Sortino ratio."""
        try:
            if volatility == 0:
                return 0.0
            
            # For simplicity, using total volatility as downside deviation
            # In practice, this would calculate actual downside deviation
            sortino_ratio = (total_return - risk_free_rate) / volatility
            return round(sortino_ratio, 4)
            
        except Exception:
            return 0.0
    
    def _calculate_calmar_ratio(self, total_return: float, max_drawdown: float) -> float:
        """Calculate Calmar ratio."""
        try:
            if max_drawdown == 0:
                return 0.0
            
            calmar_ratio = total_return / abs(max_drawdown)
            return round(calmar_ratio, 4)
            
        except Exception:
            return 0.0
    
    def _calculate_treynor_ratio(self, total_return: float, beta: float, risk_free_rate: float = 0.02) -> float:
        """Calculate Treynor ratio."""
        try:
            if beta == 0:
                return 0.0
            
            treynor_ratio = (total_return - risk_free_rate) / beta
            return round(treynor_ratio, 4)
            
        except Exception:
            return 0.0
    
    def _calculate_jensen_alpha(self, total_return: float, beta: float, market_return: float, 
                               risk_free_rate: float = 0.02) -> float:
        """Calculate Jensen's Alpha."""
        try:
            expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
            jensen_alpha = total_return - expected_return
            return round(jensen_alpha, 4)
            
        except Exception:
            return 0.0
    
    def generate_performance_report(self, portfolio_id: str, start_date: str, end_date: str) -> Dict:
        """Generate comprehensive performance report."""
        try:
            # Get all performance metrics
            performance_metrics = self.calculate_performance_metrics(portfolio_id, start_date, end_date)
            risk_adjusted_metrics = self.calculate_risk_adjusted_metrics(portfolio_id, start_date, end_date)
            
            # Get correlation matrix data
            correlation_query = AnalyticsQueries.get_correlation_matrix(portfolio_id)
            correlation_df = db_manager.execute_query('trading_system', correlation_query)
            
            # Compile comprehensive report
            report = {
                'portfolio_id': portfolio_id,
                'report_period': f"{start_date} to {end_date}",
                'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'performance_summary': {
                    'total_return': performance_metrics['total_return'],
                    'annualized_return': performance_metrics['annualized_return'],
                    'volatility': performance_metrics['volatility'],
                    'sharpe_ratio': performance_metrics['sharpe_ratio']
                },
                'risk_metrics': {
                    'max_drawdown': performance_metrics['max_drawdown'],
                    'tracking_error': performance_metrics['tracking_error'],
                    'information_ratio': performance_metrics['information_ratio']
                },
                'risk_adjusted_metrics': risk_adjusted_metrics,
                'attribution_analysis': performance_metrics['attribution_analysis'],
                'correlation_analysis': self._analyze_correlations(correlation_df),
                'benchmark_comparison': self._generate_benchmark_comparison(portfolio_id, start_date, end_date),
                'recommendations': self._generate_performance_recommendations(performance_metrics, risk_adjusted_metrics)
            }
            
            logger.info(f"Performance report generated for portfolio {portfolio_id}")
            return report
            
        except Exception as e:
            logger.error(f"Performance report generation failed: {e}")
            raise
    
    def _analyze_correlations(self, correlation_df: pd.DataFrame) -> Dict:
        """Analyze portfolio correlation structure."""
        if correlation_df.empty:
            return {}
        
        # High correlation pairs
        high_corr = correlation_df[correlation_df['correlation_value'] > 0.7]
        low_corr = correlation_df[correlation_df['correlation_value'] < -0.3]
        
        return {
            'total_correlations': len(correlation_df),
            'high_correlation_pairs': len(high_corr),
            'low_correlation_pairs': len(low_corr),
            'average_correlation': correlation_df['correlation_value'].mean(),
            'correlation_distribution': {
                'very_high': len(correlation_df[correlation_df['correlation_value'] > 0.8]),
                'high': len(correlation_df[(correlation_df['correlation_value'] > 0.6) & (correlation_df['correlation_value'] <= 0.8)]),
                'moderate': len(correlation_df[(correlation_df['correlation_value'] > 0.3) & (correlation_df['correlation_value'] <= 0.6)]),
                'low': len(correlation_df[(correlation_df['correlation_value'] > 0.0) & (correlation_df['correlation_value'] <= 0.3)]),
                'negative': len(correlation_df[correlation_df['correlation_value'] <= 0.0])
            }
        }
    
    def _generate_benchmark_comparison(self, portfolio_id: str, start_date: str, end_date: str) -> Dict:
        """Generate benchmark comparison analysis."""
        # This would typically compare against S&P 500, Russell 1000, etc.
        # For now, returning placeholder data
        return {
            'benchmarks_compared': self.benchmark_indices,
            'outperformance': 'To be calculated with actual benchmark data',
            'relative_volatility': 'To be calculated with actual benchmark data',
            'correlation_to_benchmarks': 'To be calculated with actual benchmark data'
        }
    
    def _generate_performance_recommendations(self, performance_metrics: Dict, risk_metrics: Dict) -> List[str]:
        """Generate performance improvement recommendations."""
        recommendations = []
        
        # Sharpe ratio recommendations
        if performance_metrics['sharpe_ratio'] < 1.0:
            recommendations.append("Consider improving risk-adjusted returns through better position sizing or risk management")
        
        # Volatility recommendations
        if performance_metrics['volatility'] > 0.20:
            recommendations.append("Portfolio volatility is high - consider diversification strategies")
        
        # Drawdown recommendations
        if performance_metrics['max_drawdown'] < -0.10:
            recommendations.append("Maximum drawdown exceeds 10% - review risk management protocols")
        
        # Information ratio recommendations
        if performance_metrics['information_ratio'] < 0.5:
            recommendations.append("Information ratio suggests room for improvement in active management")
        
        if not recommendations:
            recommendations.append("Portfolio performance metrics are within acceptable ranges")
        
        return recommendations
