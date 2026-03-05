-- Funnel summary: counts by event (GA4-style event table)
-- Assumes table with: event_date, event_name, user_pseudo_id, session_id, and optional ecommerce params

WITH events AS (
  SELECT
    event_date,
    user_pseudo_id,
    session_id,
    event_name
  FROM `your_project.analytics_XXXXX.events_*`
  WHERE event_name IN ('add_to_cart', 'begin_checkout', 'purchase')
),
funnel AS (
  SELECT
    event_date,
    COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart'    THEN CONCAT(user_pseudo_id, '-', session_id) END) AS added_to_cart,
    COUNT(DISTINCT CASE WHEN event_name = 'begin_checkout' THEN CONCAT(user_pseudo_id, '-', session_id) END) AS began_checkout,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase'      THEN CONCAT(user_pseudo_id, '-', session_id) END) AS purchased
  FROM events
  GROUP BY event_date
)
SELECT
  event_date,
  added_to_cart,
  began_checkout,
  purchased,
  ROUND(100.0 * began_checkout / NULLIF(added_to_cart, 0), 2)   AS cart_to_checkout_pct,
  ROUND(100.0 * purchased       / NULLIF(began_checkout, 0), 2)   AS checkout_to_purchase_pct,
  ROUND(100.0 * purchased       / NULLIF(added_to_cart, 0), 2)  AS cart_to_purchase_pct
FROM funnel
ORDER BY event_date;
