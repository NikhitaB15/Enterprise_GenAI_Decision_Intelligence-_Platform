import sqlite3
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'enterprise_data.db')

def generate_mock_data():
    np.random.seed(42)
    n_customers = 1000
    
    # 1. Customers Table (Enterprise/Telco Style)
    customers = {
        'customer_id': [f"CUST-{i:04d}" for i in range(1, n_customers + 1)],
        'name': [f"Enterprise Client {i}" for i in range(1, n_customers + 1)],
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_customers),
        'sector': np.random.choice(['Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing'], n_customers),
        'tenure_months': np.random.randint(1, 72, n_customers),
        'contract_type': np.random.choice(['Monthly', 'Annual', 'Two-Year'], n_customers),
        'monthly_spend': np.random.uniform(500, 15000, n_customers),
        'total_spend': 0, # Will calculate
    }
    customers_df = pd.DataFrame(customers)
    customers_df['total_spend'] = customers_df['monthly_spend'] * customers_df['tenure_months']

    # 2. Support Tickets Table (Synthetic High-Fidelity)
    n_tickets = 5000
    tickets = {
        'ticket_id': [f"TKT-{i:05d}" for i in range(1, n_tickets + 1)],
        'customer_id': np.random.choice(customers_df['customer_id'], n_tickets),
        'status': np.random.choice(['Closed', 'Resolved', 'Open', 'Escalated'], n_tickets, p=[0.6, 0.2, 0.15, 0.05]),
        'priority': np.random.choice(['Low', 'Medium', 'High', 'Urgent'], n_tickets),
        'created_at': [(datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(n_tickets)]
    }
    tickets_df = pd.DataFrame(tickets)

    # 3. Transactions Table
    n_transactions = 10000
    transactions = {
        'tx_id': [f"TX-{i:06d}" for i in range(1, n_transactions + 1)],
        'customer_id': np.random.choice(customers_df['customer_id'], n_transactions),
        'amount': np.random.uniform(100, 5000, n_transactions),
        'date': [(datetime.now() - timedelta(days=np.random.randint(0, 90))).strftime('%Y-%m-%d') for _ in range(n_transactions)],
        'status': np.random.choice(['Success', 'Failed', 'Pending'], n_transactions, p=[0.95, 0.03, 0.02])
    }
    transactions_df = pd.DataFrame(transactions)

    # 4. ML Insights Table (Synthetic prediction outputs)
    insights = {
        'customer_id': customers_df['customer_id'],
        'churn_risk_score': np.random.uniform(0, 1, n_customers),
        'predicted_churn': 0,
        'primary_churn_factor': np.random.choice(['Price Sensitivity', 'High Ticket Volume', 'Lack of Usage', 'Competitor Offer'], n_customers)
    }
    insights_df = pd.DataFrame(insights)
    insights_df['predicted_churn'] = (insights_df['churn_risk_score'] > 0.7).astype(int)

    # Save to SQLite
    conn = sqlite3.connect(DB_PATH)
    customers_df.to_sql('customers', conn, if_exists='replace', index=False)
    tickets_df.to_sql('support_tickets', conn, if_exists='replace', index=False)
    transactions_df.to_sql('transactions', conn, if_exists='replace', index=False)
    insights_df.to_sql('ml_insights', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"Realistic Enterprise Data generated with 4 tables in {DB_PATH}")

if __name__ == "__main__":
    generate_mock_data()
