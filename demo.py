#!/usr/bin/env python3
"""
Morgan Stanley Analytics Demo
Quick demonstration of the analytics framework capabilities.
"""

import pandas as pd
from analytics.portfolio_analytics import PortfolioAnalytics
from analytics.risk_analytics import RiskAnalytics
from analytics.compliance_analytics import ComplianceAnalytics

def quick_demo():
    """Run a quick demo of the analytics framework."""
    
    print("🚀 Morgan Stanley Analytics - Quick Demo")
    print("=" * 50)
    
    # 1. Portfolio Analysis
    print("\n📊 PORTFOLIO ANALYSIS")
    print("-" * 30)
    
    portfolio_analytics = PortfolioAnalytics()
    portfolio_data = portfolio_analytics.load_portfolio_data('PORTFOLIO_001')
    
    if not portfolio_data.empty:
        print(f"✅ Loaded {len(portfolio_data)} portfolio positions")
        print(f"💰 Total Market Value: ${portfolio_data['market_value'].sum():,.0f}")
        print(f"📈 Total Unrealized P&L: ${portfolio_data['unrealized_pnl'].sum():,.0f}")
        
        # Show top positions
        top_positions = portfolio_data.nlargest(3, 'market_value')
        print(f"\n🏆 Top 3 Positions:")
        for _, pos in top_positions.iterrows():
            print(f"  {pos['symbol']}: ${pos['market_value']:,.0f} ({pos['sector']})")
        
        # Sector breakdown
        sector_exposure = portfolio_analytics.get_sector_exposure_analysis('PORTFOLIO_001')
        if not sector_exposure.empty:
            print(f"\n🏭 Sector Exposure:")
            for _, sector in sector_exposure.iterrows():
                print(f"  {sector['sector']}: {sector['weight']:.1%} (${sector['market_value']:,.0f})")
    
    # 2. Trading Activity
    print("\n📈 TRADING ACTIVITY")
    print("-" * 30)
    
    trading_metrics = portfolio_analytics.calculate_portfolio_metrics('PORTFOLIO_001')
    if 'error' not in trading_metrics:
        print(f"✅ Total Trades: {trading_metrics.get('total_trades', 0)}")
        print(f"💰 Total Notional: ${trading_metrics.get('total_notional', 0):,.0f}")
        print(f"💸 Total Commission: ${trading_metrics.get('total_commission', 0):,.2f}")
        
        # Strategy breakdown
        strategy_breakdown = trading_metrics.get('strategy_breakdown', {})
        if strategy_breakdown:
            print(f"\n🎯 Trading Strategies:")
            for strategy, count in strategy_breakdown.items():
                print(f"  {strategy}: {count} trades")
    
    # 3. Risk Analysis
    print("\n⚠️ RISK ANALYSIS")
    print("-" * 30)
    
    risk_analytics = RiskAnalytics()
    var_result = risk_analytics.calculate_portfolio_var('PORTFOLIO_001', method='parametric')
    
    if var_result:
        print(f"✅ VaR (99%): ${var_result.get('var_absolute', 0):,.0f}")
        print(f"📊 VaR (%): {var_result.get('var_percentage', 0):.2%}")
        print(f"📈 Portfolio Volatility: {var_result.get('portfolio_volatility', 0):.2%}")
    
    # 4. Compliance Check
    print("\n🔒 COMPLIANCE CHECK")
    print("-" * 30)
    
    compliance_analytics = ComplianceAnalytics()
    position_status = compliance_analytics.monitor_position_limits('PORTFOLIO_001')
    
    if position_status:
        print(f"✅ Compliance Score: {position_status.get('compliance_score', 0):.1f}")
        print(f"🚨 Breaches: {position_status.get('breach_count', 0)}")
        print(f"⚠️ Warnings: {position_status.get('warning_count', 0)}")
        
        if position_status.get('breach_count', 0) > 0:
            print(f"\n🚨 Compliance Issues Detected:")
            for flag in position_status.get('breaches', [])[:2]:
                print(f"  • {flag['description']}")
    
    # 5. Portfolio Summary
    print("\n📋 PORTFOLIO SUMMARY REPORT")
    print("-" * 30)
    
    summary_report = portfolio_analytics.generate_portfolio_summary_report('PORTFOLIO_001')
    if summary_report:
        portfolio_summary = summary_report.get('portfolio_summary', {})
        print(f"📊 Total Positions: {portfolio_summary.get('total_positions', 0)}")
        print(f"💰 Total Value: ${portfolio_summary.get('total_market_value', 0):,.0f}")
        print(f"📈 Total P&L: ${portfolio_summary.get('total_unrealized_pnl', 0):,.0f}")
        
        # Key insights
        insights = summary_report.get('key_insights', [])
        if insights:
            print(f"\n💡 Key Insights:")
            for insight in insights[:3]:
                print(f"  • {insight}")
    
    print("\n🎉 Demo completed successfully!")
    print("🚀 Run 'python main_analytics.py' for full analysis with visualizations!")

if __name__ == "__main__":
    quick_demo()
