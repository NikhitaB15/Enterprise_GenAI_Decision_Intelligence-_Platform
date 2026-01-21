from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add the project root to path to import ml scripts
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ml.data_generator import generate_mock_data
from ml.churn_reasoning import analyze_churn

default_args = {
    'owner': 'data_science',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'enterprise_intelligence_pipeline',
    default_args=default_args,
    description='Re-generate mock data and refresh ML insights for the GenAI platform',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id='ingest_data',
        python_callable=generate_mock_data,
    )

    t2 = PythonOperator(
        task_id='run_ml_analytics',
        python_callable=analyze_churn,
    )

    t1 >> t2
