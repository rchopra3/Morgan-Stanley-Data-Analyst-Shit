"""
Risk Analytics for Morgan Stanley Global Markets
Comprehensive risk management including VaR, stress testing, and risk metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import warnings
from scipy import stats
from scipy.optimize import minimize

from config import COMPLIANCE_LIMITS, REPORTING_CONFIG
from database.queries import RiskQueries
from database.connections import db_manager

logger = logging.getLogger(__name__)

class RiskAnalytics:
    """
    Comprehensive risk analytics for Morgan Stanley Global Markets.
    Handles VaR calculations, stress testing, and risk metrics.
    """
    
    def __init__(self):
        self.compliance_limits = COMPLIANCE_LIMITS
        self.reporting_config = REPORTING_CONFIG
        self.var_confidence_level = self.compliance_limits['var_confidence_level']
        self.var_time_horizon = self.compliance_limits['var_time_horizon']
    
    def calculate_portfolio_var(self, portfolio_id: str, method: str = 'parametric', 
                              confidence_level: float = None, time_horizon: int = None) -> Dict:
        """
        Calculate Value at Risk (VaR) for portfolio using specified method.
        
        Args:
            portfolio_id: Portfolio identifier
            method: VaR calculation method ('parametric', 'historical', 'monte_carlo')
            confidence_level: VaR confidence level (default: from config)
            time_horizon: VaR time horizon in days (default: from config)
        
        Returns:
            Dictionary containing VaR calculation results
        """
        try:
            confidence_level = confidence_level or self.var_confidence_level
            time_horizon = time_horizon or self.var_time_horizon
            
            # Get portfolio data for VaR calculation
            query = RiskQueries.get_var_calculation(portfolio_id, confidence_level, time_horizon)
            portfolio_data = db_manager.execute_query('risk_management', query)
            
            if portfolio_data.empty:
                logger.warning(f"No data available for VaR calculation on portfolio {portfolio_id}")
                return {}
            
            # Calculate VaR based on method
            if method == 'parametric':
                var_result = self._calculate_parametric_var(portfolio_data, confidence_level, time_horizon)
            elif method == 'historical':
                var_result = self._calculate_historical_var(portfolio_data, confidence_level, time_horizon)
            elif method == 'monte_carlo':
                var_result = self._calculate_monte_carlo_var(portfolio_data, confidence_level, time_horizon)
            else:
                raise ValueError(f"Unsupported VaR method: {method}")
            
            # Add portfolio context
            var_result.update({
                'portfolio_id': portfolio_id,
                'calculation_method': method,
                'confidence_level': confidence_level,
                'time_horizon': time_horizon,
                'calculation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_portfolio_value': portfolio_data['market_value'].sum()
            })
            
            logger.info(f"VaR calculation completed for portfolio {portfolio_id}: {method} method")
            return var_result
            
        except Exception as e:
            logger.error(f"VaR calculation failed for portfolio {portfolio_id}: {e}")
            raise
    
    def _calculate_parametric_var(self, portfolio_data: pd.DataFrame, confidence_level: float, 
                                 time_horizon: int) -> Dict:
        """Calculate parametric VaR using variance-covariance method."""
        # Calculate portfolio weights
        total_value = portfolio_data['market_value'].sum()
        weights = portfolio_data['market_value'] / total_value
        
        # Calculate portfolio volatility (assuming returns are normally distributed)
        # For simplicity, using 30-day volatility from market data
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(
            portfolio_data['volatility_30d'].fillna(0.2) ** 2, weights
        )))
        
        # Calculate VaR
        z_score = stats.norm.ppf(confidence_level)
        var_absolute = total_value * portfolio_vol * np.sqrt(time_horizon) * z_score
        var_percentage = var_absolute / total_value
        
        # Calculate component VaR for each position
        component_var = []
        for _, position in portfolio_data.iterrows():
            position_var = position['market_value'] * position['volatility_30d'].fillna(0.2) * np.sqrt(time_horizon) * z_score
            component_var.append({
                'symbol': position['symbol'],
                'market_value': position['market_value'],
                'weight': position['market_value'] / total_value,
                'volatility': position['volatility_30d'].fillna(0.2),
                'component_var': position_var,
                'var_contribution': position_var / var_absolute if var_absolute != 0 else 0
            })
        
        return {
            'var_absolute': var_absolute,
            'var_percentage': var_percentage,
            'portfolio_volatility': portfolio_vol,
            'z_score': z_score,
            'component_var': component_var,
            'method_details': 'Parametric VaR using variance-covariance method'
        }
    
    def _calculate_historical_var(self, portfolio_data: pd.DataFrame, confidence_level: float, 
                                 time_horizon: int) -> Dict:
        """Calculate historical VaR using historical simulation."""
        # For historical VaR, we would need historical returns data
        # This is a simplified implementation
        logger.warning("Historical VaR requires historical returns data - using simplified approach")
        
        # Simulate historical returns based on current volatility
        n_simulations = 1000
        simulated_returns = []
        
        for _, position in portfolio_data.iterrows():
            vol = position['volatility_30d'].fillna(0.2)
            returns = np.random.normal(0, vol, n_simulations)
            simulated_returns.append(returns * position['market_value'])
        
        # Calculate portfolio returns
        portfolio_returns = np.sum(simulated_returns, axis=0)
        
        # Calculate VaR
        var_absolute = np.percentile(portfolio_returns, (1 - confidence_level) * 100)
        var_percentage = var_absolute / portfolio_data['market_value'].sum()
        
        return {
            'var_absolute': var_absolute,
            'var_percentage': var_percentage,
            'simulation_count': n_simulations,
            'method_details': 'Historical VaR using simulated historical returns'
        }
    
    def _calculate_monte_carlo_var(self, portfolio_data: pd.DataFrame, confidence_level: float, 
                                  time_horizon: int) -> Dict:
        """Calculate Monte Carlo VaR using random sampling."""
        n_simulations = 10000
        
        # Generate random scenarios for each position
        portfolio_values = []
        
        for _ in range(n_simulations):
            scenario_value = 0
            for _, position in portfolio_data.iterrows():
                vol = position['volatility_30d'].fillna(0.2)
                # Generate random return for this position
                return_scenario = np.random.normal(0, vol * np.sqrt(time_horizon))
                position_value = position['market_value'] * (1 + return_scenario)
                scenario_value += position_value
            
            portfolio_values.append(scenario_value)
        
        # Calculate VaR
        initial_value = portfolio_data['market_value'].sum()
        portfolio_returns = [(pv - initial_value) / initial_value for pv in portfolio_values]
        
        var_absolute = np.percentile(portfolio_returns, (1 - confidence_level) * 100) * initial_value
        var_percentage = var_absolute / initial_value
        
        return {
            'var_absolute': var_absolute,
            'var_percentage': var_percentage,
            'simulation_count': n_simulations,
            'method_details': f'Monte Carlo VaR with {n_simulations} simulations'
        }
    
    def calculate_expected_shortfall(self, portfolio_id: str, confidence_level: float = None) -> Dict:
        """Calculate Expected Shortfall (Conditional VaR) for portfolio."""
        try:
            # Get VaR first
            var_result = self.calculate_portfolio_var(portfolio_id, method='parametric', 
                                                    confidence_level=confidence_level)
            
            if not var_result:
                return {}
            
            # For Expected Shortfall, we need to calculate the average loss beyond VaR
            # This is a simplified implementation
            portfolio_data = db_manager.execute_query('risk_management', 
                RiskQueries.get_var_calculation(portfolio_id, confidence_level or self.var_confidence_level))
            
            total_value = portfolio_data['market_value'].sum()
            portfolio_vol = var_result.get('portfolio_volatility', 0.2)
            
            # Calculate Expected Shortfall (simplified)
            z_score = stats.norm.ppf(confidence_level or self.var_confidence_level)
            es_factor = stats.norm.pdf(z_score) / (1 - (confidence_level or self.var_confidence_level))
            expected_shortfall = total_value * portfolio_vol * np.sqrt(self.var_time_horizon) * es_factor
            
            return {
                'portfolio_id': portfolio_id,
                'var_absolute': var_result['var_absolute'],
                'expected_shortfall': expected_shortfall,
                'es_percentage': expected_shortfall / total_value,
                'confidence_level': confidence_level or self.var_confidence_level,
                'calculation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logger.error(f"Expected Shortfall calculation failed: {e}")
            raise
    
    def perform_stress_test(self, portfolio_id: str, scenario_id: str = None) -> Dict:
        """Perform stress testing on portfolio using predefined scenarios."""
        try:
            # Get stress test scenarios
            scenarios_query = RiskQueries.get_stress_test_scenarios()
            scenarios_df = db_manager.execute_query('risk_management', scenarios_query)
            
            if scenarios_df.empty:
                logger.warning("No stress test scenarios available")
                return {}
            
            # Get portfolio data
            portfolio_data = db_manager.execute_query('risk_management', 
                RiskQueries.get_var_calculation(portfolio_id))
            
            if portfolio_data.empty:
                return {}
            
            # Select scenario
            if scenario_id:
                scenario = scenarios_df[scenarios_df['scenario_id'] == scenario_id].iloc[0]
            else:
                # Use first available scenario
                scenario = scenarios_df.iloc[0]
            
            # Apply stress test
            stress_results = self._apply_stress_scenario(portfolio_data, scenario)
            
            return {
                'portfolio_id': portfolio_id,
                'scenario_id': scenario['scenario_id'],
                'scenario_name': scenario['scenario_name'],
                'description': scenario['description'],
                'stress_results': stress_results,
                'test_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logger.error(f"Stress testing failed: {e}")
            raise
    
    def _apply_stress_scenario(self, portfolio_data: pd.DataFrame, scenario: pd.Series) -> Dict:
        """Apply stress scenario to portfolio and calculate impact."""
        initial_value = portfolio_data['market_value'].sum()
        
        # Calculate stressed values based on scenario
        stressed_values = []
        for _, position in portfolio_data.iterrows():
            # Apply equity shock if available
            equity_shock = scenario.get('equity_shock', 0)
            stressed_value = position['market_value'] * (1 + equity_shock)
            stressed_values.append(stressed_value)
        
        stressed_portfolio_value = sum(stressed_values)
        portfolio_loss = initial_value - stressed_portfolio_value
        portfolio_loss_pct = portfolio_loss / initial_value
        
        return {
            'initial_portfolio_value': initial_value,
            'stressed_portfolio_value': stressed_portfolio_value,
            'portfolio_loss': portfolio_loss,
            'portfolio_loss_percentage': portfolio_loss_pct,
            'scenario_impact': {
                'equity_shock': scenario.get('equity_shock', 0),
                'interest_rate_shock': scenario.get('interest_rate_shock', 0),
                'credit_spread_shock': scenario.get('credit_spread_shock', 0),
                'currency_shock': scenario.get('currency_shock', 0),
                'volatility_shock': scenario.get('volatility_shock', 0)
            }
        }
    
    def get_risk_limits_status(self, portfolio_id: str) -> pd.DataFrame:
        """Get current risk limits status for portfolio."""
        query = RiskQueries.get_risk_limits(portfolio_id)
        return db_manager.execute_query('risk_management', query)
    
    def calculate_beta_exposure(self, portfolio_data: pd.DataFrame) -> Dict:
        """Calculate portfolio beta exposure to market indices."""
        if 'beta_to_sp500' not in portfolio_data.columns:
            return {'error': 'Beta data not available'}
        
        # Calculate weighted average beta
        total_value = portfolio_data['market_value'].sum()
        weights = portfolio_data['market_value'] / total_value
        
        portfolio_beta = np.average(portfolio_data['beta_to_sp500'].fillna(1.0), weights=weights)
        
        # Calculate beta contribution by position
        beta_contributions = []
        for _, position in portfolio_data.iterrows():
            beta_contrib = (position['market_value'] / total_value) * position['beta_to_sp500'].fillna(1.0)
            beta_contributions.append({
                'symbol': position['symbol'],
                'market_value': position['market_value'],
                'weight': position['market_value'] / total_value,
                'beta': position['beta_to_sp500'].fillna(1.0),
                'beta_contribution': beta_contrib
            })
        
        return {
            'portfolio_beta': portfolio_beta,
            'beta_contributions': beta_contributions,
            'high_beta_positions': portfolio_data[portfolio_data['beta_to_sp500'] > 1.5][['symbol', 'beta_to_sp500', 'market_value']].to_dict('records'),
            'low_beta_positions': portfolio_data[portfolio_data['beta_to_sp500'] < 0.5][['symbol', 'beta_to_sp500', 'market_value']].to_dict('records')
        }
