import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from sales_analyzer import SalesAnalyzer
from ai_insights import AIInsightGenerator
import io
import json

# Page config
st.set_page_config(
    page_title="AI Sales Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
# ==================== MODERN UI CSS ====================
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(55, 90, 180, 0.15), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(130, 65, 210, 0.12), transparent 30%),
        #080d16;
}

.main .block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}


/* ---------- HIDE SIDEBAR ---------- */

[data-testid="stSidebar"] {
    display: none;
}

[data-testid="collapsedControl"] {
    display: none;
}


/* ---------- TOP HEADER ---------- */

.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 22px 28px;
    margin-bottom: 16px;

    border-radius: 20px;

    background: linear-gradient(
        110deg,
        rgba(20, 40, 70, 0.98),
        rgba(24, 29, 61, 0.98)
    );

    border: 1px solid rgba(100, 135, 190, 0.22);

    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.25);
}

.header-left {
    display: flex;
    align-items: center;
    gap: 16px;
}

.brand-icon {
    width: 48px;
    height: 48px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 14px;

    background: linear-gradient(
        135deg,
        #477dff,
        #8748f5
    );

    font-size: 24px;

    box-shadow: 0 8px 22px rgba(70, 90, 255, 0.3);
}

.brand-title {
    font-size: 25px;
    font-weight: 750;
    color: #ffffff;
}

.brand-subtitle {
    font-size: 13px;
    color: #aebbd0;
    margin-top: 3px;
}

.header-right {
    text-align: right;
}

.version {
    font-size: 14px;
    color: #e3e9f5;
    font-weight: 600;
}

.powered {
    font-size: 12px;
    color: #8999b2;
    margin-top: 5px;
}

/* ---------- PAGE HEADER ---------- */

.main-header {
    font-size: 2.6rem;
    font-weight: 750;

    background: linear-gradient(
        90deg,
        #8ca8ff,
        #c48cff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-top: 25px;
    margin-bottom: 18px;
}


/* ---------- AI HERO ---------- */

.ai-hero { 
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    padding: 28px 32px; 
    margin: 20px 0; 
    border-radius: 22px; 
    background: linear-gradient(
        110deg, 
        rgba(19, 46, 82, 0.98),
        rgba(52, 38, 96, 0.98)
    ); 
    border: 1px solid rgba(105, 135, 220, 0.28); 
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25); 
} 
 
.ai-hero-left { 
    display: flex; 
    align-items: center; 
    gap: 18px; 
} 
 
.ai-icon { 
    width: 58px; 
    height: 58px; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    border-radius: 17px; 
    background: rgba(255,255,255,0.09); 
    font-size: 29px; 
} 
 
.ai-title { 
    font-size: 30px; 
    font-weight: 750; 
    color: white; 
} 
 
.ai-description { 
    margin-top: 5px; 
    color: #bdcbe0; 
    font-size: 15px; 
} 
 
.ai-status { 
    padding: 10px 16px; 
    border-radius: 20px; 
    background: rgba(130, 100, 255, 0.16); 
    border: 1px solid rgba(150, 120, 255, 0.25); 
    color: #cbbcff; 
    font-size: 13px; 
    font-weight: 600; 
}

/* ---------- CARDS ---------- */

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(20, 40, 60, 0.95),
        rgba(12, 25, 42, 0.95)
    );

    border: 1px solid rgba(80, 130, 190, 0.25);

    border-radius: 18px;

    padding: 18px;

    box-shadow: 0 8px 25px rgba(0,0,0,0.18);
}


/* ---------- BUTTONS ---------- */

.stButton > button {
    border-radius: 14px;

    border: 1px solid rgba(100, 140, 220, 0.4);

    background: linear-gradient(
        90deg,
        #477fff,
        #8b48f5
    );

    color: white;

    font-weight: 650;

    min-height: 48px;

    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 8px 25px rgba(80, 90, 255, 0.3);
}


/* ---------- INFO BOX ---------- */

[data-testid="stAlert"] {
    border-radius: 14px;
}


