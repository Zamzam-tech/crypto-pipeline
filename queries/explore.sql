--SELECT DISTINCT coin_id FROM marts_coin

--SELECT COUNT(*) FROM crypto_data

--SELECT * FROM marts_coin 
--LIMIT 5

 --WITH first_cte AS(
    --SELECT coin_id, current_price, DATE(ingested_at) AS ingested_date
    --FROM stg_coins
  --  WHERE coin_id = 'bitcoin'
--    ORDER BY ingested_at ASC
--)

--SELECT coin_id, MAX(current_price) AS max_current_price,MIN(current_price) AS min_current_price, MIN(ingested_date) AS first_ingested_date, MAX(ingested_date) AS latest_ingested_date, (MAX(current_price) - MIN(current_price)) AS price_difference
--FROM first_cte
--GROUP BY coin_id

--SELECT DISTINCT coin_id FROM stg_coins
--SELECT coin_id, ingested_at, current_price
--FROM stg_coins
--WHERE coin_id = 'bitcoin'
--ORDER BY ingested_at DESC
--LIMIT 1

--SELECT COUNT(*) FROM stg_coins

--Top five coins by market_cap
SELECT coin_name, market_cap,
     ROW_NUMBER() OVER(PARTITION BY coin_name ORDER BY market_cap DESC) AS rank
FROM crypto_data
WHERE rank <= 5