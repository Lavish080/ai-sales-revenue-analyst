import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(months=12, records_per_month=500):
    """Generate realistic sample sales data"""
    
    np.random.seed(42)
    
    # Parameters
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    regions = ['North', 'South', 'East', 'West', 'Central']
    salespeople = ['John Smith', 'Sarah Johnson', 'Mike Brown', 'Emily Davis', 'Robert Wilson']
    
    data = []
    
    # Generate data for specified months
    for month in range(months):
        base_date = datetime(2023, 1, 1) + timedelta(days=30*month)
        
        for _ in range(records_per_month):
            # Random date within month
            day = np.random.randint(1, 29)
            date = base_date.replace(day=day)
            
            # Product selection with trend decay
            product = np.random.choice(products, p=[0.35, 0.25, 0.20, 0.12, 0.08])
            
            # Product-specific pricing
            if product == 'Product A':
                base_price = 100
            elif product == 'Product B':
                base_price = 250
            elif product == 'Product C':
                base_price = 500
            elif product == 'Product D':
                base_price = 75
            else:  # Product E
                base_price = 1500
            
            # Price variation
            price = base_price * np.random.uniform(0.8, 1.2)
            quantity = np.random.randint(1, 5)
            
            # Discount (higher in later months for Products A and B)
            if product in ['Product A', 'Product B'] and month >= 8:
                discount = np.random.uniform(0.05, 0.20)  # 5-20% discount
            else:
                discount = np.random.uniform(0, 0.10)  # 0-10% discount
            
            revenue = price * quantity * (1 - discount)
            
            # Regional and salesperson assignment
            region = np.random.choice(regions)
            salesperson = np.random.choice(salespeople)
            
            # Customer info
            customer_id = f"CUST{np.random.randint(1000, 5000)}"
            customer_type = np.random.choice(['new', 'returning'], p=[0.3, 0.7])
            
            # Add some churn/decline pattern
            if month >= 6 and product in ['Product A', 'Product B']:
                # Simulate declining performance
                if np.random.random() < 0.15:  # 15% chance of no sale
                    continue
            
            data.append({
                'date': date,
                'product': product,
                'region': region,
                'customer_id': customer_id,
                'customer_type': customer_type,
                'salesperson': salesperson,
                'quantity': quantity,
                'price': price,
                'discount': discount,
                'revenue': revenue
            })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    return df

def generate_realistic_decline_data():
    """Generate sample data with obvious sales decline for demo"""
    
    np.random.seed(42)
    
    products = ['Premium Software', 'Standard Software', 'Basic Software', 'Support Package', 'Training']
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
    salespeople = ['Alice Chen', 'Bob Martinez', 'Carol White', 'David Lee', 'Emma Thompson']
    
    data = []
    
    for month in range(12):
        base_date = datetime(2023, 1, 1) + timedelta(days=30*month)
        
        # Declining trend over time
        month_multiplier = 1 - (month * 0.08)  # 8% decline per month
        
        records = int(600 * month_multiplier)
        
        for _ in range(records):
            day = np.random.randint(1, 29)
            date = base_date.replace(day=day)
            
            product = np.random.choice(products, p=[0.35, 0.25, 0.20, 0.15, 0.05])
            
            # Pricing based on product type
            price_map = {
                'Premium Software': 5000,
                'Standard Software': 2500,
                'Basic Software': 500,
                'Support Package': 1000,
                'Training': 800
            }
            
            base_price = price_map.get(product, 1000)
            price = base_price * np.random.uniform(0.9, 1.1)
            quantity = np.random.randint(1, 3)
            
            # Discounting increases over time (worse margins)
            discount = np.random.uniform(0.05, 0.05 + (month * 0.02))
            
            revenue = price * quantity * (1 - discount)
            
            region = np.random.choice(regions)
            salesperson = np.random.choice(salespeople)
            customer_id = f"CUS{str(np.random.randint(10000, 99999))}"
            customer_type = 'returning' if np.random.random() < 0.65 else 'new'
            
            data.append({
                'date': date,
                'product': product,
                'region': region,
                'customer_id': customer_id,
                'customer_type': customer_type,
                'salesperson': salesperson,
                'quantity': quantity,
                'price': price,
                'discount': discount,
                'revenue': revenue
            })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    # Test the generator
    df = generate_sample_data(months=12, records_per_month=500)
    print(f"Generated {len(df)} records")
    print(df.head(10))
    print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")
    print(f"Total Revenue: ${df['revenue'].sum():,.2f}")
    
    # Save sample
    df.to_csv('/home/claude/sample_sales_data.csv', index=False)
    print("\nSample data saved to sample_sales_data.csv")
