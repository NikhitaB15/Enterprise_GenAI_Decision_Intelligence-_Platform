import sqlite3
import pandas as pd
import numpy as np
import os

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
CSV_PATH = os.path.join(DATA_DIR, 'WA_Fn-UseC_-Telco-Customer-Churn.csv')
DB_PATH = os.path.join(DATA_DIR, 'enterprise_data.db')

def prepare_data():
    print(f"Loading data from {CSV_PATH}...")
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)
    
    # Data Cleaning
    # TotalCharges can be empty strings, coerce to numeric
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    
    # Convert Churn to binary 0/1 for easier SQL analysis later
    df['Churn'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    # Store in SQLite
    conn = sqlite3.connect(DB_PATH)
    
    # Write to 'customer_metrics' table, matching the previous schema name but new columns
    df.to_sql('customer_metrics', conn, if_exists='replace', index=False)
    
    print(f"Data ingested. {len(df)} rows saved to 'customer_metrics' table in {DB_PATH}")
    
    # Verify
    print("Columns:", list(df.columns))
    conn.close()

if __name__ == "__main__":
    prepare_data()
