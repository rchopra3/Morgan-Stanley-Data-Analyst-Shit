#!/usr/bin/env python3
"""
Morgan Stanley Global Markets Analytics - Main Analytics Script
Comprehensive demonstration of portfolio analysis, risk management, compliance monitoring, and performance analytics.
"""

import os
import sys
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analytics.portfolio_analytics import PortfolioAnalytics
from analytics.risk_analytics import RiskAnalytics
from analytics.compliance_analytics import ComplianceAnalytics
from analytics.performance_analytics import PerformanceAnalytics
from visualization.charts import PortfolioCharts, RiskCharts, ComplianceCharts, PerformanceCharts
from config import MS_CONFIG, COMPLIANCE_LIMITS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_sample_data():
    """Create sample data for demonstration purposes."""
    logger.info("Creating sample data for analytics demonstration...")
    
    # Sample portfolio positions
    sample_positions = [
        {'symbol': 'AAPL', 'quantity': 1000, 'cost_basis': 150.0, 'market_value': 175000, 
         'unrealized_pnl': 25000, 'realized_pnl': 5000, 'sector': 'Technology', 'region': 'US', 'currency': 'USD'},
        {'symbol': 'MSFT', 'quantity': 800, 'cost_basis': 280.0, 'market_value': 240000, 
         'unrealized_pnl': 16000, 'realized_pnl': 8000, 'sector': 'Technology', 'region': 'US', 'currency': 'USD'},
        {'symbol': 'JPM', 'quantity': 1200, 'cost_basis': 140.0, 'market_value': 168000, 
         'unrealized_pnl': 12000, 'realized_pnl': 3000, 'sector': 'Financial', 'region': 'US', 'currency': 'USD'},
        {'symbol': 'JNJ', 'quantity': 600, 'cost_basis': 160.0, 'market_value': 96000, 
         'unrealized_pnl': 6000, 'realized_pnl': 2000, 'sector': 'Healthcare', 'region': 'US', 'currency': 'USD'},
        {'symbol': 'XOM', 'quantity': 900, 'cost_basis': 80.0, 'market_value': 81000, 
         'unrealized_pnl': 9000, 'realized_pnl': 1000, 'sector': 'Energy', 'region': 'US', 'currency': 'USD'}
    ]
    
    # Sample performance attribution data
    sample_attribution = [
        {'factor_name': 'Stock Selection', 'factor_return': 0.08, 'factor_weight': 0.6, 'contribution': 0.048},
        {'factor_name': 'Sector Allocation', 'factor_return': 0.05, 'factor_weight': 0.3, 'contribution': 0.015},
        {'factor_name': 'Market Timing', 'factor_return': 0.02, 'factor_weight': 0.1, 'contribution': 0.002}
    ]
    
    return sample_positions, sample_attribution

def run_portfolio_analysis():
    """Run comprehensive portfolio analysis."""
    logger.info("=" * 60)
    logger.info("PORTFOLIO ANALYSIS")
    logger.info("=" * 60)
    
    portfolio_analytics = PortfolioAnalytics()
    
    # Create sample portfolio data
    sample_positions, _ = create_sample_data()
    
    # Simulate portfolio analysis (in practice, this would use real database data)
    portfolio_data = {
        'portfolio_id': 'DEMO_PORTFOLIO_001',
        'as_of_date': datetime.now().strftime('%Y-%m-%d'),
        'total_positions': len(sample_positions),
        'total_market_value': sum(pos['market_value'] for pos in sample_positions),
        'total_cost_basis': sum(pos['cost_basis'] * pos['quantity'] for pos in sample_positions),
        'total_unrealized_pnl': sum(pos['unrealized_pnl'] for pos in sample_positions),
        'total_realized_pnl': sum(pos['realized_pnl'] for pos in sample_positions),
        'positions': sample_positions
    }
    
    # Analyze portfolio
    analysis = portfolio_analytics.analyze_portfolio_positions('DEMO_PORTFOLIO_001')
    
    # Display results
    logger.info(f"Portfolio Analysis Results:")
    logger.info(f"  Portfolio ID: {analysis.get('portfolio_id', 'N/A')}")
    logger.info(f"  Total Positions: {analysis.get('total_positions', 0)}")
    logger.info(f"  Total Market Value: ${analysis.get('total_market_value', 0):,.0f}")
    logger.info(f"  Total Unrealized P&L: ${analysis.get('total_unrealized_pnl', 0):,.0f}")
    logger.info(f"  Total Realized P&L: ${analysis.get('total_realized_pnl', 0):,.0f}")
    
    # Display concentration analysis
    concentration = analysis.get('concentration_analysis', {})
    logger.info(f"  Herfindahl Index: {concentration.get('herfindahl_index', 0):.3f}")
    logger.info(f"  Concentration Level: {concentration.get('concentration_level', 'N/A')}")
    logger.info(f"  Diversification Score: {concentration.get('diversification_score', 0):.1f}")
    
    # Display compliance flags
    compliance_flags = analysis.get('compliance_flags', [])
    if compliance_flags:
        logger.warning(f"  Compliance Flags: {len(compliance_flags)} issues detected")
        for flag in compliance_flags[:3]:  # Show first 3 flags
            logger.warning(f"    - {flag['description']}")
    else:
        logger.info("  Compliance Status: No issues detected")
    
    return analysis

