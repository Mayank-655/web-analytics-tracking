# SQL examples

## Public dataset (use first)

- **04_public_dataset_funnel.sql**: Funnel (view → cart → purchase) for Kaggle-style schema: table `events` with `event_time`, `event_type`, `user_id`, `user_session`. Use with DuckDB, BigQuery (after loading CSV), or any SQL engine. Adjust table/column names to match your export.

## GA4 / BigQuery export (use when you add GA4)

- **01_funnel_summary.sql**: Daily funnel (add_to_cart → begin_checkout → purchase) for GA4 BigQuery export.
- **02_revenue_and_events.sql**: Daily revenue and transaction count from `purchase` events (GA4 stores `value` in micros).
- **03_qa_duplicate_transactions.sql**: QA check — duplicate `transaction_id` (should be empty).

Replace `your_project.analytics_XXXXX.events_*` with your GA4 BigQuery project/dataset. Adjust parameter names if your schema uses different keys (e.g. `ecommerce.purchase_revenue`).
