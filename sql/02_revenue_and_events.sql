-- Revenue and key metrics by day (GA4 BigQuery export schema)
-- Uses events + event_params / ecommerce for value and transaction_id

WITH purchase_events AS (
  SELECT
    event_date,
    (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'value') AS value,
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') AS transaction_id
  FROM `your_project.analytics_XXXXX.events_*`
  WHERE event_name = 'purchase'
),
daily AS (
  SELECT
    event_date,
    COUNT(DISTINCT transaction_id) AS transactions,
    SUM(value / 1e6) AS revenue  -- GA4 stores value in micros
  FROM purchase_events
  WHERE transaction_id IS NOT NULL
  GROUP BY event_date
)
SELECT * FROM daily ORDER BY event_date;
