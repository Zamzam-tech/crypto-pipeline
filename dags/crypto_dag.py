from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine')
from ingestion.crypto_ingestion import cleanup_old_files, fetch_coin_gecko, load_crypto_data

with DAG(
    dag_id='crypto_pipeline',
    schedule=timedelta(minutes=30),  # Run every 30 minutes
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

    #Schedule task 3 which is cleaning up old files to save space
    clean_up=PythonOperator(
        task_id='cleanup_old_files',
        python_callable=cleanup_old_files
    )

    # Schedule task 3 which is a bash command to run dbt transformations
    run_dbt = BashOperator(
    task_id='run_dbt',
    bash_command='cd /mnt/c/Users/yasab/OneDrive/Desktop/Lean\\ Data\\ pipleine/dbt/crypto_pipeline && /home/zamzam/airflow-env-311/bin/dbt run --profiles-dir /home/zamzam/.dbt'
)

    #Schedule task for which is abash command to run dbt tests
    
    test_dbt = BashOperator(
    task_id='test_dbt',
    bash_command='cd /mnt/c/Users/yasab/OneDrive/Desktop/Lean\\ Data\\ pipleine/dbt/crypto_pipeline && /home/zamzam/airflow-env-311/bin/dbt test --profiles-dir /home/zamzam/.dbt'
)

    #Defining task dependencies
    fetch_task >> load_crypto >> clean_up >> run_dbt >> test_dbt