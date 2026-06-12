WITH source AS(
    SELECT * FROM {{ source('crypto_data','crypto_data') }}
),
renamed AS (
    SELECT 
        id as coin_id, 
        symbol, 
        name as coin_name, 
        current_price, 
        market_cap, 
        total_volume, 
        last_updated::timestamp as last_updated,
        CASE 
            WHEN ingested_at LIKE '2026%' OR ingested_at LIKE '2025%'
            THEN ingested_at::timestamp
            ELSE to_timestamp(CAST(ingested_at AS BIGINT) / 1000)
        END as ingested_at
    FROM source
)

SELECT * FROM renamed