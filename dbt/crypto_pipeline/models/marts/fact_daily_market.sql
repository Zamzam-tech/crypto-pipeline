WITH daily_crypto AS (
    SELECT
        DATE(ingested_at) as date,
        coin_name,
        AVG(current_price) as avg_price,
        MAX(current_price) as high_price,
        MIN(current_price) as low_price,
        AVG(total_volume) as avg_volume,
        AVG(market_cap) as avg_market_cap
    FROM {{ ref('stg_coins') }}
    GROUP BY DATE(ingested_at), coin_name
),
sentiment AS (
    SELECT * FROM {{ ref('stg_fear_greed') }}
)
SELECT
    c.date,
    c.coin_name,
    c.avg_price,
    c.high_price,
    c.low_price,
    c.avg_volume,
    c.avg_market_cap,
    s.fear_greed_score,
    s.sentiment
FROM daily_crypto c
LEFT JOIN sentiment s ON c.date = s.fetch_date
ORDER BY c.date DESC, c.avg_market_cap DESC
