# 🚀 AI Sales Analyst - Complete Setup Guide

This guide walks you through setting up and running the AI Sales & Revenue Analyst application.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Loading Data](#loading-data)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended for large datasets)
- **Disk Space**: 500MB for application + data

### Required Accounts
- **Anthropic API**: Get your free API key from [console.anthropic.com](https://console.anthropic.com)

### Check Python Installation
```bash
python --version
# Should show Python 3.8 or higher

pip --version
# Should show pip with Python version
```

---

## Installation

### Step 1: Download/Clone the Project

**Option A: Download ZIP**
1. Download the project as ZIP
2. Extract to your desired location
3. Open terminal/command prompt in that folder

**Option B: Git Clone**
```bash
git clone <repository-url>
cd ai-sales-analyst
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `streamlit` - Web app framework
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `plotly` - Interactive visualizations
- `anthropic` - Claude API client
- `python-dotenv` - Environment variable management

### Step 4: Verify Installation

```bash
python -c "import streamlit; print(f'Streamlit {streamlit.__version__}')"
python -c "import pandas; print(f'Pandas {pandas.__version__}')"
python -c "import anthropic; print('Anthropic SDK installed')"
```

---

## Configuration

### Step 1: Get Your API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy the key (you won't see it again!)

### Step 2: Configure Environment Variables

**Method 1: Using .env file (Recommended)**

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Open `.env` in your text editor:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

3. Replace `your_actual_api_key_here` with your real key

⚠️ **Security**: Never commit `.env` to version control!

**Method 2: Environment Variable**

*Windows Command Prompt:*
```cmd
set ANTHROPIC_API_KEY=your_api_key_here
streamlit run sales_analyst_app.py
```

*Windows PowerShell:*
```powershell
$env:ANTHROPIC_API_KEY="your_api_key_here"
streamlit run sales_analyst_app.py
```

*macOS/Linux:*
```bash
export ANTHROPIC_API_KEY=your_api_key_here
streamlit run sales_analyst_app.py
```

### Step 3: Verify Configuration

Create a test script `test_config.py`:
```python
import os
from anthropic import Anthropic

api_key = os.getenv('ANTHROPIC_API_KEY')
if api_key:
    print("✅ API key found")
    client = Anthropic()
    print("✅ Anthropic client initialized")
else:
    print("❌ API key not found")
```

Run it:
```bash
python test_config.py
```

---

## Running the Application

### Start the App

```bash
streamlit run sales_analyst_app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://your-ip:8501
```

### Open in Browser

- Click the local URL or manually go to `http://localhost:8501`
- The app should load with the upload page

### Stop the App

Press `Ctrl+C` in the terminal.

---

## Loading Data

### Option 1: Use Sample Data (Recommended First Time)

1. Go to **📤 Upload Data** page
2. Click **"Load Sample Dataset"**
3. Sample data loads automatically
4. Proceed to analytics dashboard

### Option 2: Upload Your Own Data

#### Prepare Your CSV File

Create a CSV with these columns:

```csv
date,product,region,customer_id,customer_type,salesperson,quantity,price,discount,revenue
2024-01-01,Product A,North,CUST1001,returning,John Smith,2,100.00,0.05,190.00
2024-01-02,Product B,South,CUST1002,new,Sarah Johnson,1,250.00,0.10,225.00
2024-01-03,Product A,East,CUST1003,returning,Mike Brown,3,100.00,0.00,300.00
```

**Column Requirements:**

| Column | Type | Required? | Example |
|--------|------|-----------|---------|
| date | YYYY-MM-DD | ✅ | 2024-01-15 |
| product | Text | ✅ | "Product A" |
| region | Text | ✅ | "North" |
| customer_id | Text | ✅ | "CUST1001" |
| customer_type | "new"/"returning" | ⚠️ | "returning" |
| salesperson | Text | ⚠️ | "John Smith" |
| quantity | Number | ⚠️ | 2 |
| price | Decimal | ⚠️ | 99.99 |
| discount | 0-1 decimal | ⚠️ | 0.10 (=10%) |
| revenue | Decimal | ⚠️ | 179.99 |

✅ = Required | ⚠️ = Recommended

#### Upload in App

1. Go to **📤 Upload Data**
2. Click **"Choose a CSV file"**
3. Select your prepared CSV
4. Review the data preview
5. Verify all columns recognized

---

## Using the Application

### Workflow

```
1. Upload Data (CSV or sample)
    ↓
2. Explore Analytics Dashboard
    ↓
3. Generate AI Insights
    ↓
4. Review Recommendations
    ↓
5. Export & Share Results
```

### Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API key configured in `.env` file
- [ ] API key is valid and has quota
- [ ] Sample data loaded or CSV prepared
- [ ] Application running at http://localhost:8501

---

## Advanced Setup

### Option A: Use Database Instead of CSV

```bash
python db_manager.py
```

This creates a SQLite database with sample data.

To import your own CSV:
```python
from db_manager import import_csv_to_db

import_csv_to_db('your_data.csv')
```

### Option B: Deploy to Cloud

**Streamlit Cloud (Free)**
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from GitHub
4. Add API key in Streamlit Secrets

**Heroku**
```bash
heroku create your-app-name
git push heroku main
```

**AWS/Google Cloud**
- Use containerization (Docker)
- Deploy as web service

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Problem: "ANTHROPIC_API_KEY not found"

**Check:**
1. `.env` file exists in project root
2. API key is correct format (starts with `sk-`)
3. No quotes around API key in .env

**Verify:**
```bash
cat .env  # Unix/Mac
type .env  # Windows
```

### Problem: App runs but "API Error" when analyzing

**Causes:**
1. Invalid API key
2. API quota exceeded
3. Network connectivity issue

**Solutions:**
1. Verify key at [console.anthropic.com](https://console.anthropic.com)
2. Check your API usage and limits
3. Check internet connection
4. Restart app: `Ctrl+C` then `streamlit run sales_analyst_app.py`

### Problem: "Connection refused" or "Address already in use"

**Solution - Change port:**
```bash
streamlit run sales_analyst_app.py --server.port 8502
```

### Problem: Slow performance with large datasets

**Solutions:**
1. Filter to smaller date ranges
2. Use database instead of CSV for faster loading
3. Aggregate data by month instead of day
4. Increase Streamlit cache timeout:
```bash
streamlit run sales_analyst_app.py --client.caching=true
```

### Problem: Data upload fails

**Check:**
1. CSV format is correct
2. No special characters in file name
3. File size < 200MB
4. All required columns present

---

## Performance Tips

### Optimize for Speed
1. **Use indexes**: Database manager creates them automatically
2. **Filter dates**: Analyze 3-6 months instead of years
3. **Aggregate data**: Use monthly summaries for large datasets
4. **Cache results**: Streamlit caches by default

### Optimize for Accuracy
1. **Validate data**: Check for nulls and duplicates
2. **Consistent formatting**: Ensure product names match exactly
3. **Complete records**: Fill in all fields where possible
4. **Clean outliers**: Review extreme values

---

## Getting Help

### Check These First
1. README.md for feature overview
2. This setup guide for installation issues
3. Streamlit docs: https://docs.streamlit.io/
4. Anthropic docs: https://docs.anthropic.com/

### Common Questions

**Q: Can I use this with large datasets (millions of rows)?**
A: Yes, but filter by date range or aggregate to monthly data.

**Q: Can I customize the AI analysis?**
A: Yes, edit the prompt in `ai_insights.py`

**Q: What data is sent to Claude?**
A: Summary statistics and aggregated data, not raw transactions.

**Q: Can I use without internet?**
A: No, requires API connection to Claude. Dashboards work but AI features need internet.

---

## Next Steps

1. ✅ Complete this setup guide
2. 📊 Load sample data and explore
3. 🤖 Generate AI insights
4. 💡 Review recommendations
5. 📈 Prepare your own data
6. 🚀 Deploy to production

---

**Happy analyzing! 🎉**

For issues or questions, refer to the README.md or check the app's error messages for guidance.
