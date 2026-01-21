import sqlite3
import pandas as pd
import numpy as np
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'enterprise_data.db')

def generate_mock_data():
    np.random.seed(42)
    n_customers = 1000
    
    data = {
        'customer_id': range(1, n_customers + 1),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_customers),
        'monthly_spend': np.random.uniform(100, 5000, n_customers),
        'tenure_months': np.random.randint(1, 72, n_customers),
        'support_tickets': np.random.randint(0, 10, n_customers),
        'last_login_days_ago': np.random.randint(0, 30, n_customers),
        'contract_type': np.random.choice(['Monthly', 'Annual', 'Two-Year'], n_customers),
        'price_sensitivity': np.random.uniform(0, 1, n_customers),
        'churned': np.random.choice([0, 1], n_customers, p=[0.85, 0.15])
    }
    
    df = pd.DataFrame(data)
    
    # Add some bias for churn
    df.loc[df['support_tickets'] > 5, 'churned'] = np.random.choice([0, 1], len(df[df['support_tickets'] > 5]), p=[0.4, 0.6])
    df.loc[df['last_login_days_ago'] > 20, 'churned'] = np.random.choice([0, 1], len(df[df['last_login_days_ago'] > 20]), p=[0.5, 0.5])
    
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('customer_metrics', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Mock data generated and saved to {DB_PATH}")

if __name__ == "__main__":
    generate_mock_data()
