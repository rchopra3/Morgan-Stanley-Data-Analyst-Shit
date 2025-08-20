"""
Professional Charting Utilities for Morgan Stanley Global Markets Analytics
Business-ready visualizations for traders, risk managers, and executives.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
import warnings

from config import REPORTING_CONFIG, MS_CONFIG

# Configure matplotlib and seaborn for professional output
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

logger = logging.getLogger(__name__)

class PortfolioCharts:
    """Portfolio visualization charts for Morgan Stanley analytics."""
    
    def __init__(self):
        self.config = REPORTING_CONFIG
        self.ms_config = MS_CONFIG
    
    def create_portfolio_overview(self, portfolio_data: Dict, save_path: str = None) -> plt.Figure:
        """Create comprehensive portfolio overview dashboard."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'Portfolio Overview - {portfolio_data.get("portfolio_id", "Unknown")}', 
                    fontsize=16, fontweight='bold')
        
        # Position size distribution
        position_dist = portfolio_data.get('position_analysis', {}).get('position_size_distribution', {})
        if position_dist:
            sizes = list(position_dist.values())
            labels = list(position_dist.keys())
            axes[0, 0].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            axes[0, 0].set_title('Position Size Distribution')
        
        # Sector exposure
        sector_data = portfolio_data.get('exposure_analysis', {}).get('sector', [])
        if sector_data:
            sector_df = pd.DataFrame(sector_data)
            if not sector_df.empty:
                axes[0, 1].barh(sector_df['sector'], sector_df['weight'])
                axes[0, 1].set_title('Sector Exposure')
                axes[0, 1].set_xlabel('Weight')
        
        # Top positions by market value
        top_positions = portfolio_data.get('position_analysis', {}).get('largest_positions', [])
        if top_positions:
            top_df = pd.DataFrame(top_positions)
            if not top_df.empty:
                axes[1, 0].barh(top_df['symbol'], top_df['market_value'])
                axes[1, 0].set_title('Top 10 Positions by Market Value')
                axes[1, 0].set_xlabel('Market Value ($)')
        
        # P&L distribution
        positions_df = pd.DataFrame(portfolio_data.get('positions', []))
        if not positions_df.empty and 'unrealized_pnl' in positions_df.columns:
            axes[1, 1].hist(positions_df['unrealized_pnl'], bins=20, alpha=0.7)
            axes[1, 1].set_title('Unrealized P&L Distribution')
            axes[1, 1].set_xlabel('P&L ($)')
            axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Portfolio overview chart saved to {save_path}")
        
        return fig
    
    def create_exposure_heatmap(self, exposure_data: Dict, save_path: str = None) -> plt.Figure:
        """Create exposure heatmap by sector and region."""
        # Prepare data for heatmap
        sector_data = exposure_data.get('sector', [])
        region_data = exposure_data.get('region', [])
        
        if not sector_data or not region_data:
            logger.warning("Insufficient data for exposure heatmap")
            return None
        
        # Create pivot table for heatmap
        sector_df = pd.DataFrame(sector_data)
        region_df = pd.DataFrame(region_data)
        
        # This is a simplified heatmap - in practice, you'd have sector-region combinations
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create sample heatmap data (replace with actual sector-region matrix)
        sectors = sector_df['sector'].unique() if not sector_df.empty else ['Tech', 'Finance', 'Healthcare']
        regions = region_df['region'].unique() if not region_df.empty else ['US', 'Europe', 'Asia']
        
        # Sample data - replace with actual calculations
        heatmap_data = np.random.rand(len(sectors), len(regions))
        
        sns.heatmap(heatmap_data, 
                   xticklabels=regions, 
                   yticklabels=sectors, 
                   annot=True, 
                   fmt='.2f',
                   cmap='RdYlBu_r',
                   ax=ax)
        
        ax.set_title('Portfolio Exposure Heatmap (Sector vs Region)', fontweight='bold')
        ax.set_xlabel('Region')
        ax.set_ylabel('Sector')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Exposure heatmap saved to {save_path}")
        
        return fig
    
    def create_concentration_analysis(self, concentration_data: Dict, save_path: str = None) -> plt.Figure:
        """Create portfolio concentration analysis charts."""
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # HHI and concentration metrics
        hhi = concentration_data.get('herfindahl_index', 0)
        diversification_score = concentration_data.get('diversification_score', 0)
        
        # Concentration gauge chart
        axes[0].pie([hhi, 1-hhi], labels=['Concentration', 'Diversification'], 
                   colors=['red', 'green'], autopct='%1.1f%%', startangle=90)
        axes[0].set_title(f'Portfolio Concentration\nHHI: {hhi:.3f}')
        
        # Diversification score bar
        axes[1].bar(['Diversification Score'], [diversification_score], 
                   color='blue', alpha=0.7)
        axes[1].set_ylim(0, 100)
        axes[1].set_title('Diversification Score (0-100)')
        axes[1].set_ylabel('Score')
        
        # Add score annotation
        axes[1].text(0, diversification_score + 2, f'{diversification_score:.1f}', 
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Concentration analysis chart saved to {save_path}")
        
        return fig

class RiskCharts:
    """Risk management visualization charts."""
    
    def __init__(self):
        self.config = REPORTING_CONFIG
    
    def create_var_analysis(self, var_data: Dict, save_path: str = None) -> plt.Figure:
        """Create VaR analysis visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Value at Risk Analysis', fontsize=16, fontweight='bold')
        
        # VaR summary
        var_absolute = var_data.get('var_absolute', 0)
        var_percentage = var_data.get('var_percentage', 0)
        portfolio_value = var_data.get('total_portfolio_value', 1)
        
        # VaR gauge
        axes[0, 0].pie([abs(var_percentage), 1-abs(var_percentage)], 
                       labels=['VaR', 'Remaining'], 
                       colors=['red', 'lightgray'], 
                       autopct='%1.2f%%', startangle=90)
        axes[0, 0].set_title(f'VaR: ${var_absolute:,.0f}\n({var_percentage:.2%})')
        
        # Component VaR breakdown
        component_var = var_data.get('component_var', [])
        if component_var:
            comp_df = pd.DataFrame(component_var)
            if not comp_df.empty:
                axes[0, 1].barh(comp_df['symbol'], comp_df['var_contribution'])
                axes[0, 1].set_title('VaR Contribution by Position')
                axes[0, 1].set_xlabel('VaR Contribution')
        
        # Volatility distribution
        if component_var:
            vol_data = [comp['volatility'] for comp in component_var]
            axes[1, 0].hist(vol_data, bins=15, alpha=0.7, color='skyblue')
            axes[1, 0].set_title('Position Volatility Distribution')
            axes[1, 0].set_xlabel('Volatility')
            axes[1, 0].set_ylabel('Frequency')
        
        # Risk vs Return scatter
        if component_var:
            market_values = [comp['market_value'] for comp in component_var]
            var_contribs = [comp['component_var'] for comp in component_var]
            axes[1, 1].scatter(market_values, var_contribs, alpha=0.6)
            axes[1, 1].set_title('Position Size vs VaR Contribution')
            axes[1, 1].set_xlabel('Market Value ($)')
            axes[1, 1].set_ylabel('VaR Contribution ($)')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"VaR analysis chart saved to {save_path}")
        
        return fig
    
    def create_stress_test_results(self, stress_data: Dict, save_path: str = None) -> plt.Figure:
        """Create stress test results visualization."""
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Portfolio value impact
        initial_value = stress_data.get('initial_portfolio_value', 0)
        stressed_value = stress_data.get('stressed_portfolio_value', 0)
        portfolio_loss = stress_data.get('portfolio_loss', 0)
        
        # Value comparison
        values = [initial_value, stressed_value]
        labels = ['Initial', 'Stressed']
        colors = ['green', 'red']
        
        axes[0].bar(labels, values, color=colors, alpha=0.7)
        axes[0].set_title('Portfolio Value: Initial vs Stressed')
        axes[0].set_ylabel('Portfolio Value ($)')
        
        # Add value annotations
        for i, v in enumerate(values):
            axes[0].text(i, v + max(values) * 0.01, f'${v:,.0f}', 
                        ha='center', va='bottom', fontweight='bold')
        
        # Loss breakdown
        loss_pct = stress_data.get('portfolio_loss_percentage', 0)
        axes[1].pie([abs(loss_pct), 1-abs(loss_pct)], 
                   labels=['Loss', 'Remaining'], 
                   colors=['red', 'lightgray'], 
                   autopct='%1.2f%%', startangle=90)
        axes[1].set_title(f'Portfolio Loss: ${portfolio_loss:,.0f}\n({loss_pct:.2%})')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Stress test results chart saved to {save_path}")
        
        return fig

class ComplianceCharts:
    """Compliance monitoring visualization charts."""
    
    def __init__(self):
        self.config = REPORTING_CONFIG
    
    def create_compliance_dashboard(self, compliance_data: Dict, save_path: str = None) -> plt.Figure:
        """Create compliance monitoring dashboard."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Compliance Monitoring Dashboard', fontsize=16, fontweight='bold')
        
        # Overall compliance score
        overall_score = compliance_data.get('overall_compliance_score', 0)
        axes[0, 0].pie([overall_score, 100-overall_score], 
                       labels=['Compliant', 'Non-Compliant'], 
                       colors=['green', 'red'], 
                       autopct='%1.1f%%', startangle=90)
        axes[0, 0].set_title(f'Overall Compliance Score: {overall_score:.1f}')
        
        # Position limit status
        position_status = compliance_data.get('position_limits', {})
        if position_status:
            breach_count = position_status.get('breach_count', 0)
            warning_count = position_status.get('warning_count', 0)
            compliant_count = position_status.get('total_positions_monitored', 0) - breach_count - warning_count
            
            status_counts = [compliant_count, warning_count, breach_count]
            status_labels = ['Compliant', 'Warning', 'Breach']
            status_colors = ['green', 'orange', 'red']
            
            axes[0, 1].bar(status_labels, status_counts, color=status_colors, alpha=0.7)
            axes[0, 1].set_title('Position Limit Status')
            axes[0, 1].set_ylabel('Number of Positions')
        
        # Large trade monitoring
        large_trade_status = compliance_data.get('large_trades', {})
        if large_trade_status and large_trade_status.get('status') == 'LARGE_TRADES_DETECTED':
            total_trades = large_trade_status.get('total_large_trades', 0)
            review_required = large_trade_status.get('compliance_review_required', 0)
            
            axes[1, 0].pie([review_required, total_trades-review_required], 
                           labels=['Review Required', 'No Review'], 
                           colors=['red', 'green'], 
                           autopct='%1.1f%%', startangle=90)
            axes[1, 0].set_title('Large Trades: Review Requirements')
        
        # Compliance trend (placeholder for time series)
        axes[1, 1].text(0.5, 0.5, 'Compliance Trend\n(Time Series Chart)', 
                        ha='center', va='center', transform=axes[1, 1].transAxes,
                        fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        axes[1, 1].set_title('Compliance Score Trend')
        axes[1, 1].set_xlim(0, 1)
        axes[1, 1].set_ylim(0, 1)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Compliance dashboard saved to {save_path}")
        
        return fig

class PerformanceCharts:
    """Performance analytics visualization charts."""
    
    def __init__(self):
        self.config = REPORTING_CONFIG
    
    def create_performance_summary(self, performance_data: Dict, save_path: str = None) -> plt.Figure:
        """Create performance summary dashboard."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Performance Summary Dashboard', fontsize=16, fontweight='bold')
        
        # Key metrics
        total_return = performance_data.get('total_return', 0)
        sharpe_ratio = performance_data.get('sharpe_ratio', 0)
        volatility = performance_data.get('volatility', 0)
        max_drawdown = performance_data.get('max_drawdown', 0)
        
        # Return vs Risk scatter
        axes[0, 0].scatter(volatility, total_return, s=200, alpha=0.7, color='blue')
        axes[0, 0].set_xlabel('Volatility')
        axes[0, 0].set_ylabel('Total Return')
        axes[0, 0].set_title('Return vs Risk Profile')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Add annotation
        axes[0, 0].annotate(f'Sharpe: {sharpe_ratio:.2f}', 
                           xy=(volatility, total_return), 
                           xytext=(volatility+0.02, total_return+0.02),
                           arrowprops=dict(arrowstyle='->', color='red'))
        
        # Sharpe ratio gauge
        sharpe_normalized = min(max(sharpe_ratio / 2, 0), 1)  # Normalize to 0-1
        axes[0, 1].pie([sharpe_normalized, 1-sharpe_normalized], 
                       labels=['Sharpe', 'Target'], 
                       colors=['green', 'lightgray'], 
                       autopct='%1.1f%%', startangle=90)
        axes[0, 1].set_title(f'Sharpe Ratio: {sharpe_ratio:.2f}')
        
        # Drawdown analysis
        axes[1, 0].bar(['Max Drawdown'], [abs(max_drawdown)], 
                       color='red', alpha=0.7)
        axes[1, 0].set_title('Maximum Drawdown')
        axes[1, 0].set_ylabel('Drawdown')
        axes[1, 0].text(0, abs(max_drawdown) + 0.01, f'{max_drawdown:.2%}', 
                        ha='center', va='bottom', fontweight='bold')
        
        # Performance attribution (placeholder)
        attribution = performance_data.get('attribution_analysis', {})
        if attribution and attribution.get('top_contributors'):
            top_contrib = attribution['top_contributors'][:5]
            contributors = [contrib['factor_name'] for contrib in top_contrib]
            contributions = [contrib['contribution'] for contrib in top_contrib]
            
            axes[1, 1].barh(contributors, contributions, alpha=0.7)
            axes[1, 1].set_title('Top Performance Contributors')
            axes[1, 1].set_xlabel('Contribution')
        else:
            axes[1, 1].text(0.5, 0.5, 'Performance Attribution\n(Data Not Available)', 
                            ha='center', va='center', transform=axes[1, 1].transAxes,
                            fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
            axes[1, 1].set_title('Performance Attribution')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Performance summary chart saved to {save_path}")
        
        return fig
