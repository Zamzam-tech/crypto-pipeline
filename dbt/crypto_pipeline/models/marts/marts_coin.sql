WITH latest_snapshot AS (
    SELECT *
    FROM {{ ref('stg_coins') }}
    WHERE ingested_at = (SELECT MAX(ingested_at) FROM {{ ref('stg_coins') }})
),
ranked AS (
    SELECT *,
        RANK() OVER(ORDER BY market_cap DESC) AS market_cap_rank,
        RANK() OVER(ORDER BY total_volume DESC) AS volume_rank,
        CASE
            WHEN current_price < 1 THEN 'Low'
            WHEN current_price >= 1 AND current_price < 100 THEN 'Medium'
            ELSE 'High'
        END AS price_category
    FROM latest_snapshot
)
SELECT 
    coin_id,
    symbol,
    coin_name,
    current_price,
    market_cap,
    total_volume,
    last_updated,
    ingested_at,
    market_cap_rank,
    volume_rank,
    price_category
FROM ranked
WHERE market_cap_rank <= 10