def run_risk_analysis():
    """Run comprehensive risk analysis."""
    logger.info("=" * 60)
    logger.info("RISK ANALYSIS")
    logger.info("=" * 60)
    
    risk_analytics = RiskAnalytics()
    
    # Calculate VaR using different methods
    portfolio_id = 'DEMO_PORTFOLIO_001'
    
    # Parametric VaR
    var_parametric = risk_analytics.calculate_portfolio_var(portfolio_id, method='parametric')
    if var_parametric:
        logger.info(f"Parametric VaR Results:")
        logger.info(f"  VaR (99%): ${var_parametric.get('var_absolute', 0):,.0f}")
        logger.info(f"  VaR (%): {var_parametric.get('var_percentage', 0):.2%}")
        logger.info(f"  Portfolio Volatility: {var_parametric.get('portfolio_volatility', 0):.2%}")
    
    # Monte Carlo VaR
    var_monte_carlo = risk_analytics.calculate_portfolio_var(portfolio_id, method='monte_carlo')
    if var_monte_carlo:
        logger.info(f"Monte Carlo VaR Results:")
        logger.info(f"  VaR (99%): ${var_monte_carlo.get('var_absolute', 0):,.0f}")
        logger.info(f"  VaR (%): {var_monte_carlo.get('var_percentage', 0):.2%}")
        logger.info(f"  Simulations: {var_monte_carlo.get('simulation_count', 0):,}")
    
    # Expected Shortfall
    es_result = risk_analytics.calculate_expected_shortfall(portfolio_id)
    if es_result:
        logger.info(f"Expected Shortfall Results:")
        logger.info(f"  Expected Shortfall: ${es_result.get('expected_shortfall', 0):,.0f}")
        logger.info(f"  ES (%): {es_result.get('es_percentage', 0):.2%}")
    
    # Stress Testing
    stress_result = risk_analytics.perform_stress_test(portfolio_id)
    if stress_result:
        logger.info(f"Stress Test Results:")
        logger.info(f"  Scenario: {stress_result.get('scenario_name', 'N/A')}")
        stress_data = stress_result.get('stress_results', {})
        logger.info(f"  Portfolio Loss: ${stress_data.get('portfolio_loss', 0):,.0f}")
        logger.info(f"  Loss (%): {stress_data.get('portfolio_loss_percentage', 0):.2%}")
    
    return {
        'parametric_var': var_parametric,
        'monte_carlo_var': var_monte_carlo,
        'expected_shortfall': es_result,
        'stress_test': stress_result
    }

