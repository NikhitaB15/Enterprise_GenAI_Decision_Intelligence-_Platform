import sqlite3
import pandas as pd
import json
import os
from langchain.tools import tool

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'enterprise_data.db')
INSIGHTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ml_insights.json')

@tool
def query_db(query: str) -> str:
    """Execute a SQL query against the enterprise database. 
    Tables: 
    - customers (customer_id, name, region, sector, tenure_months, monthly_spend)
    - support_tickets (ticket_id, customer_id, status, priority, created_at)
    - transactions (tx_id, customer_id, amount, date, status)
    - ml_insights (customer_id, churn_risk_score, predicted_churn, primary_churn_factor)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_json(orient='records')
    except Exception as e:
        return f"Error executing query: {str(e)}"

@tool
def get_ml_insights(customer_id: str = None) -> str:
    """Retrieve predictive ML insights for a specific customer or all customers."""
    try:
        conn = sqlite3.connect(DB_PATH)
        query = f"SELECT * FROM ml_insights"
        if customer_id:
            query += f" WHERE customer_id = '{customer_id}'"
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_json(orient='records')
    except Exception as e:
        return f"Error reading insights: {str(e)}"

@tool
def get_company_policy(topic: str) -> str:
    """Search for company policies in the /docs folder (pricing, retention, support)."""
    topic_map = {
        "pricing": "pricing_policy.md",
        "retention": "retention_strategy.md",
        "support": "retention_strategy.md" # Reusing for now
    }
    
    filename = topic_map.get(topic.lower())
    if not filename:
        return f"No documentation found for topic: {topic}"
        
    doc_path = os.path.join(os.path.dirname(__file__), '..', 'docs', filename)
    try:
        if os.path.exists(doc_path):
            with open(doc_path, 'r') as f:
                return f.read()
        return f"Policy document {filename} not found."
    except Exception as e:
        return f"Error reading policy: {str(e)}"
