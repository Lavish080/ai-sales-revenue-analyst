# 📁 Project Structure Guide

Complete breakdown of the AI Sales & Revenue Analyst project structure.

## Directory Tree

```
ai-sales-analyst/
│
├── 📄 Main Application Files
│   ├── sales_analyst_app.py          # Main Streamlit application (UI)
│   ├── sales_analyzer.py             # Core data analysis engine
│   ├── ai_insights.py                # AI-powered insights using Claude
│   └── db_manager.py                 # Database management utilities
│
├── 📊 Data & Configuration
│   ├── sample_data.py                # Sample data generator
│   ├── sample_sales_data.csv         # Generated sample dataset
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment template
│   ├── .env                          # Environment variables (⚠️ GITIGNORE)
│   └── sales_data.db                 # SQLite database (optional)
│
├── 🐳 Docker & Deployment
│   ├── Dockerfile                    # Docker container definition
│   ├── docker-compose.yml            # Multi-container setup
│   └── nginx.conf                    # Nginx reverse proxy config
│
├── 📚 Documentation
│   ├── README.md                     # Main documentation
│   ├── SETUP_GUIDE.md               # Detailed setup instructions
│   ├── DEPLOYMENT.md                # Production deployment guide
│   └── PROJECT_STRUCTURE.md         # This file
│
├── 📁 User Data Directory (Auto-created)
│   └── data/                         # Your CSV files and exports
│
└── 📁 Optional Directories
    ├── .streamlit/                   # Streamlit configuration
    ├── __pycache__/                  # Python cache files
    ├── venv/                         # Virtual environment
    └── .git/                         # Git repository
```

---

## Core Application Files

### 1. `sales_analyst_app.py` (Main App)

**Purpose**: Streamlit web application frontend

**Key Components**:
- Page routing (5 pages)
- UI layout and styling
- File upload handling
- Data visualization
- Session state management

**Pages**:
- 📤 Upload Data
- 📈 Analytics Dashboard
- 🤖 AI Insights
- 💡 Recommendations
- 📋 Data Explorer

**Key Functions**:
```python
# Main UI rendering
st.set_page_config()      # App configuration
st.sidebar.radio()        # Page navigation
st.file_uploader()        # CSV upload
st.plotly_chart()         # Visualizations
```

### 2. `sales_analyzer.py` (Analysis Engine)

**Purpose**: Data analysis and calculations

**Key Classes**:
- `SalesAnalyzer` - Main analysis class

**Key Methods**:
```python
get_monthly_trend()           # Monthly revenue trend
get_by_dimension()            # Analyze by product/region/etc
get_discount_impact()         # Discount analysis
get_customer_analysis()       # Customer insights
get_salesperson_performance() # Team metrics
get_regional_analysis()       # Regional breakdown
identify_anomalies()          # Detect unusual patterns
calculate_metrics()           # Comprehensive metrics
```

**Data Flow**:
```
Raw Data → Filtering → Grouping → Aggregation → Metrics
```

### 3. `ai_insights.py` (AI Engine)

**Purpose**: Claude API integration for intelligent analysis

**Key Classes**:
- `AIInsightGenerator` - AI analysis class

**Key Methods**:
```python
generate_insights()    # Main analysis method
_prepare_analysis_data()  # Gather data
_create_analysis_prompt() # Build Claude prompt
_parse_insights()        # Parse API response
_generate_fallback_insights() # Fallback if parsing fails
```

**Data Flow**:
```
Analyzed Data → Prompt Creation → Claude API → JSON Parsing → Insights
```

### 4. `db_manager.py` (Database)

**Purpose**: SQLite database management (optional)

**Key Classes**:
- `DatabaseManager` - Database operations

**Key Methods**:
```python
_create_connection()  # Connect to DB
_create_tables()      # Initialize schema
insert_data()         # Add records
read_data()           # Query records
get_summary_stats()   # Database statistics
export_to_csv()       # Export data
clear_data()          # Delete records
```

---

## Data & Configuration Files

### `sample_data.py`

**Purpose**: Generate realistic sample sales data

**Functions**:
```python
generate_sample_data()        # Basic sample (12 months)
generate_realistic_decline_data() # With sales decline pattern
```

**Output**: 5,700+ sample records in CSV format

### `requirements.txt`

**Purpose**: Python package dependencies

```
streamlit==1.28.1        # Web framework
pandas==2.1.3            # Data manipulation
numpy==1.24.3            # Numerical computing
plotly==5.17.0           # Interactive charts
anthropic==0.7.1         # Claude API client
python-dotenv==1.0.0     # Environment variables
```

### `.env` File

**Purpose**: Store sensitive configuration

```
ANTHROPIC_API_KEY=sk-your-key-here
DATABASE_PATH=./sales_data.db
APP_TITLE=AI Sales & Revenue Analyst
DEBUG_MODE=false
```

⚠️ **Security**: Never commit `.env` to version control!

---

## Docker & Deployment Files

### `Dockerfile`

**Purpose**: Container definition

```dockerfile
FROM python:3.11-slim    # Base image
WORKDIR /app             # Working directory
RUN pip install -r requirements.txt  # Install dependencies
CMD ["streamlit", "run", "sales_analyst_app.py"]  # Run command
```

### `docker-compose.yml`

**Purpose**: Multi-container orchestration

```yaml
services:
  sales-analyst:         # Main app service
    build: .             # Build from Dockerfile
    ports: 8501:8501    # Port mapping
    volumes:             # Mount directories
    environment:         # Environment variables
  nginx:                 # Reverse proxy service
    image: nginx:alpine  # Official Nginx image
    ports: 80:80        # HTTP port
```

### `nginx.conf`

**Purpose**: Reverse proxy and load balancing

