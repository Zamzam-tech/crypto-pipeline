import requests
import json
import duckdb
from datetime import datetime

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


def load_fear_greed():
    """Load Fear & Greed data into DuckDB — no duplicates"""
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
        
        existing = conn.execute("""
            SELECT COUNT(*) FROM fear_greed 
            WHERE fetch_date = ?
        """, [fetch_date]).fetchone()[0]
        
        if existing == 0:
            conn.execute("""
                INSERT INTO fear_greed VALUES (?, ?, ?, ?)
            """, [int(entry['score']), entry['classification'], fetch_date, entry['fetched_at']])
            inserted += 1
    
    conn.close()
    print(f"Fear & Greed: {inserted} new rows loaded ✅")


if __name__ == "__main__":
    fetch_fear_greed()
    load_fear_greed()
