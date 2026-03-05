-- Funnel summary for PUBLIC DATASET (e.g. Kaggle eCommerce Events)
-- Schema: event_time, event_type, user_id, user_session, product_id, category_id, price, ...
-- Event types: view, cart, remove_from_cart, purchase
--
-- Use with: DuckDB, BigQuery (after loading CSV), or any SQL engine.
-- Adjust table name and date column; here we assume a single table 'events'.

WITH daily_sessions AS (
  SELECT
    DATE(event_time) AS event_date,
    user_id,
    user_session,
    MAX(CASE WHEN event_type = 'view'    THEN 1 ELSE 0 END) AS had_view,
    MAX(CASE WHEN event_type = 'cart'    THEN 1 ELSE 0 END) AS had_cart,
    MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS had_purchase
  FROM events
  WHERE event_type IN ('view', 'cart', 'purchase')
  GROUP BY DATE(event_time), user_id, user_session
),
funnel AS (
  SELECT
    event_date,
    COUNT(DISTINCT CASE WHEN had_view    = 1 THEN user_session END) AS viewed,
    COUNT(DISTINCT CASE WHEN had_cart   = 1 THEN user_session END) AS added_to_cart,
    COUNT(DISTINCT CASE WHEN had_purchase = 1 THEN user_session END) AS purchased
  FROM daily_sessions
  GROUP BY event_date
)
SELECT
  event_date,
  viewed,
  added_to_cart,
  purchased,
  ROUND(100.0 * added_to_cart / NULLIF(viewed, 0), 2)     AS view_to_cart_pct,
  ROUND(100.0 * purchased       / NULLIF(added_to_cart, 0), 2) AS cart_to_purchase_pct,
  ROUND(100.0 * purchased       / NULLIF(viewed, 0), 2)    AS view_to_purchase_pct
FROM funnel
ORDER BY event_date;
