from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine')
from ingestion.crypto_ingestion import fetch_coin_gecko, load_crypto_data

with DAG(
    dag_id='crypto_pipeline',
    schedule='@hourly',
    start_date=datetime(2026, 1, 1),
    catchup=False
) as dag:
    
    #Schedule task 1 which is Fetching crypto data
    fetch_task=PythonOperator(
        task_id='fetch_crypto_data',
        python_callable=fetch_coin_gecko
    )

    #Schedule task 2 which is loading data into DuckDB
    load_crypto=PythonOperator(
        task_id='load_data',
        python_callable=load_crypto_data
    )

    # Schedule task 3 which is a bash command to run dbt transformations
    run_dbt=BashOperator(
        task_id='run_dbt',
        bash_command='cd /mnt/c/Users/yasab/OneDrive/Desktop/Lean\\ Data\\ pipleine/dbt/crypto_pipeline && dbt run'
    )

    #Schedule task for which is abash command to run dbt tests
    test_dbt=BashOperator(
        task_id='test_dbt',
        bash_command='cd /mnt/c/Users/yasab/OneDrive/Desktop/Lean\\ Data\\ pipleine/dbt/crypto_pipeline && dbt run'
    )

    #Defining task dependencies
    fetch_task >> load_crypto >> run_dbt >> test_dbt