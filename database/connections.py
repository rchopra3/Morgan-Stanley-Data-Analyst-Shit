"""
Database Connection Management for Morgan Stanley Global Markets Analytics
Handles connections to trading, risk management, and compliance databases.
"""

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Dict, Optional, Any
import warnings

from config import DATABASE_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Centralized database connection manager for Morgan Stanley analytics.
    Handles connections to trading, risk, and compliance databases.
    """
    
    def __init__(self):
        self.engines = {}
        self.connections = {}
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Initialize database connections for all systems."""
        for system_name, config in DATABASE_CONFIG.items():
            try:
                connection_string = (
                    f"postgresql://{config['user']}:{config['password']}"
                    f"@{config['host']}:{config['port']}/{config['database']}"
                )
                
                engine = create_engine(
                    connection_string,
                    pool_size=5,
                    max_overflow=10,
                    pool_timeout=30,
                    pool_recycle=3600
                )
                
                # Test connection
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                
                self.engines[system_name] = engine
                logger.info(f"Successfully connected to {system_name} database")
                
            except SQLAlchemyError as e:
                logger.error(f"Failed to connect to {system_name} database: {e}")
                self.engines[system_name] = None
    
    def get_engine(self, system_name: str) -> Optional[sa.Engine]:
        """Get database engine for specified system."""
        return self.engines.get(system_name)
    
    def execute_query(self, system_name: str, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        Execute SQL query and return results as DataFrame.
        
        Args:
            system_name: Database system to query (trading_system, risk_management, compliance)
            query: SQL query string
            params: Query parameters (optional)
        
        Returns:
            pandas DataFrame with query results
        """
        engine = self.get_engine(system_name)
        if not engine:
            raise ValueError(f"No connection available for {system_name}")
        
        try:
            if params:
                df = pd.read_sql_query(query, engine, params=params)
            else:
                df = pd.read_sql_query(query, engine)
            
            logger.info(f"Successfully executed query on {system_name}: {len(df)} rows returned")
            return df
            
        except SQLAlchemyError as e:
            logger.error(f"Query execution failed on {system_name}: {e}")
            raise
    
    def execute_transaction(self, system_name: str, queries: list) -> bool:
        """
        Execute multiple queries in a transaction.
        
        Args:
            system_name: Database system to use
            queries: List of SQL queries to execute
        
        Returns:
            True if successful, False otherwise
        """
        engine = self.get_engine(system_name)
        if not engine:
            raise ValueError(f"No connection available for {system_name}")
        
        try:
            with engine.begin() as conn:
                for query in queries:
                    conn.execute(text(query))
            
            logger.info(f"Successfully executed transaction on {system_name}: {len(queries)} queries")
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"Transaction failed on {system_name}: {e}")
            return False
    
    def test_connections(self) -> Dict[str, bool]:
        """Test all database connections and return status."""
        status = {}
        for system_name, engine in self.engines.items():
            if engine:
                try:
                    with engine.connect() as conn:
                        conn.execute(text("SELECT 1"))
                    status[system_name] = True
                except SQLAlchemyError:
                    status[system_name] = False
            else:
                status[system_name] = False
        
        return status
    
    def close_connections(self):
        """Close all database connections."""
        for engine in self.engines.values():
            if engine:
                engine.dispose()
        logger.info("All database connections closed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connections()

# Global database manager instance
db_manager = DatabaseManager()
