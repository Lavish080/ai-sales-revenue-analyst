"""Database manager for sales data"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages SQLite database for sales data"""
    
    def __init__(self, db_path: str = "sales_data.db"):
        """Initialize database manager"""
        self.db_path = db_path
        self.conn = None
        self._create_connection()
        self._create_tables()
    
    def _create_connection(self):
        """Create database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def _create_tables(self):
        """Create necessary tables"""
        create_sales_table = """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            product TEXT NOT NULL,
            region TEXT NOT NULL,
            customer_id TEXT NOT NULL,
            customer_type TEXT,
            salesperson TEXT,
            quantity INTEGER,
            price REAL,
            discount REAL,
            revenue REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        create_index = """
        CREATE INDEX IF NOT EXISTS idx_date ON sales(date);
        CREATE INDEX IF NOT EXISTS idx_product ON sales(product);
        CREATE INDEX IF NOT EXISTS idx_region ON sales(region);
        CREATE INDEX IF NOT EXISTS idx_customer ON sales(customer_id);
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_sales_table)
            
            for idx in create_index.split(';'):
                if idx.strip():
                    cursor.execute(idx)
            
            self.conn.commit()
            logger.info("Database tables created successfully")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def insert_data(self, df: pd.DataFrame, table: str = 'sales'):
        """Insert dataframe into database"""
        try:
            df.to_sql(table, self.conn, if_exists='append', index=False)
            logger.info(f"Inserted {len(df)} records into {table}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error inserting data: {e}")
            return False
    
    def read_data(self, 
                  start_date: Optional[str] = None, 
                  end_date: Optional[str] = None,
                  region: Optional[str] = None,
                  product: Optional[str] = None) -> pd.DataFrame:
        """Read data from database with optional filters"""
        
        query = "SELECT * FROM sales WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        if region:
            query += " AND region = ?"
            params.append(region)
        
        if product:
            query += " AND product = ?"
            params.append(product)
        
        try:
            df = pd.read_sql_query(query, self.conn, params=params)
            df['date'] = pd.to_datetime(df['date'])
            return df
        except sqlite3.Error as e:
            logger.error(f"Error reading data: {e}")
            return pd.DataFrame()
    
    def get_summary_stats(self) -> dict:
        """Get database summary statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Total records
            cursor.execute("SELECT COUNT(*) as count FROM sales")
            total_records = cursor.fetchone()[0]
            
            # Date range
            cursor.execute("SELECT MIN(date) as min_date, MAX(date) as max_date FROM sales")
            min_date, max_date = cursor.fetchone()
            
            # Total revenue
            cursor.execute("SELECT SUM(revenue) as total FROM sales")
            total_revenue = cursor.fetchone()[0]
            
            # Unique values
            cursor.execute("SELECT COUNT(DISTINCT product) FROM sales")
            unique_products = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT region) FROM sales")
            unique_regions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM sales")
            unique_customers = cursor.fetchone()[0]
            
            return {
                'total_records': total_records,
                'min_date': min_date,
                'max_date': max_date,
                'total_revenue': total_revenue,
                'unique_products': unique_products,
                'unique_regions': unique_regions,
                'unique_customers': unique_customers
            }
        except sqlite3.Error as e:
            logger.error(f"Error getting stats: {e}")
            return {}
    
    def export_to_csv(self, output_path: str, **filters):
        """Export filtered data to CSV"""
        df = self.read_data(**filters)
        df.to_csv(output_path, index=False)
        logger.info(f"Exported {len(df)} records to {output_path}")
    
    def clear_data(self, confirmation: bool = False):
        """Clear all data from database"""
        if not confirmation:
            logger.warning("Confirmation required to clear data")
            return False
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM sales")
            self.conn.commit()
            logger.info("All data cleared from database")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error clearing data: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def import_csv_to_db(csv_path: str, db_path: str = "sales_data.db"):
    """Convenience function to import CSV to database"""
    
    if not Path(csv_path).exists():
        logger.error(f"CSV file not found: {csv_path}")
        return False
    
    try:
        # Read CSV
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded {len(df)} records from {csv_path}")
        
        # Insert into database
        with DatabaseManager(db_path) as db:
            success = db.insert_data(df)
            if success:
                stats = db.get_summary_stats()
                logger.info(f"Database stats: {stats}")
            return success
    
    except Exception as e:
        logger.error(f"Error importing CSV: {e}")
        return False


if __name__ == "__main__":
    # Example usage
    
    # Create database and import sample data
    from sample_data import generate_sample_data
    
    # Generate and import sample data
    print("Generating sample data...")
    df = generate_sample_data(months=12, records_per_month=500)
    
    print("Importing to database...")
    with DatabaseManager("sales_data.db") as db:
        db.insert_data(df)
        stats = db.get_summary_stats()
        print(f"\nDatabase Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Example query
        print("\nSample query results:")
        recent_data = db.read_data(start_date="2023-06-01")
        print(f"Records from June onwards: {len(recent_data)}")
