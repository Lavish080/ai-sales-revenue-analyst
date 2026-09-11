import json
import os
from google import genai
import pandas as pd
from sales_analyzer import SalesAnalyzer
from typing import Dict, Any

class AIInsightGenerator:
    """Generates AI-powered insights using Google Gemini API"""
    
    def __init__(self, data: pd.DataFrame, analyzer: SalesAnalyzer):
        self.data = data
        self.analyzer = analyzer
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured. Add it to Streamlit Secrets or your environment.")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
    
    def generate_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive AI insights from sales data"""
        
        # Gather all analytical data
        analysis_data = self._prepare_analysis_data(df)
        
        # Create prompt for Gemini
        prompt = self._create_analysis_prompt(analysis_data)
        
        # Call Gemini API
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        # Parse response
        response_text = response.text or ""
        
        # Extract insights
        insights = self._parse_insights(response_text, analysis_data)
        
        return insights
    
    def _prepare_analysis_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Prepare all data needed for analysis"""
        
        data = {}
        
        # Basic metrics
        data['total_revenue'] = df['revenue'].sum()
        data['total_orders'] = len(df)
        data['avg_order_value'] = df['revenue'].mean()
        data['unique_customers'] = df['customer_id'].nunique()
        
        # By product
        product_analysis = self.analyzer.get_by_dimension(df, 'product')
        data['products'] = product_analysis.to_dict('records')
        
        # By region
        region_analysis = self.analyzer.get_by_dimension(df, 'region')
        data['regions'] = region_analysis.to_dict('records')
        
        # By customer type
        customer_analysis = self.analyzer.get_customer_analysis(df)
        data['customer_analysis'] = customer_analysis
        
        # Discount impact
        discount_impact = self.analyzer.get_discount_impact(df)
        data['discount_impact'] = discount_impact.to_dict('records')
        
        # Salesperson performance
        sales_perf = self.analyzer.get_salesperson_performance(df)
        data['sales_team'] = sales_perf.to_dict('records')
        
        # Monthly trend
        trend = self.analyzer.get_monthly_trend(df)
        data['monthly_trend'] = trend.to_dict('records')
        
        # Anomalies
        anomalies = self.analyzer.identify_anomalies(df)
        data['anomalies'] = anomalies
        
        return data
    
    def _create_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Create the analysis prompt for Gemini"""
        
        prompt = f"""
You are an expert sales analyst. Analyze the following sales data and provide insights in JSON format.

SALES DATA:
Total Revenue: ${data['total_revenue']:,.2f}
Total Orders: {data['total_orders']}
Average Order Value: ${data['avg_order_value']:,.2f}
Unique Customers: {data['unique_customers']}

PRODUCT PERFORMANCE (Top 5):
{self._format_products(data['products'][:5])}

REGIONAL PERFORMANCE:
{self._format_regions(data['regions'])}

CUSTOMER INSIGHTS:
{self._format_customer_insights(data['customer_analysis'])}

DISCOUNT IMPACT:
{self._format_discount_impact(data['discount_impact'])}

SALES TEAM PERFORMANCE (Top 5):
{self._format_sales_team(data['sales_team'][:5])}

MONTHLY TREND:
{self._format_monthly_trend(data['monthly_trend'])}

ANOMALIES DETECTED:
{self._format_anomalies(data['anomalies'])}

Please provide analysis in the following JSON structure:
{{
    "summary": "A 2-3 sentence executive summary of key findings",
    "revenue_analysis": {{
        "total_revenue": "formatted revenue",
        "mom_change": percent_change,
        "yoy_change": percent_change,
        "top_products": [
            {{"name": "product", "change": percent, "revenue": "formatted"}},
        ],
        "regions": [
            {{"name": "region", "change": percent, "revenue": "formatted"}},
        ],
        "key_drivers": ["driver1", "driver2", "driver3"]
    }},
    "customer_insights": {{
        "returning_change": percent,
        "new_change": percent,
        "at_risk_count": number,
        "key_finding": "main insight about customers"
    }},
    "root_causes": [
        {{
            "cause": "specific root cause",
            "impact": "percentage or amount impact",
            "evidence": "data supporting this cause"
        }}
    ],
    "recommendations": [
        {{
            "action": "specific action to take",
            "description": "detailed description",
            "impact": "expected positive impact",
            "timeline": "timeframe to implement",
            "priority": "High/Medium/Low",
            "owner": "responsible team"
        }}
    ],
    "risks": ["risk1", "risk2"],
    "opportunities": ["opportunity1", "opportunity2"]
}}

