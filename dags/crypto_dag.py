from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine')
from ingestion.crypto_ingestion import cleanup_old_files, fetch_coin_gecko, load_crypto_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='crypto_pipeline',
    schedule=timedelta(minutes=10),
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args=default_args
) as dag:
    
    fetch_task = PythonOperator(
        task_id='fetch_crypto_data',
        python_callable=fetch_coin_gecko
    )

    load_crypto = PythonOperator(
        task_id='load_data',
        python_callable=load_crypto_data
    )

    clean_up = PythonOperator(
        task_id='cleanup_old_files',
        python_callable=cleanup_old_files
    )

    run_dbt = BashOperator(
        task_id='run_dbt',
        # Added the --select flag to target your incremental crypto models specifically
        bash_command='cd /mnt/c/Users/yasab/OneDrive/Desktop/Lean\\ Data\\ pipleine/dbt/crypto_pipeline && /home/zamzam/airflow-env-311/bin/dbt run --profiles-dir /home/zamzam/.dbt'
    )

    test_dbt = BashOperator(
        task_id='test_dbt',
        # Matches the selection so you only test what just ran
        bash_command='cd /mnt/c/Users/yasab/OneDrive/Desktop/Lean\\ Data\\ pipleine/dbt/crypto_pipeline && /home/zamzam/airflow-env-311/bin/dbt test --profiles-dir /home/zamzam/.dbt'
    )

    fetch_task >> load_crypto >> clean_up >> run_dbt >> test_dbt