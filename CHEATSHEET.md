# ⚡ AI Sales Analyst - Developer Cheatsheet

Quick reference for common tasks and commands.

---

## 🚀 Getting Started (Copy-Paste)

### Setup (Mac/Linux)
```bash
git clone <repo>
cd ai-sales-analyst
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
streamlit run sales_analyst_app.py
```

### Setup (Windows)
```bash
git clone <repo>
cd ai-sales-analyst
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your API key
streamlit run sales_analyst_app.py
```

### Docker
```bash
export ANTHROPIC_API_KEY=your_key
docker-compose up -d
# Visit http://localhost
```

---

## 📝 Data Format

### Minimal CSV
```csv
date,product,region,customer_id,revenue
2024-01-01,Product A,North,CUST001,199.99
```

### Complete CSV
```csv
date,product,region,customer_id,customer_type,salesperson,quantity,price,discount,revenue
2024-01-01,Product A,North,CUST001,returning,John Smith,2,100.00,0.05,190.00
```

---

## 📊 Common Python Operations

### Load & Analyze Data
```python
import pandas as pd
from sales_analyzer import SalesAnalyzer

# Load CSV
df = pd.read_csv('sales_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Create analyzer
analyzer = SalesAnalyzer(df)

# Get metrics
monthly = analyzer.get_monthly_trend(df)
products = analyzer.get_by_dimension(df, 'product')
regions = analyzer.get_by_dimension(df, 'region')

# Customer analysis
customers = analyzer.get_customer_analysis(df)
sales_perf = analyzer.get_salesperson_performance(df)
```

### Generate AI Insights
```python
from ai_insights import AIInsightGenerator

# Create insight generator
insight_gen = AIInsightGenerator(df, analyzer)

# Generate insights
insights = insight_gen.generate_insights(df)

# Access results
print(insights['summary'])
print(insights['revenue_analysis'])
print(insights['recommendations'])
```

### Use Database
```python
from db_manager import DatabaseManager

# Connect
db = DatabaseManager('sales_data.db')

# Insert data
db.insert_data(df)

# Query data
filtered = db.read_data(
    start_date='2024-01-01',
    end_date='2024-01-31',
    region='North'
)

# Get stats
stats = db.get_summary_stats()

# Close
db.close()
```

---

## 🎨 Streamlit Components

### File Upload
```python
uploaded_file = st.file_uploader("Choose CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
```

### Display Data
```python
st.dataframe(df)
st.table(df)
st.write(df)
```

### Metrics
```python
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", "$100K", "+5%")
col2.metric("Orders", "1,234")
col3.metric("AOV", "$81.11")
```

### Charts
```python
import plotly.express as px

# Line chart
fig = px.line(df, x='date', y='revenue', title='Revenue Trend')
st.plotly_chart(fig, use_container_width=True)

# Bar chart
fig = px.bar(df, x='product', y='revenue', color='region')
st.plotly_chart(fig, use_container_width=True)

# Pie chart
fig = px.pie(df, values='revenue', names='product')
st.plotly_chart(fig, use_container_width=True)

# Scatter
fig = px.scatter(df, x='discount', y='revenue', size='quantity')
st.plotly_chart(fig, use_container_width=True)
```

### Select/Filter
```python
selected_product = st.selectbox(
    "Choose product",
    df['product'].unique()
)
filtered = df[df['product'] == selected_product]

selected_regions = st.multiselect(
    "Choose regions",
    df['region'].unique(),
    default=df['region'].unique()
)
filtered = df[df['region'].isin(selected_regions)]
```

### Date Range
```python
col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date")
end_date = col2.date_input("End Date")

filtered = df[
    (df['date'] >= pd.Timestamp(start_date)) &
    (df['date'] <= pd.Timestamp(end_date))
]
```

### Expandable Sections
```python
with st.expander("Advanced Settings", expanded=False):
    threshold = st.slider("Threshold", 0, 100, 50)
    metric = st.selectbox("Metric", ["Revenue", "Orders"])
```

