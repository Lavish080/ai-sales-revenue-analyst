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
    page_title="AI Sales & Revenue Analyst",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header { font-size: 2.5em; color: #1f77b4; margin-bottom: 0.5em; }
    .metric-card { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .negative { color: #ff6b6b; }
    .positive { color: #51cf66; }
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
st.sidebar.markdown("# 📊 AI Sales Analyst")
page = st.sidebar.radio(
    "Navigation",
    ["📤 Upload Data", "📈 Analytics Dashboard", "🤖 AI Insights", "💡 Recommendations", "📋 Data Explorer"]
)

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
elif page == "📈 Analytics Dashboard":
    if st.session_state.data is None:
        st.warning("⚠️ Please upload data first!")
    else:
        st.markdown('<div class="main-header">📈 Analytics Dashboard</div>', unsafe_allow_html=True)
        
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
        st.markdown('<div class="main-header">🤖 AI-Powered Insights</div>', unsafe_allow_html=True)
        
        # Date range
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Analysis Start Date", value=st.session_state.data['date'].min())
        with col2:
            end_date = st.date_input("Analysis End Date", value=st.session_state.data['date'].max())
        
        filtered_df = st.session_state.data[
            (st.session_state.data['date'] >= pd.Timestamp(start_date)) &
            (st.session_state.data['date'] <= pd.Timestamp(end_date))
        ]
        
        if st.button("🚀 Generate AI Analysis", use_container_width=True):
            with st.spinner("Analyzing sales data with AI..."):
                try:
                    analyzer = SalesAnalyzer(st.session_state.data)
                    insight_gen = AIInsightGenerator(st.session_state.data, analyzer)
                    
                    insights = insight_gen.generate_insights(filtered_df)
                    st.session_state.insights = insights
                    
                except Exception as e:
                    st.error(f"Error generating insights: {str(e)}")
        
        if st.session_state.insights:
            insights = st.session_state.insights
            
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
    total_revenue = float(str(total_revenue).replace('$', '').replace(',', ''))
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
elif page == "📋 Data Explorer":
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

st.sidebar.markdown("---")
st.sidebar.markdown("📧 **AI Sales Analyst v1.0**")
st.sidebar.markdown("Powered by Google Gemini AI + Streamlit")
