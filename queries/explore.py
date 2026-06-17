import duckdb

conn = duckdb.connect('ingestion/crypto_data.db')

print('FACT DAILY MARKET - Bitcoin + Fear & Greed:')
print(conn.execute("""
    SELECT date, coin_name, avg_price, fear_greed_score, sentiment
    FROM fact_daily_market
    WHERE coin_name = 'Bitcoin'
    ORDER BY date DESC
    LIMIT 10
""").df())

conn.close()