### Tabs
```python
tab1, tab2, tab3 = st.tabs(["Overview", "Details", "Export"])

with tab1:
    st.write("Tab 1 content")

with tab2:
    st.write("Tab 2 content")

with tab3:
    st.write("Tab 3 content")
```

---

## 🐍 Pandas Operations

### Basic
```python
# Load
df = pd.read_csv('file.csv')

# View
df.head(10)
df.tail(5)
df.info()
df.describe()

# Columns
df.columns
df.dtypes
df['column'].unique()
```

### Filtering
```python
# Single condition
df[df['column'] > 100]

# Multiple conditions
df[(df['region'] == 'North') & (df['revenue'] > 1000)]

# Exclude
df[df['column'] != 'value']

# In list
df[df['product'].isin(['A', 'B', 'C'])]

# Date range
df[(df['date'] >= '2024-01-01') & (df['date'] <= '2024-01-31')]
```

### Grouping & Aggregation
```python
# Sum by group
df.groupby('product')['revenue'].sum()

# Multiple aggregations
df.groupby('region').agg({
    'revenue': ['sum', 'mean', 'count'],
    'customer_id': 'nunique'
})

# Multiple grouping
df.groupby(['product', 'region'])['revenue'].sum()
```

### Calculations
```python
# New column
df['profit'] = df['revenue'] * 0.35

# Percentage
df['pct_change'] = df['revenue'].pct_change() * 100

# Rank
df['rank'] = df['revenue'].rank(ascending=False)

# Running total
df['cumsum'] = df['revenue'].cumsum()
```

### Sorting
```python
# Sort ascending
df.sort_values('revenue')

# Sort descending
df.sort_values('revenue', ascending=False)

# Sort by multiple columns
df.sort_values(['region', 'revenue'], ascending=[True, False])

# Top N
df.nlargest(5, 'revenue')
df.nsmallest(5, 'revenue')
```

### Pivot Tables
```python
pivot = df.pivot_table(
    values='revenue',
    index='product',
    columns='region',
    aggfunc='sum'
)
```

---

## 🔧 Configuration

### .env Template
```
ANTHROPIC_API_KEY=sk-your-key-here
DATABASE_PATH=./sales_data.db
MAX_RECORDS_DASHBOARD=50000
LOG_LEVEL=INFO
```

### Streamlit Config (~/.streamlit/config.toml)
```toml
[logger]
level = "info"

[client]
showErrorDetails = true

[server]
maxUploadSize = 200
enableXsrfProtection = true
```

---

## 🧪 Testing & Debugging

### Test Imports
```python
python -c "import streamlit; print('OK')"
python -c "import pandas; print('OK')"
python -c "from anthropic import Anthropic; print('OK')"
```

### Test API
```python
import anthropic
client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello"}]
)
print(msg.content[0].text)
```

### Debug Output
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or in Streamlit
st.write(df.dtypes)
st.write(df.head())
st.json(dict_variable)
```

---

## 📦 Docker Commands

```bash
# Build
docker build -t sales-analyst .

# Run
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your_key \
  sales-analyst

# Logs
docker logs container_id
docker logs -f container_id

# List
docker ps
docker ps -a

# Stop
docker stop container_id

# Remove
docker rm container_id

# Compose
docker-compose up -d
docker-compose down
docker-compose logs -f
```

---

## 🔍 Debugging Tips

### Check Data Types
```python
print(df.dtypes)
# Ensure date is datetime, revenue is float
```

### Handle Missing Values
```python
# Check for nulls
df.isnull().sum()

# Fill nulls
df.fillna(0)
df.fillna(method='ffill')

# Drop nulls
df.dropna()
```

### Check for Duplicates
```python
# Find duplicates
df[df.duplicated()]

# Remove duplicates
df.drop_duplicates()

# Count duplicates
df.duplicated().sum()
```

### Verify Data Quality
```python
# Unique values
df['column'].nunique()
df['column'].value_counts()