```nginx
upstream sales_analyst {
    server sales-analyst:8501;  # Route to Streamlit
}

server {
    listen 80;
    location / {
        proxy_pass http://sales_analyst;  # Forward requests
    }
}
```

---

## Documentation Files

### `README.md`

**Contents**:
- Feature overview
- Quick start guide
- Installation instructions
- Usage examples
- Data format specification
- Troubleshooting
- Advanced features

### `SETUP_GUIDE.md`

**Contents**:
- Detailed prerequisites
- Step-by-step installation
- Configuration instructions
- Verification steps
- Troubleshooting guide
- Performance tips

### `DEPLOYMENT.md`

**Contents**:
- Local deployment
- Docker deployment
- Cloud options (AWS, Heroku, Google Cloud)
- Production configuration
- Monitoring setup
- Scaling strategies
- Maintenance procedures

---

## File Relationships

### Data Flow Diagram

```
User Input (CSV)
    ↓
sales_analyst_app.py (Upload Page)
    ↓
pandas.read_csv()
    ↓
st.session_state.data
    ↓
analytics_dashboard.py (Visualization)
    ├─→ sales_analyzer.py (Analysis)
    │   ├─→ get_monthly_trend()
    │   ├─→ get_by_dimension()
    │   └─→ identify_anomalies()
    │
    └─→ ai_insights.py (AI)
        ├─→ _prepare_analysis_data()
        ├─→ _create_analysis_prompt()
        └─→ Claude API
            ↓
        Recommendations & Insights
            ↓
        UI Display
```

### Module Imports

```python
# sales_analyst_app.py imports
from sales_analyzer import SalesAnalyzer
from ai_insights import AIInsightGenerator
from sample_data import generate_sample_data

# ai_insights.py imports
from anthropic import Anthropic
from sales_analyzer import SalesAnalyzer

# db_manager.py imports
import sqlite3
import pandas as pd
```

---

## Configuration Locations

### Streamlit Config
```
~/.streamlit/config.toml
~/.streamlit/secrets.toml
```

### Environment Variables
```
.env (local)
OS environment (Docker/Cloud)
Streamlit Secrets (Streamlit Cloud)
```

### Database
```
./sales_data.db (SQLite)
Cloud database connection string
```

---

## Adding New Features

### Add New Analysis Metric

1. **Add to `sales_analyzer.py`**:
```python
def get_new_metric(self, df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('dimension').agg({'revenue': 'sum'})
```

2. **Use in `sales_analyst_app.py`**:
```python
analyzer = SalesAnalyzer(data)
metric_data = analyzer.get_new_metric(filtered_df)
st.dataframe(metric_data)
```

### Add New Page

1. **Add to navigation in `sales_analyst_app.py`**:
```python
page = st.sidebar.radio(
    "Navigation",
    ["📤 Upload Data", "📈 Analytics", "🆕 New Page"]  # Add new
)

if page == "🆕 New Page":
    st.write("Your new content here")
```

### Add New Visualization

```python
import plotly.express as px

fig = px.scatter(df, x='x_col', y='y_col')
st.plotly_chart(fig, use_container_width=True)
```

---

## File Sizes & Performance

| File | Size | Purpose |
|------|------|---------|
| sales_analyst_app.py | ~20 KB | Main app |
| sales_analyzer.py | ~15 KB | Analytics |
| ai_insights.py | ~18 KB | AI integration |
| db_manager.py | ~12 KB | Database |
| sample_data.py | ~8 KB | Sample generator |
| sample_sales_data.csv | ~800 KB | Test data |

---

## Development Workflow

### Local Development

```
1. Clone repository
2. Create virtual environment
3. Install requirements
4. Configure .env
5. Run: streamlit run sales_analyst_app.py
6. Make changes
7. Refresh browser (Streamlit auto-reloads)
```

### Testing Changes

```python
# Test in terminal
python -c "from sales_analyzer import SalesAnalyzer; print('OK')"

# Or run sample data generator
python sample_data.py
```

### Version Control

```bash
# .gitignore entries
.env
.streamlit/
__pycache__/
*.pyc
venv/
sales_data.db
data/
```

---

## Extending the Project

### Suggested Enhancements

1. **Machine Learning**
   - Sales forecasting
   - Customer churn prediction
   - Anomaly detection

2. **Integrations**
   - Salesforce CRM
   - Google Sheets
   - Slack notifications

3. **Advanced Features**
   - Real-time data streaming
   - Custom report generation
   - Email alerts

4. **Performance**
   - Caching layer
   - Database indexing
   - Query optimization

---

## Troubleshooting by File

### `sales_analyst_app.py` Issues
- Page not showing → Check page name in radio()
- File upload fails → Check file format
- Visualization error → Check data columns

### `sales_analyzer.py` Issues
- Calculation errors → Check data types
- Missing values → Add .fillna()
- Performance → Optimize groupby()

### `ai_insights.py` Issues
- API errors → Check API key
- JSON parsing → Check Claude response
- Slow analysis → Reduce data size

### `db_manager.py` Issues
- Connection failed → Check database path
- Query errors → Verify SQL syntax
- Missing data → Check insert_data() call

---

## Quick Reference

### Import Statements
```python
import streamlit as st
import pandas as pd
from sales_analyzer import SalesAnalyzer
from ai_insights import AIInsightGenerator
```

### Common Patterns
```python
# Create analyzer
analyzer = SalesAnalyzer(data)

# Get metrics
metrics = analyzer.get_by_dimension(df, 'product')

# Generate insights
insight_gen = AIInsightGenerator(data, analyzer)
insights = insight_gen.generate_insights(filtered_df)

# Display in UI
st.dataframe(metrics)
st.json(insights)
```

---

**Last Updated**: 2024 | Version 1.0
