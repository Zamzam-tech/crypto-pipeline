-- Top coins bt market cap
WITH ranked_coins_market_cap AS(
    SELECT *,
    RANK() OVER(ORDER BY market_cap DESC) AS rank
    FROM {{ref('stg_coins')}}
),
-- Top coins by trading volume
ranked_coins_volume AS(
    SELECT *,
    RANK() OVER( ORDER BY total_volume DESC) AS rank
    FROM {{ref('stg_coins')}}
),
-- Categorize coins based on price
price_category AS(
    SELECT *,
       CASE
        WHEN current_price < 1 THEN 'Low'
        WHEN current_price >= 1 AND current_price < 100 THEN 'Medium'
       ELSE 'High'
    END AS price_category
    FROM {{ref('stg_coins')}}
)
SELECT c.coin_id,
       c.symbol,
       c.coin_name,
       c.current_price,
       c.market_cap,
       c.total_volume,
       c.last_updated,
       c.ingested_at,
       c.rank AS market_cap_rank,
       rcv.rank AS volume_rank,
       pc.price_category
FROM ranked_coins_market_cap c
JOIN ranked_coins_volume rcv ON c.coin_id = rcv.coin_id
JOIN price_category pc ON c.coin_id = pc.coin_id
WHERE c.rank <=10