def run_compliance_analysis():
    """Run comprehensive compliance analysis."""
    logger.info("=" * 60)
    logger.info("COMPLIANCE ANALYSIS")
    logger.info("=" * 60)
    
    compliance_analytics = ComplianceAnalytics()
    
    # Monitor position limits
    position_status = compliance_analytics.monitor_position_limits('DEMO_PORTFOLIO_001')
    logger.info(f"Position Limit Monitoring:")
    logger.info(f"  Status: {position_status.get('status', 'N/A')}")
    logger.info(f"  Compliance Score: {position_status.get('compliance_score', 0):.1f}")
    logger.info(f"  Breaches: {position_status.get('breach_count', 0)}")
    logger.info(f"  Warnings: {position_status.get('warning_count', 0)}")
    
    # Monitor large trades
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    large_trade_status = compliance_analytics.monitor_large_trades(start_date=start_date, end_date=end_date)
    logger.info(f"Large Trade Monitoring:")
    logger.info(f"  Status: {large_trade_status.get('status', 'N/A')}")
    logger.info(f"  Large Trades: {large_trade_status.get('total_large_trades', 0)}")
    logger.info(f"  Review Required: {large_trade_status.get('compliance_review_required', 0)}")
    
    # Detect wash trades
    wash_trade_status = compliance_analytics.detect_wash_trades(start_date, end_date)
    logger.info(f"Wash Trade Detection:")
    logger.info(f"  Status: {wash_trade_status.get('status', 'N/A')}")
    logger.info(f"  Potential Wash Trades: {wash_trade_status.get('total_potential_wash', 0)}")
    logger.info(f"  High Risk: {wash_trade_status.get('high_risk_count', 0)}")
    
    # Calculate overall compliance metrics
    compliance_metrics = compliance_analytics.calculate_compliance_metrics('DEMO_PORTFOLIO_001')
    logger.info(f"Overall Compliance Metrics:")
    logger.info(f"  Overall Score: {compliance_metrics.get('overall_compliance_score', 0):.1f}")
    logger.info(f"  Compliance Level: {compliance_metrics.get('compliance_level', 'N/A')}")
    logger.info(f"  Next Review: {compliance_metrics.get('next_review_date', 'N/A')}")
    
    return {
        'position_limits': position_status,
        'large_trades': large_trade_status,
        'wash_trades': wash_trade_status,
        'overall_metrics': compliance_metrics
    }