# Range
df['revenue'].min()
df['revenue'].max()

# Statistics
df.describe()
```

---

## 🚀 Deployment Shortcuts

### Quick Docker Deploy
```bash
export ANTHROPIC_API_KEY=your_key
docker-compose up -d
echo "Running at http://localhost:80"
```

### Push to GitHub & Deploy to Streamlit Cloud
```bash
git add .
git commit -m "Initial commit"
git push origin main

# Go to share.streamlit.io and deploy
# Add ANTHROPIC_API_KEY in secrets
```

### Quick Heroku Deploy
```bash
heroku create app-name
heroku config:set ANTHROPIC_API_KEY=your_key
git push heroku main
```

---

## 📊 API Endpoints Reference

### Claude API (via Anthropic SDK)
```python
from anthropic import Anthropic

client = Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Your prompt here"}
    ]
)
print(message.content[0].text)
```

---

## 💾 File Operations

### Read/Write CSV
```python
# Read
df = pd.read_csv('file.csv')

# Write
df.to_csv('output.csv', index=False)

# Append
df.to_csv('output.csv', mode='a', header=False, index=False)
```

### Read/Write JSON
```python
# Read
data = pd.read_json('file.json')

# Write
df.to_json('output.json', orient='records')
```

### Download in Streamlit
```python
csv = df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv"
)
```

---

## 🎯 Common Patterns

### Date Filtering
```python
# Last month
last_month = df[
    (df['date'] >= '2024-01-01') & 
    (df['date'] <= '2024-01-31')
]

# Last 30 days
thirty_days_ago = pd.Timestamp.now() - pd.Timedelta(days=30)
recent = df[df['date'] >= thirty_days_ago]

# Year-to-date
ytd = df[df['date'].dt.year == pd.Timestamp.now().year]
```

### Calculate Growth
```python
# Month-over-month
current = df[df['date'].dt.month == 1]['revenue'].sum()
previous = df[df['date'].dt.month == 12]['revenue'].sum()
growth = ((current - previous) / previous) * 100

# Year-over-year
current_year = df[df['date'].dt.year == 2024]['revenue'].sum()
previous_year = df[df['date'].dt.year == 2023]['revenue'].sum()
growth = ((current_year - previous_year) / previous_year) * 100
```

### Top N Analysis
```python
# Top 5 products
df.groupby('product')['revenue'].sum().nlargest(5)

# Bottom 5 regions
df.groupby('region')['revenue'].sum().nsmallest(5)

# Top customers
df.groupby('customer_id')['revenue'].sum().nlargest(10)
```

---

## 📱 Mobile Streamlit Config

```python
st.set_page_config(
    page_title="Sales Analyst",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

---

## ⚠️ Common Errors & Fixes

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | `pip install -r requirements.txt` |
| `FileNotFoundError: .env not found` | `cp .env.example .env` |
| `AttributeError: 'NoneType'` | Check for null values with `.fillna()` |
| `KeyError: 'column_name'` | Verify column exists: `print(df.columns)` |
| `ValueError: No numeric types to aggregate` | Check data types: `print(df.dtypes)` |
| `API Error: 401` | Check API key in `.env` |
| `Port 8501 already in use` | `streamlit run app.py --server.port 8502` |

---

## 🔗 Useful Links

- [Streamlit Docs](https://docs.streamlit.io/)
- [Pandas Docs](https://pandas.pydata.org/)
- [Plotly Docs](https://plotly.com/python/)
- [Anthropic API](https://docs.anthropic.com/)
- [Docker Docs](https://docs.docker.com/)
- [GitHub Guides](https://guides.github.com/)

---

## 📌 Keyboard Shortcuts (Streamlit)

- `C` - Clear cache
- `R` - Rerun script
- `T` - Toggle theme
- `K` - Keyboard shortcuts

---

**Save this file and bookmark it for quick reference!**

