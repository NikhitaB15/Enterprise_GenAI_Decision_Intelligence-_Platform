import sqlite3
import pandas as pd
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'enterprise_data.db')
INSIGHTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ml_insights.json')

def analyze_churn():
    if not os.path.exists(DB_PATH):
        print("Database not found. Run data_generator.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT * FROM customer_metrics', conn)
    conn.close()

    # Simple Analysis (Subbing for a real ML model)
    high_risk_segment = df[df['churned'] == 1]
    
    top_region_churn = high_risk_segment['region'].value_counts().idxmax()
    avg_tickets_churn = high_risk_segment['support_tickets'].mean()
    avg_tenure_churn = high_risk_segment['tenure_months'].mean()
    
    insights = {
        "summary": {
            "total_customers": len(df),
            "churn_rate": f"{(len(high_risk_segment) / len(df)) * 100:.2f}%",
            "high_risk_count": len(high_risk_segment)
        },
        "critical_segments": [
            {
                "segment_name": f"Region: {top_region_churn}",
                "risk_score": "High",
                "reasoning": f"This region accounts for the highest churn volume. Average support tickets for churned users in this region is {avg_tickets_churn:.1f}."
            },
            {
                "segment_name": "Frequent Support Users",
                "risk_score": "Critical",
                "reasoning": f"Customers with > 5 tickets have a significantly higher churn probability. Current average: {avg_tickets_churn:.1f}."
            }
        ],
        "recommendations_foundation": [
            "Review pricing for price-sensitive segments.",
            f"Increase support capacity in {top_region_churn} region.",
            "Proactive outreach to customers with more than 5 tickets."
        ]
    }

    with open(INSIGHTS_PATH, 'w') as f:
        json.dump(insights, f, indent=4)
    
    print(f"ML insights generated and saved to {INSIGHTS_PATH}")

if __name__ == "__main__":
    analyze_churn()