def run_performance_analysis():
    """Run comprehensive performance analysis."""
    logger.info("=" * 60)
    logger.info("PERFORMANCE ANALYSIS")
    logger.info("=" * 60)
    
    performance_analytics = PerformanceAnalytics()
    
    # Calculate performance metrics
    portfolio_id = 'DEMO_PORTFOLIO_001'
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    performance_metrics = performance_analytics.calculate_performance_metrics(portfolio_id, start_date, end_date)
    logger.info(f"Performance Metrics:")
    logger.info(f"  Total Return: {performance_metrics.get('total_return', 0):.2%}")
    logger.info(f"  Annualized Return: {performance_metrics.get('annualized_return', 0):.2%}")
    logger.info(f"  Volatility: {performance_metrics.get('volatility', 0):.2%}")
    logger.info(f"  Sharpe Ratio: {performance_metrics.get('sharpe_ratio', 0):.2f}")
    logger.info(f"  Max Drawdown: {performance_metrics.get('max_drawdown', 0):.2%}")
    logger.info(f"  Information Ratio: {performance_metrics.get('information_ratio', 0):.2f}")
    
    # Calculate risk-adjusted metrics
    risk_adjusted_metrics = performance_analytics.calculate_risk_adjusted_metrics(portfolio_id, start_date, end_date)
    logger.info(f"Risk-Adjusted Metrics:")
    logger.info(f"  Sortino Ratio: {risk_adjusted_metrics.get('sortino_ratio', 0):.2f}")
    logger.info(f"  Calmar Ratio: {risk_adjusted_metrics.get('calmar_ratio', 0):.2f}")
    logger.info(f"  Treynor Ratio: {risk_adjusted_metrics.get('treynor_ratio', 0):.2f}")
    logger.info(f"  Jensen's Alpha: {risk_adjusted_metrics.get('jensen_alpha', 0):.2%}")
    
    # Generate performance report
    performance_report = performance_analytics.generate_performance_report(portfolio_id, start_date, end_date)
    logger.info(f"Performance Report Generated:")
    logger.info(f"  Report Period: {performance_report.get('report_period', 'N/A')}")
    logger.info(f"  Generation Date: {performance_report.get('generation_date', 'N/A')}")
    
    # Display recommendations
    recommendations = performance_report.get('recommendations', [])
    if recommendations:
        logger.info(f"Performance Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            logger.info(f"  {i}. {rec}")
    
    return {
        'performance_metrics': performance_metrics,
        'risk_adjusted_metrics': risk_adjusted_metrics,
        'performance_report': performance_report
    }

def generate_visualizations(analysis_results):
    """Generate comprehensive visualizations."""
    logger.info("=" * 60)
    logger.info("GENERATING VISUALIZATIONS")
    logger.info("=" * 60)
    
    # Create output directory
    output_dir = 'reports'
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Portfolio Charts
        portfolio_charts = PortfolioCharts()
        portfolio_data = analysis_results.get('portfolio_analysis', {})
        
        if portfolio_data:
            # Portfolio overview
            fig = portfolio_charts.create_portfolio_overview(portfolio_data)
            fig.savefig(f'{output_dir}/portfolio_overview.png', dpi=300, bbox_inches='tight')
            logger.info("Portfolio overview chart saved")
            
            # Exposure heatmap
            exposure_data = portfolio_data.get('exposure_analysis', {})
            if exposure_data:
                fig = portfolio_charts.create_exposure_heatmap(exposure_data)
                if fig:
                    fig.savefig(f'{output_dir}/exposure_heatmap.png', dpi=300, bbox_inches='tight')
                    logger.info("Exposure heatmap saved")
            
            # Concentration analysis
            concentration_data = portfolio_data.get('concentration_analysis', {})
            if concentration_data:
                fig = portfolio_charts.create_concentration_analysis(concentration_data)
                fig.savefig(f'{output_dir}/concentration_analysis.png', dpi=300, bbox_inches='tight')
                logger.info("Concentration analysis chart saved")
        
        # Risk Charts
        risk_charts = RiskCharts()
        risk_data = analysis_results.get('risk_analysis', {})
        
        if risk_data:
            # VaR analysis
            var_data = risk_data.get('parametric_var', {})
            if var_data:
                fig = risk_charts.create_var_analysis(var_data)
                fig.savefig(f'{output_dir}/var_analysis.png', dpi=300, bbox_inches='tight')
                logger.info("VaR analysis chart saved")
            
            # Stress test results
            stress_data = risk_data.get('stress_test', {}).get('stress_results', {})
            if stress_data:
                fig = risk_charts.create_stress_test_results(stress_data)
                fig.savefig(f'{output_dir}/stress_test_results.png', dpi=300, bbox_inches='tight')
                logger.info("Stress test results chart saved")
        
        # Compliance Charts
        compliance_charts = ComplianceCharts()
        compliance_data = analysis_results.get('compliance_analysis', {}).get('overall_metrics', {})
        
        if compliance_data:
            fig = compliance_charts.create_compliance_dashboard(compliance_data)
            fig.savefig(f'{output_dir}/compliance_dashboard.png', dpi=300, bbox_inches='tight')
            logger.info("Compliance dashboard saved")
        
        # Performance Charts
        performance_charts = PerformanceCharts()
        performance_data = analysis_results.get('performance_analysis', {}).get('performance_metrics', {})
        
        if performance_data:
            fig = performance_charts.create_performance_summary(performance_data)
            fig.savefig(f'{output_dir}/performance_summary.png', dpi=300, bbox_inches='tight')
            logger.info("Performance summary chart saved")
        
        logger.info(f"All visualizations saved to {output_dir}/ directory")
        
    except Exception as e:
        logger.error(f"Error generating visualizations: {e}")

def main():
    """Main analytics execution function."""
    logger.info("=" * 80)
    logger.info(f"MORGAN STANLEY GLOBAL MARKETS ANALYTICS")
    logger.info(f"Team: {MS_CONFIG['team']}")
    logger.info(f"Division: {MS_CONFIG['division']}")
    logger.info(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    try:
        # Run comprehensive analytics
        analysis_results = {}
        
        # Portfolio Analysis
        analysis_results['portfolio_analysis'] = run_portfolio_analysis()
        
        # Risk Analysis
        analysis_results['risk_analysis'] = run_risk_analysis()
        
        # Compliance Analysis
        analysis_results['compliance_analysis'] = run_compliance_analysis()
        
        # Performance Analysis
        analysis_results['performance_analysis'] = run_performance_analysis()
        
        # Generate Visualizations
        generate_visualizations(analysis_results)
        
        # Summary
        logger.info("=" * 80)
        logger.info("ANALYTICS EXECUTION COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        logger.info("Next Steps:")
        logger.info("1. Review generated charts in reports/ directory")
        logger.info("2. Analyze compliance flags and risk metrics")
        logger.info("3. Share insights with trading and risk teams")
        logger.info("4. Schedule follow-up analysis based on findings")
        logger.info("5. Update compliance monitoring thresholds if needed")
        
        return analysis_results
        
    except Exception as e:
        logger.error(f"Analytics execution failed: {e}")
        raise

if __name__ == "__main__":
    main()
