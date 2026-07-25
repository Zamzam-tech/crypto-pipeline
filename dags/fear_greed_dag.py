from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine')
from ingestion.fear_greed_ingestion import fetch_fear_greed, load_fear_greed

with DAG(
    dag_id='fear_greed_pipeline',
    schedule=timedelta(hours=24),  # Run once a day
    start_date=datetime(2026, 1, 1),
    catchup=False
) as dag:

    # Task 1 — Fetch Fear & Greed from alternative.me
    fetch_fg = PythonOperator(
        task_id='fetch_fear_greed',
        python_callable=fetch_fear_greed
    )

    # Task 2 — Load into DuckDB
    load_fg = PythonOperator(
        task_id='load_fear_greed',
        python_callable=load_fear_greed
    )

    # Task 3 — Run dbt transformations
    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command='cd /mnt/c/Users/yasab/OneDrive/Desktop/Lean\\ Data\\ pipleine/dbt/crypto_pipeline && /home/zamzam/airflow-env-311/bin/dbt run --profiles-dir /home/zamzam/.dbt'
    )

    # Task 4 — Run dbt tests
    test_dbt = BashOperator(
        task_id='test_dbt',
        bash_command='cd /mnt/c/Users/yasab/OneDrive/Desktop/Lean\\ Data\\ pipleine/dbt/crypto_pipeline && /home/zamzam/airflow-env-311/bin/dbt test --profiles-dir /home/zamzam/.dbt'
    )

    # Task dependencies
    fetch_fg >> load_fg >> run_dbt >> test_dbt