/* ---------- SECTION HEADINGS ---------- */

h2, h3 {
    color: #f1f5ff;
}


/* ---------- INPUTS ---------- */

div[data-baseweb="input"] {
    border-radius: 12px;
}


/* ---------- MOBILE ---------- */

@media (max-width: 900px) {
    .ai-title {
        font-size: 26px;
    }

    .main-header {
        font-size: 2rem;
    }
}

</style>
""", unsafe_allow_html=True)
# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'analysis' not in st.session_state:
    st.session_state.analysis = None
if 'insights' not in st.session_state:
    st.session_state.insights = None

# Sidebar Navigation

# ==================== TOP NAVIGATION ====================
if "page" not in st.session_state:
    st.session_state.page = "📊 Analytics Dashboard"

nav_items = [
    ("📤", "Upload Data"),
    ("📊", "Analytics Dashboard"),
    ("🤖", "AI Insights"),
    ("💡", "Recommendations"),
    ("📁", "Data Explorer")
]

nav_cols = st.columns(5)

for i, (icon, label) in enumerate(nav_items):
    with nav_cols[i]:
        full_name = f"{icon} {label}"

        if st.button(
            full_name,
            key=f"nav_{i}",
            use_container_width=True
        ):
            st.session_state.page = full_name

page = st.session_state.page

# ==================== PAGE 1: UPLOAD DATA ====================
if page == "📤 Upload Data":
    st.markdown('<div class="main-header">📤 Upload Sales Data</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("📋 Expected columns: date, product, region, customer_id, customer_type, salesperson, quantity, price, discount, revenue")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                # Data validation
                required_cols = ['date', 'product', 'region', 'customer_id', 'revenue']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.error(f"❌ Missing columns: {', '.join(missing_cols)}")
                else:
                    # Convert date
                    df['date'] = pd.to_datetime(df['date'])
                    
                    st.session_state.data = df
                    st.success("✅ Data uploaded successfully!")
                    
                    # Display preview
                    st.subheader("Data Preview")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    st.subheader("Data Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Records", len(df))
                    col2.metric("Date Range", f"{df['date'].min().date()} to {df['date'].max().date()}")
                    col3.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")
                    col4.metric("Avg Order Value", f"${df['revenue'].mean():,.2f}")
                    
                    st.subheader("Column Info")
                    st.write(df.dtypes)
                    
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    
    with col2:
        st.subheader("📝 Or Use Sample Data")
        if st.button("Load Sample Dataset", use_container_width=True):
            from sample_data import generate_sample_data
            sample_df = generate_sample_data()
            st.session_state.data = sample_df
            st.success("✅ Sample data loaded!")
            st.rerun()

# ==================== PAGE 2: ANALYTICS DASHBOARD ====================
elif page == "📊 Analytics Dashboard":
    if st.session_state.data is None:
        st.warning("⚠️ Please upload data first!")
    else:
        st.markdown('<div class="main-header">📊 Analytics Dashboard</div>', unsafe_allow_html=True)        
        # Initialize analyzer
        analyzer = SalesAnalyzer(st.session_state.data)
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=st.session_state.data['date'].min())
        with col2:
            end_date = st.date_input("End Date", value=st.session_state.data['date'].max())
        
        # Filter data
        filtered_df = st.session_state.data[
            (st.session_state.data['date'] >= pd.Timestamp(start_date)) &
            (st.session_state.data['date'] <= pd.Timestamp(end_date))
        ]
        
        # Key Metrics
        st.subheader("📊 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_revenue = filtered_df['revenue'].sum()
        total_orders = len(filtered_df)
        avg_order_value = filtered_df['revenue'].mean()
        
        # Calculate MoM change if possible
        prev_month_start = start_date.replace(day=1) - timedelta(days=1)
        prev_month_start = prev_month_start.replace(day=1)
        prev_month_end = start_date.replace(day=1) - timedelta(days=1)
        
        prev_data = st.session_state.data[
            (st.session_state.data['date'] >= pd.Timestamp(prev_month_start)) &
            (st.session_state.data['date'] <= pd.Timestamp(prev_month_end))
        ]
        prev_revenue = prev_data['revenue'].sum()
        
        if prev_revenue > 0:
            mom_change = ((total_revenue - prev_revenue) / prev_revenue) * 100
        else:
            mom_change = 0
        
        with col1:
            st.metric("Total Revenue", f"${total_revenue:,.2f}", f"{mom_change:+.1f}%")
        with col2:
            st.metric("Total Orders", f"{total_orders:,}")
        with col3:
            st.metric("Avg Order Value", f"${avg_order_value:,.2f}")
        with col4:
            conversion_rate = len(filtered_df[filtered_df['customer_type'] == 'new']) / len(filtered_df) * 100
            st.metric("New Customers %", f"{conversion_rate:.1f}%")
        
        # Revenue Trend
        st.subheader("💹 Revenue Trend")
        trend_data = analyzer.get_monthly_trend(filtered_df)
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=trend_data['month'],
            y=trend_data['revenue'],
            mode='lines+markers',
            fill='tozeroy',
            name='Revenue',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        fig_trend.update_layout(
            title="Monthly Revenue Trend",
            xaxis_title="Month",
            yaxis_title="Revenue ($)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Multi-dimensional Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏢 Revenue by Product")
            product_data = analyzer.get_by_dimension(filtered_df, 'product')
            fig_prod = px.bar(
                product_data,
                x='product',
                y='revenue',
                color='growth%',
                color_continuous_scale='RdYlGn',
                hover_data={'revenue': ':.2f', 'growth%': ':.1f'}
            )
            fig_prod.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig_prod, use_container_width=True)
        
        with col2:
            st.subheader("🌍 Revenue by Region")
            region_data = analyzer.get_by_dimension(filtered_df, 'region')
            fig_reg = px.pie(
                region_data,
                values='revenue',
                names='region',
                hole=0.4
            )
            fig_reg.update_layout(height=400)
            st.plotly_chart(fig_reg, use_container_width=True)
        
        # Additional Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 Revenue by Customer Type")
            cust_data = analyzer.get_by_dimension(filtered_df, 'customer_type')
            fig_cust = px.bar(
                cust_data,
                x='customer_type',
                y='revenue',
                color='revenue',
                color_continuous_scale='Viridis'
            )
            fig_cust.update_layout(height=400)
            st.plotly_chart(fig_cust, use_container_width=True)
        
        with col2:
            st.subheader("💰 Discount Impact")
            discount_data = analyzer.get_discount_impact(filtered_df)
            fig_disc = px.scatter(
                discount_data,
                x='discount%',
                y='revenue',
                size='quantity',
                color='revenue',
                hover_name='product',
                color_continuous_scale='Blues'
            )
            fig_disc.update_layout(height=400)
            st.plotly_chart(fig_disc, use_container_width=True)

# ==================== PAGE 3: AI INSIGHTS ====================
elif page == "🤖 AI Insights":
    if st.session_state.data is None:
        st.warning("⚠️ Please upload data first!")
    else:
        st.markdown("""
        <div class="ai-hero">
            <div class="ai-hero-left">
                <div class="ai-icon">🤖</div>

                <div>
                    <div class="ai-title">AI-Powered Insights</div>
                    <div class="ai-description">
                        Get intelligent analysis and actionable insights from your sales data
                    </div>
                </div>
            </div>

            <div class="ai-status">✨ Gemini AI</div>
        </div>
        """, unsafe_allow_html=True)

        # Date range
        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input(
                "Analysis Start Date",
                value=st.session_state.data['date'].min()
            )

        with col2:
            end_date = st.date_input(
                "Analysis End Date",
                value=st.session_state.data['date'].max()
            )
            # Main Insight Card
            st.markdown("### 🎯 Executive Summary")
            st.info(insights.get('summary', ''))
            
            # Revenue Analysis
            st.markdown("### 💹 Revenue Analysis")
            revenue_section = insights.get('revenue_analysis', {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                total_revenue = revenue_section.get('total_revenue', 0)
                
                try:
                    total_revenue = float(
                        str(total_revenue).replace('$', '').replace(',', '')
                    )
                except (ValueError, TypeError):
                    total_revenue = 0
                    
                st.metric(
                    "Current Period Revenue",
                    f"${total_revenue:,.2f}"
                )
            with col2:
                st.metric("MoM Change", 
                         f"{revenue_section.get('mom_change', 0):+.1f}%",
                         delta_color="normal")
            with col3:
                st.metric("YoY Change", 
                         f"{revenue_section.get('yoy_change', 0):+.1f}%")
            
            # Dimensional Analysis
            st.markdown("### 📊 Analysis by Dimension")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Top Performing Products:**")
                products = revenue_section.get('top_products', [])
                for i, prod in enumerate(products[:3], 1):
                    st.write(f"{i}. {prod['name']}: {prod['change']:+.1f}% ({prod['revenue']})")
            
            with col2:
                st.markdown("**Regional Performance:**")
                regions = revenue_section.get('regions', [])
                for i, region in enumerate(regions[:3], 1):
                    st.write(f"{i}. {region['name']}: {region['change']:+.1f}% ({region['revenue']})")
            
            # Customer Insights
            st.markdown("### 👥 Customer Insights")
            customer_insights = insights.get('customer_insights', {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Returning Customers:** {customer_insights.get('returning_change', 0):+.1f}%")
            with col2:
                st.write(f"**New Customers:** {customer_insights.get('new_change', 0):+.1f}%")
            with col3:
                st.write(f"**At-Risk Customers:** {customer_insights.get('at_risk_count', 0)}")
            
            # Root Cause Analysis
            st.markdown("### 🔍 Root Cause Analysis")
            root_causes = insights.get('root_causes', [])
            for i, cause in enumerate(root_causes, 1):
                st.write(f"**{i}. {cause['cause']}**")
                st.write(f"   Impact: {cause['impact']}")
                st.write(f"   Evidence: {cause['evidence']}")

# ==================== PAGE 4: RECOMMENDATIONS ====================
elif page == "💡 Recommendations":
    if st.session_state.insights is None:
        st.warning("⚠️ Please generate AI insights first!")
    else:
        st.markdown('<div class="main-header">💡 Strategic Recommendations</div>', unsafe_allow_html=True)
        
        insights = st.session_state.insights
        recommendations = insights.get('recommendations', [])
        
        st.subheader("Recommended Actions")
        
        for i, rec in enumerate(recommendations, 1):
            with st.expander(f"**{i}. {rec['action']}**", expanded=i==1):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Description:** {rec['description']}")
                    st.write(f"**Expected Impact:** {rec['impact']}")
                    st.write(f"**Timeline:** {rec['timeline']}")
                    st.write(f"**Owner:** {rec.get('owner', 'Sales Team')}")
                
                with col2:
                    priority = rec.get('priority', 'Medium')
                    color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}.get(priority, '🟡')
                    st.metric("Priority", f"{color} {priority}")

# ==================== PAGE 5: DATA EXPLORER ====================
elif page == "📁 Data Explorer":
    if st.session_state.data is None:
        st.warning("⚠️ Please upload data first!")
    else:
        st.markdown('<div class="main-header">📋 Data Explorer</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Filter by Product")
            products = st.multiselect("Select Products", 
                                     options=st.session_state.data['product'].unique(),
                                     default=st.session_state.data['product'].unique()[:3])
        
        with col2:
            st.subheader("Filter by Region")
            regions = st.multiselect("Select Regions",
                                    options=st.session_state.data['region'].unique(),
                                    default=st.session_state.data['region'].unique())
        
        # Apply filters
        filtered_df = st.session_state.data[
            (st.session_state.data['product'].isin(products)) &
            (st.session_state.data['region'].isin(regions))
        ]
        
        st.subheader(f"Data ({len(filtered_df)} records)")
        st.dataframe(filtered_df.sort_values('date', ascending=False), use_container_width=True)
        
        # Download
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data",
            data=csv,
            file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
