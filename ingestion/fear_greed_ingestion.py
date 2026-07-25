import requests
import json
import duckdb
from datetime import datetime
from google.cloud import bigquery  # <-- Swapped duckdb for bigquery

DB_PATH = "/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine/ingestion/crypto_data.db"
FG_PATH = "/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine/ingestion/fear_greed_raw.json"

def fetch_fear_greed():
    """Fetch Fear & Greed Index - 100 days history"""
    url = "https://api.alternative.me/fng/?limit=100"
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    results = []
    for entry in data['data']:
        results.append({
            'score': entry['value'],
            'classification': entry['value_classification'],
            'timestamp': entry['timestamp'],
            'fetched_at': datetime.now().isoformat()
        })
    
    with open(FG_PATH, 'w') as f:
        json.dump(results, f)
    
    print(f"Fear & Greed fetched: {len(results)} days ✅")


import json
from datetime import datetime
import duckdb
from google.cloud import bigquery

def load_fear_greed():
    """
    Production Pattern: Load Fear & Greed data into DuckDB as a resilient 
    local staging layer, then mirror the FULL historical state to BigQuery.
    """
    with open(FG_PATH, 'r') as f:
        data = json.load(f)
    
    conn = duckdb.connect(DB_PATH)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS fear_greed (
            score INTEGER,
            classification VARCHAR,
            fetch_date DATE,
            fetched_at TIMESTAMP
        )
    """)
    
    inserted = 0
    for entry in data:
        fetch_date = datetime.fromtimestamp(int(entry['timestamp'])).date()
        existing = conn.execute(
            "SELECT COUNT(*) FROM fear_greed WHERE fetch_date = ?", 
            [fetch_date]
        ).fetchone()[0]
        
        if existing == 0:
            conn.execute(
                "INSERT INTO fear_greed VALUES (?, ?, ?, ?)", 
                [int(entry['score']), entry['classification'], fetch_date, entry['fetched_at']]
            )
            inserted += 1
    
    print(f"Staging complete: {inserted} new records committed to local DuckDB. 🗄️")

    # Read the FULL local table state so we can populate BigQuery
    # ====================================================================
    sync_df = conn.execute("""
        SELECT 
            score, 
            classification, 
            fetch_date, 
            CAST(fetched_at AS TIMESTAMP) as fetched_at 
        FROM fear_greed
    """).df()
    conn.close() 

    # Sync local state to Google Cloud Data Warehouse
    if not sync_df.empty:
        client = bigquery.Client()
        table_id = "crypto-pipeline-project-500308.crypto_raw.fear_greed" 
        
        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("score", "INTEGER"),
                bigquery.SchemaField("classification", "STRING"),
                bigquery.SchemaField("fetch_date", "DATE"),
                bigquery.SchemaField("fetched_at", "TIMESTAMP"),
            ],
            write_disposition="WRITE_TRUNCATE" # Wipes the empty cloud table and drops the full history in
        )
        
        print(f"Initiating cloud sync to BigQuery target table: {table_id}... Total rows: {len(sync_df)}")
        job = client.load_table_from_dataframe(sync_df, table_id, job_config=job_config)
        job.result()  # Wait for cloud upload to finish
        
        print(f"Cloud Sync Successful! BigQuery table '{table_id}' is live and healthy. ☁️🚀")
    else:
        print("Staging table is completely empty. Nothing to sync.")

if __name__ == "__main__":
    print("Running local end-to-end integration test...")
    fetch_fear_greed()
    load_fear_greed()