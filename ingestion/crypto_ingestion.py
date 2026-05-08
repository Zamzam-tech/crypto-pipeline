import requests
import json
import pandas as pd
import duckdb

def fetch_coin_gecko():
    URL="https://api.coingecko.com/api/v3/coins/markets"
    params={
        "vs_currency":"usd",
        "order":"market_cap_desc",
        "per_page":50,
        "page":1,
        "sparkline":False
    }
    #Fetching live data
    try:
        response=requests.get(URL, params=params)
    except requests.RequestException as e:
        print(f"Error fetching crypto data: {e}")
        return None

    if response.status_code==200:
        df=pd.DataFrame(response.json())
        #Selecting relevant columns
        df['ingested_at']=pd.Timestamp.now().isoformat()
        df=df[["id","symbol","name","current_price","market_cap","total_volume","last_updated","ingested_at"]]
        df.to_json("cgk_raw.json", orient="records", indent=4)
        print("Crypto data fetched and saved to cgk_raw.json")
    else:
        print(f"Failed to fetch crypto data. Status code: {response.status_code}")
    return df

# loading data into DuckDB
def load_crypto_data():
    try:
        connect_db=duckdb.connect("crypto_data.db")
        print("Loading transformed crypto data into DuckDB...")
        connect_db.execute("""
        CREATE OR REPLACE TABLE crypto_data AS
        SELECT * FROM read_json('cgk_raw.json');
        """)
        print(" Success! Crypto data loaded into DuckDB.")

        #Querying data from DuckDB to verify
        connect_db.sql("SELECT id, symbol, current_price FROM crypto_data LIMIT 5").show()

        connect_db.close()
    except duckdb.Error as e:
        print(f"Error loading data into DuckDB: {e}")
        return None
    

    

if __name__=="__main__":
    fetch_coin_gecko()  
    load_crypto_data()
