-- QA: Duplicate transaction_id (purchase events should be idempotent)
-- Returns any transaction_id that appears more than once (should be empty)

SELECT
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') AS transaction_id,
  COUNT(*) AS event_count
FROM `your_project.analytics_XXXXX.events_*`
WHERE event_name = 'purchase'
GROUP BY 1
HAVING COUNT(*) > 1
ORDER BY event_count DESC;
