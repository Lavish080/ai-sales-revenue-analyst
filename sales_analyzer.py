import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class SalesAnalyzer:
    """Analyzes sales data across multiple dimensions"""
    
    def __init__(self, data: pd.DataFrame):
        """Initialize analyzer with sales data"""
        self.data = data.copy()
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data['year_month'] = self.data['date'].dt.to_period('M')
        
        # Ensure required columns
        if 'discount' not in self.data.columns:
            self.data['discount'] = 0
        if 'customer_type' not in self.data.columns:
            self.data['customer_type'] = 'unknown'
        if 'salesperson' not in self.data.columns:
            self.data['salesperson'] = 'unknown'
    
    def get_monthly_trend(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate monthly revenue trend"""
        monthly = df.groupby(df['date'].dt.to_period('M')).agg({
            'revenue': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        monthly['month'] = monthly['date'].astype(str)
        monthly['growth%'] = monthly['revenue'].pct_change() * 100
        
        return monthly.drop('date', axis=1)
    
    def get_by_dimension(self, df: pd.DataFrame, dimension: str) -> pd.DataFrame:
        """Analyze revenue by a specific dimension"""
        grouped = df.groupby(dimension).agg({
            'revenue': ['sum', 'mean', 'count'],
            'quantity': 'sum',
            'discount': 'mean'
        }).reset_index()
        
        grouped.columns = [dimension, 'revenue', 'avg_order_value', 'order_count', 'quantity', 'avg_discount']
        grouped = grouped.sort_values('revenue', ascending=False)
        
        # Calculate previous period for comparison
        current_month = df['date'].max().to_period('M')
        prev_month = current_month - 1
        
        prev_data = self.data[self.data['year_month'] == prev_month]
        if len(prev_data) > 0:
            prev_grouped = prev_data.groupby(dimension)['revenue'].sum().to_dict()
            grouped['prev_revenue'] = grouped[dimension].map(prev_grouped).fillna(0)
            grouped['growth%'] = ((grouped['revenue'] - grouped['prev_revenue']) / grouped['prev_revenue'].replace(0, 1)) * 100
        else:
            grouped['growth%'] = 0
        
        return grouped
    
    def get_discount_impact(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze discount impact on sales"""
        result = df.groupby('product').agg({
            'discount': lambda x: (x * 100).mean(),  # Convert to percentage
            'revenue': ['sum', 'count'],
            'quantity': 'sum'
        }).reset_index()
        
        result.columns = ['product', 'discount%', 'revenue', 'order_count', 'quantity']
        
        # Add margin impact (assume 30% base margin)
        result['estimated_margin'] = result['revenue'] * 0.3 * (1 - result['discount%']/100)
        
        return result
    
    def get_customer_analysis(self, df: pd.DataFrame) -> Dict:
        """Analyze customer behavior"""
        result = {}
        
        # Customer type analysis
        customer_type_revenue = df.groupby('customer_type')['revenue'].agg(['sum', 'count', 'mean'])
        result['by_type'] = customer_type_revenue.to_dict()
        
        # Get previous period
        current_month = df['date'].max().to_period('M')
        prev_month = current_month - 1
        prev_data = self.data[self.data['year_month'] == prev_month]
        
        if len(prev_data) > 0:
            prev_type_revenue = prev_data.groupby('customer_type')['revenue'].sum().to_dict()
            result['prev_by_type'] = prev_type_revenue
        
        # Top customers
        top_customers = df.groupby('customer_id')['revenue'].sum().nlargest(10).reset_index()
        result['top_customers'] = top_customers.to_dict('records')
        
        # Customer concentration
        result['concentration'] = {
            'top_10_pct': df.groupby('customer_id')['revenue'].sum().nlargest(10).sum() / df['revenue'].sum() * 100,
            'total_unique_customers': df['customer_id'].nunique()
        }
        
        return result
    
    def get_salesperson_performance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze salesperson performance"""
        perf = df.groupby('salesperson').agg({
            'revenue': ['sum', 'count', 'mean'],
            'customer_id': 'nunique',
            'discount': 'mean'
        }).reset_index()
        
        perf.columns = ['salesperson', 'total_revenue', 'order_count', 'avg_order_value', 'unique_customers', 'avg_discount']
        perf = perf.sort_values('total_revenue', ascending=False)
        
        return perf
    
    def get_regional_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detailed regional analysis"""
        regional = df.groupby('region').agg({
            'revenue': ['sum', 'count', 'mean'],
            'product': 'nunique',
            'customer_id': 'nunique',
            'discount': 'mean'
        }).reset_index()
        
        regional.columns = ['region', 'total_revenue', 'order_count', 'avg_order_value', 'product_variety', 'unique_customers', 'avg_discount']
        
        return regional.sort_values('total_revenue', ascending=False)
    
    def get_product_performance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Product performance metrics"""
        products = df.groupby('product').agg({
            'revenue': ['sum', 'count', 'mean'],
            'quantity': 'sum',
            'discount': 'mean',
            'customer_id': 'nunique'
        }).reset_index()
        
        products.columns = ['product', 'total_revenue', 'order_count', 'avg_price', 'units_sold', 'avg_discount', 'unique_customers']
        
        # Profitability (assume different margins by product)
        products['estimated_profit'] = products['total_revenue'] * 0.35 * (1 - products['avg_discount'])
        
        return products.sort_values('total_revenue', ascending=False)
    
    def identify_anomalies(self, df: pd.DataFrame) -> Dict:
        """Identify sales anomalies"""
        anomalies = {}
        
        # Sudden drops in specific products/regions
        monthly_by_product = df.groupby([df['date'].dt.to_period('M'), 'product'])['revenue'].sum().reset_index()
        
        # Products with significant decline
        recent_months = monthly_by_product['date'].unique()[-2:]
        if len(recent_months) >= 2:
            prev_month = monthly_by_product[monthly_by_product['date'] == recent_months[0]]
            current_month = monthly_by_product[monthly_by_product['date'] == recent_months[1]]
            
            merged = prev_month.merge(current_month, on='product', how='inner', suffixes=('_prev', '_curr'))
            merged['change%'] = ((merged['revenue_curr'] - merged['revenue_prev']) / merged['revenue_prev']) * 100
            
            declining = merged[merged['change%'] < -10].sort_values('change%')
            anomalies['declining_products'] = declining[['product', 'change%']].to_dict('records')
        
        return anomalies
    
    def get_comparison_periods(self, current_start: datetime, current_end: datetime) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Get data for current and previous periods"""
        current = self.data[
            (self.data['date'] >= current_start) &
            (self.data['date'] <= current_end)
        ]
        
        period_length = (current_end - current_start).days
        prev_start = current_start - timedelta(days=period_length)
        prev_end = current_start - timedelta(days=1)
        
        previous = self.data[
            (self.data['date'] >= prev_start) &
            (self.data['date'] <= prev_end)
        ]
        
        return current, previous
    
    def calculate_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate comprehensive metrics"""
        return {
            'total_revenue': df['revenue'].sum(),
            'avg_order_value': df['revenue'].mean(),
            'total_orders': len(df),
            'total_units': df['quantity'].sum(),
            'unique_customers': df['customer_id'].nunique(),
            'avg_discount': df['discount'].mean() * 100,
            'discount_impact': (df['discount'].sum() * df['revenue'].mean()),
        }
