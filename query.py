import duckdb
import sys

DB_PATH = "/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine/crypto_data.db"
SQL_FILE = sys.argv[1] if len(sys.argv) > 1 else "queries/explore.sql"

conn = duckdb.connect(DB_PATH, read_only=True)
results = conn.sql(open(SQL_FILE).read())
print(results)
conn.close()