Be specific with numbers and percentages. Focus on actionable insights.
"""
        return prompt
    
    def _format_products(self, products: list) -> str:
        formatted = ""
        for p in products:
            formatted += f"\n- {p['product']}: ${p['revenue']:,.2f} (Growth: {p.get('growth%', 0):+.1f}%)"
        return formatted
    
    def _format_regions(self, regions: list) -> str:
        formatted = ""
        for r in regions:
            formatted += f"\n- {r['region']}: ${r['revenue']:,.2f} ({r['order_count']} orders, Growth: {r.get('growth%', 0):+.1f}%)"
        return formatted
    
    def _format_customer_insights(self, customer_analysis: dict) -> str:
        formatted = "Customer Types:\n"
        for ctype, metrics in customer_analysis.get('by_type', {}).items():
            if isinstance(metrics, dict):
                formatted += f"- {ctype}: ${metrics.get('sum', 0):,.2f}\n"
        return formatted
    
    def _format_discount_impact(self, discounts: list) -> str:
        formatted = ""
        for d in discounts[:5]:
            formatted += f"\n- {d['product']}: {d['discount%']:.1f}% avg discount, Impact: ${d.get('estimated_margin', 0):,.2f}"
        return formatted
    
    def _format_sales_team(self, team: list) -> str:
        formatted = ""
        for t in team:
            formatted += f"\n- {t['salesperson']}: ${t['total_revenue']:,.2f} ({t['order_count']} orders)"
        return formatted
    
    def _format_monthly_trend(self, trend: list) -> str:
        formatted = ""
        for t in trend[-3:]:
            formatted += f"\n- {t['month']}: ${t['revenue']:,.2f} (Growth: {t.get('growth%', 0):+.1f}%)"
        return formatted
    
    def _format_anomalies(self, anomalies: dict) -> str:
        if not anomalies or not anomalies.get('declining_products'):
            return "No significant anomalies detected"
        
        formatted = ""
        for p in anomalies.get('declining_products', []):
            formatted += f"\n- {p['product']}: {p['change%']:+.1f}% change"
        return formatted
    
    def _parse_insights(self, response_text: str, analysis_data: Dict) -> Dict[str, Any]:
        """Parse Gemini's response into structured insights"""
        try:
            # Extract JSON from response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            json_str = response_text[start:end]
            
            insights = json.loads(json_str)
            
        except (json.JSONDecodeError, ValueError):
            # Fallback if parsing fails
            insights = self._generate_fallback_insights(analysis_data)
        
        return insights
    
    def _generate_fallback_insights(self, data: Dict) -> Dict[str, Any]:
        """Generate insights if Claude parsing fails"""
        
        products = data.get('products', [])
        regions = data.get('regions', [])
        
        top_declining = [p for p in products if p.get('growth%', 0) < 0][:3]
        
        return {
            'summary': f"Sales analysis shows total revenue of ${data.get('total_revenue', 0):,.2f} across {data.get('total_orders', 0)} orders.",
            'revenue_analysis': {
                'total_revenue': f"${data.get('total_revenue', 0):,.2f}",
                'mom_change': products[0].get('growth%', 0) if products else 0,
                'yoy_change': 0,
                'top_products': [{'name': p['product'], 'change': p.get('growth%', 0), 'revenue': f"${p['revenue']:,.2f}"} for p in products[:3]],
                'regions': [{'name': r['region'], 'change': r.get('growth%', 0), 'revenue': f"${r['revenue']:,.2f}"} for r in regions[:3]],
                'key_drivers': ['Product mix', 'Regional performance', 'Customer acquisition']
            },
            'customer_insights': {
                'returning_change': 0,
                'new_change': 0,
                'at_risk_count': 0,
                'key_finding': 'Analyze customer retention to identify opportunities'
            },
            'root_causes': [
                {'cause': 'Product performance variation', 'impact': 'Variable', 'evidence': 'Significant product mix changes'},
                {'cause': 'Regional demand fluctuation', 'impact': 'Variable', 'evidence': 'Uneven regional growth'}
            ],
            'recommendations': [
                {
                    'action': 'Optimize underperforming products',
                    'description': 'Review and improve products with declining revenue',
                    'impact': '5-10% revenue increase',
                    'timeline': '30 days',
                    'priority': 'High',
                    'owner': 'Product Team'
                },
                {
                    'action': 'Increase regional marketing',
                    'description': 'Focus marketing efforts on high-potential regions',
                    'impact': '8-15% regional growth',
                    'timeline': '60 days',
                    'priority': 'High',
                    'owner': 'Marketing Team'
                },
                {
                    'action': 'Reduce excessive discounting',
                    'description': 'Review discount strategy to protect margins',
                    'impact': '3-5% margin improvement',
                    'timeline': '15 days',
                    'priority': 'Medium',
                    'owner': 'Sales Management'
                }
            ],
            'risks': ['Market saturation', 'Increased competition', 'Margin compression from discounts'],
            'opportunities': ['Expand to new regions', 'Launch new products', 'Improve customer retention']
        }
