WITH source AS(
    SELECT * FROM {{source('crypto_data','crypto_data')}}
),
renamed AS (
SELECT id as coin_id, 
         symbol, 
         name as coin_name, 
         current_price, 
         market_cap, 
         total_volume, 
         last_updated::timestamp as last_updated,
         ingested_at::timestamp as ingested_at
FROM source
)

SELECT * FROM renamed