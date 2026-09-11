# 📈 AI Sales & Revenue Analyst

An intelligent sales analytics platform that uses AI to automatically analyze sales data, identify root causes of revenue changes, and provide actionable recommendations.

## 🌟 Features

### 📊 Real-time Analytics Dashboard
- **Revenue Trends**: Monthly revenue tracking with growth indicators
- **Multi-dimensional Analysis**: Break down sales by:
  - Products
  - Geographic regions
  - Customer types
  - Salespeople
  - Discount impact
- **Interactive Visualizations**: Powered by Plotly for deep data exploration

### 🤖 AI-Powered Insights
- **Automatic Root Cause Analysis**: AI identifies why sales fell or grew
- **Dimensional Performance Analysis**: Compare across all key metrics
- **Anomaly Detection**: Flag unusual patterns automatically
- **Customer Insights**: Understand returning vs. new customer trends

### 💡 Strategic Recommendations
- **Prioritized Actions**: Get high, medium, and low priority recommendations
- **Expected Impact**: See potential revenue/margin improvement
- **Implementation Timeline**: Know when to execute
- **Ownership**: Clear team accountability

### 📋 Data Explorer
- Filter and explore raw transaction data
- Download filtered datasets for further analysis
- Inspect detailed customer and product information

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Google Gemini API key (for Google Gemini AI)

### Installation

1. **Clone or download the project**
```bash
cd ai-sales-analyst
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up your API key**
```bash
# Create a .env file
echo "GEMINI_API_KEY=your_key_here" > .env
```

Or set it as an environment variable:
```bash
export GEMINI_API_KEY=your_key_here
```

5. **Run the application**
```bash
streamlit run sales_analyst_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
ai-sales-analyst/
├── sales_analyst_app.py          # Main Streamlit application
├── sales_analyzer.py              # Data analysis engine
├── ai_insights.py                 # AI-powered insights using Gemini
├── sample_data.py                 # Sample data generator
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .env                          # Environment variables (create this)
└── data/                         # Your CSV files (create this folder)
```

## 📊 Data Format

Upload a CSV file with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| date | datetime | Transaction date (YYYY-MM-DD) |
| product | string | Product name |
| region | string | Geographic region |
| customer_id | string | Unique customer identifier |
| customer_type | string | 'new' or 'returning' |
| salesperson | string | Sales rep name |
| quantity | integer | Units sold |
| price | float | Unit price |
| discount | float | Discount rate (0-1) |
| revenue | float | Final revenue amount |

### Example CSV Format:
```csv
date,product,region,customer_id,customer_type,salesperson,quantity,price,discount,revenue
2024-01-01,Product A,North,CUST1001,returning,John Smith,2,100.00,0.05,190.00
2024-01-02,Product B,South,CUST1002,new,Sarah Johnson,1,250.00,0.10,225.00
```

## 🎯 How to Use

### Step 1: Upload Data
- Go to **📤 Upload Data** page
- Upload your CSV file or load sample data
- Verify data is correctly recognized

### Step 2: Explore Analytics
- Visit **📈 Analytics Dashboard**
- Select date range
- View revenue trends and breakdowns
- Analyze performance by dimension

### Step 3: Generate AI Insights
- Go to **🤖 AI Insights**
- Click "Generate AI Analysis"
- Wait for Gemini to analyze your data
- Review automatic insights and findings

### Step 4: Review Recommendations
- Navigate to **💡 Recommendations**
- See prioritized action items
- Review expected impact and timeline
- Plan implementation with responsible teams

### Step 5: Explore Details
- Use **📋 Data Explorer** for granular analysis
- Filter by product, region, or other dimensions
- Download filtered data for further analysis

## 🧠 How AI Analysis Works

The AI Insight Generator:

1. **Gathers all analytical data** from the sales database
2. **Prepares comprehensive context** including:
   - Product performance and trends
   - Regional analysis
   - Customer behavior patterns
   - Discount impact analysis
   - Sales team performance
   - Monthly trends
   - Detected anomalies

3. **Sends to Google Gemini AI** with detailed analysis prompt
4. **Receives structured insights** including:
   - Executive summary
   - Revenue analysis with comparisons
   - Customer insights
   - Root cause analysis
   - Strategic recommendations

5. **Formats results** for easy consumption in the UI

## 📈 Key Metrics Explained

### Revenue Metrics
- **Total Revenue**: Sum of all sales in period
- **MoM Change**: Month-over-Month percentage change
- **YoY Change**: Year-over-Year percentage change

### Performance Metrics
- **Avg Order Value**: Average revenue per transaction
- **Customer Concentration**: % of revenue from top customers
- **Unique Customers**: Number of distinct customers

### Health Metrics
- **Discount Impact**: Total revenue lost to discounting
- **Product Variety**: Number of different products sold
- **Sales Team Performance**: Revenue per salesperson

## 🔍 Analysis Examples

### Example 1: Declining Sales
If revenue drops 14% in a month:
- Product A down 21% (quality issues?)
- North region down 18% (new competitor?)
- Returning customers down 9% (retention issue?)
- Excessive discounting detected

**Recommendation**: Investigate product quality, competitive landscape, and customer satisfaction

### Example 2: Uneven Performance
- Some regions growing 25%, others declining
- New customers strong, returning customers flat
- Specific salespeople outperforming peers

**Recommendation**: Share best practices, improve territory management

## 🛠️ Customization

### Add New Dimensions
Edit `sales_analyzer.py` to add analysis by:
```python
def get_by_new_dimension(self, df: pd.DataFrame, dimension: str):
    # Add your custom analysis
    pass
