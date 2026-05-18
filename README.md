# Crypto Data Pipeline

End-to-end data engineering pipeline that ingests live cryptocurrency data from CoinGecko API, transforms it using dbt, and loads it into DuckDB.

## Stack
- Python
- DuckDB
- dbt
- Airflow (coming soon)
- BigQuery (coming soon)

## Pipeline Architecture
CoinGecko API → Ingestion (Python) → DuckDB → dbt (Silver/Gold) 

## Project Structure
- `ingestion/` - API fetch and load scripts
- `dbt/crypto_pipeline/` - dbt transformation models
- `dags/` - Airflow DAGs (coming soon)

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run ingestion: `python ingestion/main.py`
3. Run dbt: `cd dbt/crypto_pipeline && dbt run`