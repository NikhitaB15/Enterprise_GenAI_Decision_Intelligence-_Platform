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
    # Join customers with tickets and insights
    query = """
    SELECT c.*, i.churn_risk_score, i.primary_churn_factor,
           (SELECT COUNT(*) FROM support_tickets WHERE customer_id = c.customer_id) as ticket_count
    FROM customers c
    JOIN ml_insights i ON c.customer_id = i.customer_id
    """
    df = pd.read_sql(query, conn)
    conn.close()

    high_risk_segment = df[df['churn_risk_score'] > 0.7]
    
    top_region_risk = high_risk_segment['region'].value_counts().idxmax()
    avg_tickets_risk = high_risk_segment['ticket_count'].mean()
    
    insights = {
        "summary": {
            "total_customers": len(df),
            "high_risk_percentage": f"{(len(high_risk_segment) / len(df)) * 100:.2f}%",
            "at_risk_count": len(high_risk_segment)
        },
        "critical_segments": [
            {
                "segment_name": f"Region: {top_region_risk}",
                "risk_score": "High",
                "reasoning": f"This region has the highest concentration of at-risk customers. Average ticket volume here is {avg_tickets_risk:.1f}."
            },
            {
                "segment_name": "High Support Load",
                "risk_score": "Critical",
                "reasoning": f"At-risk customers are averaging {avg_tickets_risk:.1f} support tickets. Primary driver: {high_risk_segment['primary_churn_factor'].iloc[0]}."
            }
        ],
        "recommendations_foundation": [
            "Initiate high-touch outreach for accounts in the North region.",
            "Deploy specialized success managers for technical support escalations.",
            "Review contract types for high-spend annual clients showing low usage."
        ]
    }

    with open(INSIGHTS_PATH, 'w') as f:
        json.dump(insights, f, indent=4)
    
    print(f"Enterprise ML insights generated and saved to {INSIGHTS_PATH}")

if __name__ == "__main__":
    analyze_churn()