```

### Modify AI Prompts
Edit the prompt in `ai_insights.py`:
```python
def _create_analysis_prompt(self, data: Dict[str, Any]) -> str:
    # Customize the analysis request to Gemini
    pass
```

### Change Visualization Colors
Edit CSS in `sales_analyst_app.py`:
```python
fig.update_layout(
    template="plotly_dark",  # or "plotly", "ggplot2", etc.
    # ... other settings
)
```

## 🔐 Security Considerations

1. **API Key**: Keep your `.env` file secure and never commit it
2. **Data Privacy**: 
   - Sales data is sent to Gemini API
   - Consider using only summary statistics for sensitive data
   - Check Anthropic's privacy policy
3. **File Upload**: Only upload CSV files, validate data before processing

## 📊 Sample Data Generation

Generate test data:
```python
from sample_data import generate_sample_data, generate_realistic_decline_data

# Basic sample
df = generate_sample_data(months=12, records_per_month=500)

# With obvious decline
df = generate_realistic_decline_data()

df.to_csv('test_data.csv', index=False)
```

## 🚨 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

### "API key not found"
Ensure `.env` file exists with:
```
GEMINI_API_KEY=your_actual_key_here
```

### Slow performance with large datasets
- Filter to smaller date ranges
- Use monthly aggregates instead of daily
- Consider pre-processing data

### Streamlit connection issues
```bash
streamlit run sales_analyst_app.py --logger.level=debug
```

## 📚 Advanced Features

### Custom Dashboards
Extend the app by adding new pages in `sales_analyst_app.py`:
```python
elif page == "🎯 Custom Analysis":
    # Your custom analysis code
    pass
```

### Database Integration
Replace CSV with SQL database:
```python
import sqlite3
conn = sqlite3.connect('sales.db')
df = pd.read_sql_query("SELECT * FROM sales", conn)
```

### Forecast Integration
Add forecasting models:
```python
from sklearn.linear_model import LinearRegression
# Train and predict future sales
```

## 📞 Support & Contribution

- Report issues or suggest features
- Customize analysis for your specific needs
- Extend functionality as needed

## 📄 License

Open source - Use and modify freely

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas User Guide](https://pandas.pydata.org/docs/)
- [Plotly Graph Objects](https://plotly.com/python/)
- [Gemini API Documentation](https://docs.google-genai.com/)

---

**Version 1.0** | Built with Python, Streamlit, and Google Gemini AI
