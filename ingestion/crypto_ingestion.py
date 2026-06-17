import requests
import pandas as pd
import duckdb
import os
import glob

def fetch_coin_gecko():
    URL = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }

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
        with open("/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine/ingestion/latest_file.txt", "r") as f:
            filename = f.read().strip()

        connect_db = duckdb.connect("/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine/ingestion/crypto_data.db")
        print("Loading transformed crypto data into DuckDB...")

        connect_db.execute("""
        CREATE TABLE IF NOT EXISTS crypto_data (
            id TEXT,
            symbol TEXT,
            name TEXT,
            current_price DOUBLE,
            market_cap DOUBLE,
            total_volume DOUBLE,
            last_updated TEXT,
            ingested_at TIMESTAMP
        )
        """)

        connect_db.execute(f"INSERT INTO crypto_data SELECT * FROM read_json('{filename}')")
        print("Success! Crypto data loaded into DuckDB.")

        connect_db.sql("SELECT id as coin_id,MAX(current_price) as highest_price,MIN(current_price) as lowest_price,AVG(current_price) as avg_price FROM crypto_data GROUP BY id;").show()
        connect_db.close()

    except Exception as e:
        print(f"Error loading data into DuckDB: {e}")

#Remove old files to save space
def cleanup_old_files():
    files=glob.glob("/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine/ingestion/cgk_raw_*.json")
    for file in files:
        os.remove(file)
        print(f"Deleted {len(files)} old files to save space.")
            

if __name__ == "__main__":
    fetch_coin_gecko()
    load_crypto_data()
    cleanup_old_files()