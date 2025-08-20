"""
Morgan Stanley Global Markets Analytics - Database Package
Database connection and query utilities for trading, risk, and compliance data.
"""

from .connections import DatabaseManager
from .queries import TradingQueries, RiskQueries, ComplianceQueries

__all__ = ['DatabaseManager', 'TradingQueries', 'RiskQueries', 'ComplianceQueries']
