import sqlite3
import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
CSV_PATH = os.path.join(DATA_DIR, 'WA_Fn-UseC_-Telco-Customer-Churn.csv')
LOCAL_DB_PATH = os.path.join(DATA_DIR, 'enterprise_data.db')

def get_db_engine():
    """Returns the database engine based on environment configuration."""
    db_url = os.getenv('DATABASE_URL')
    if db_url and db_url.startswith('postgres'):
        # Fix for SQLAlchemy requiring postgresql:// instead of postgres://
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        print("Connecting to External Database (Supabase)...")
        return create_engine(db_url)
    else:
        print(f"Connecting to Local SQLite: {LOCAL_DB_PATH}")
        return create_engine(f'sqlite:///{LOCAL_DB_PATH}')

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
    
    # Store in Database
    engine = get_db_engine()
    
    try:
        # Write to 'customer_metrics' table
        df.to_sql('customer_metrics', engine, if_exists='replace', index=False)
        print(f"Data ingested. {len(df)} rows saved to 'customer_metrics' table.")
        
        # Verify
        print("Columns:", list(df.columns))
    except Exception as e:
        print(f"Error saving to database: {e}")

if __name__ == "__main__":
    prepare_data()
