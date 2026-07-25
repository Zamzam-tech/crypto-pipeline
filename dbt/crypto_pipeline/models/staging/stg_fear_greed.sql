WITH source AS(
    SELECT * FROM {{ source('crypto_data','fear_greed') }}
),
renamed AS (
    SELECT
        score as fear_greed_score,
        classification as sentiment,
        fetch_date,
        fetched_at
    FROM source
)
SELECT * FROM renamed
