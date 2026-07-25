import requests
import pandas as pd
from google.cloud import bigquery  # <-- Swapped duckdb for bigquery
import os
import glob

#Function to fetch crypto data from CoinGecko API
def fetch_coin_gecko():
    URL = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd", # Fetch prices in USD
        "order": "market_cap_desc", # Order by market cap descending
        "per_page": 50, # Fetch top 50 coins
        "page": 1, # Fetch the first page
        "sparkline": False # Do not include sparkline data
    }
# Handle potential request errors gracefully
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data)
        df["ingested_at"] = pd.Timestamp.utcnow()
        df = df[[
            "id", "symbol", "name",
            "current_price", "market_cap",
            "total_volume", "last_updated",
            "ingested_at"
        ]]

        timestamp = pd.Timestamp.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine/ingestion/cgk_raw_{timestamp}.json"
        df.to_json(filename, orient="records", indent=4)
        print(f"Crypto data fetched and saved to {filename}")

        with open("/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine/ingestion/latest_file.txt", "w") as f:
            f.write(filename)

    except requests.RequestException as e:
        print(f"Error fetching crypto data: {e}")


def load_crypto_data():
    try:
        # 1. Read the latest file path
        with open("/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine/ingestion/latest_file.txt", "r") as f:
            filename = f.read().strip()

        # 2. Load the JSON data back into a Pandas DataFrame
        df = pd.read_json(filename)

        # 3. Initialize the BigQuery Client (picks up your key automatically!)
        client = bigquery.Client()
        
        # Targets your dataset 'crypto_raw' and table 'crypto_data'
        table_id = f"{client.project}.crypto_raw.crypto_data"
        print(f"Loading transformed crypto data into BigQuery table: {table_id}...")

        # 4. Configure the load job to append data 
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )

        # 5. Ship it to the cloud!
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # Waits for the table upload to complete

        print("Success! Crypto data loaded into BigQuery.")

    except Exception as e:
        print(f"Error loading data into BigQuery: {e}")


# Remove old files to save space
def cleanup_old_files():
    files = glob.glob("/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine/ingestion/cgk_raw_*.json")
    for file in files:
        os.remove(file)
    print(f"Deleted old files to save space.")
            

if __name__ == "__main__":
    fetch_coin_gecko()
    load_crypto_data()
    cleanup_old_files()