{{
    config(
        materialized='table',
        partition_by={
            "field": "date",
            "data_type": "date"
        }
    )
}}

WITH daily_volume AS (
    SELECT
        DATE(ingested_at) as date,
        coin_name,
        AVG(total_volume) as avg_volume
    FROM {{ ref('stg_coins') }}
    GROUP BY DATE(ingested_at), coin_name
),
ranked AS (
    SELECT
        date,
        coin_name,
        avg_volume,
        RANK() OVER(PARTITION BY date ORDER BY avg_volume DESC) as rank_high,
        RANK() OVER(PARTITION BY date ORDER BY avg_volume ASC) as rank_low
    FROM daily_volume
),
top_coin AS (
    SELECT date, coin_name as top_coin, avg_volume as top_volume
    FROM ranked WHERE rank_high = 1
),
bottom_coin AS (
    SELECT date, coin_name as bottom_coin, avg_volume as bottom_volume
    FROM ranked WHERE rank_low = 1
)
SELECT
    t.date,
    t.top_coin,
    t.top_volume,
    b.bottom_coin,
    b.bottom_volume,
    t.top_volume - b.bottom_volume as volume_gap
FROM top_coin t
JOIN bottom_coin b ON t.date = b.date
