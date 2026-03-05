# Using a public dataset (current phase)

This project first uses a **public clickstream / e-commerce dataset** so you can apply the tracking plan, event taxonomy, and QA checklist without setting up GA4. Later you’ll add GA4 (see [GA4 next steps](ga4-next-steps.md)).

---

## Recommended dataset

**eCommerce Events History in Cosmetics Shop** (Kaggle)

- **Link**: [Kaggle — eCommerce Events History in Cosmetics Shop](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop) (or search “ecommerce events cosmetics”).
- **Format**: CSV per month (e.g. `2019-Oct.csv`, `2019-Nov.csv`, …, `2020-Feb.csv`).
- **Columns**: `event_time`, `event_type`, `product_id`, `category_id`, `category_code`, `brand`, `price`, `user_id`, `user_session`.

---

## Schema mapping → our event taxonomy

Map the dataset’s columns to the events and parameters in the [tracking plan](tracking-plan.md):

| Dataset `event_type` | Our event name    | Notes |
|----------------------|-------------------|--------|
| `view`               | `view_item`       | Product/catalog view; use `user_session` as session context. |
| `cart`               | `add_to_cart`     | Item added to cart. |
| `remove_from_cart`   | `remove_from_cart`| Item removed. |
| `purchase`           | `purchase`        | Order; treat `user_session` as `transaction_id` for idempotency. |

There is no explicit `page_view` or `begin_checkout` in this dataset; you can still compute funnel as **view → cart → purchase** and run QA (volume, funnel order, duplicate transactions).

**Parameter mapping:**

| Our parameter   | Dataset column / derivation |
|-----------------|-----------------------------|
| `item_id`       | `product_id` |
| `item_name`     | (optional) from `category_code` or leave blank |
| `item_category` | `category_code` or `category_id` |
| `price`, `quantity` | `price`; quantity = 1 per row (aggregate in SQL by session). |
| `transaction_id` (purchase) | `user_session` |
| `value` (purchase) | Sum of `price` for that `user_session` in purchase rows. |

---

## Where to put the data

1. Use the folder: **`data/kaggle_data/`** (already created in this project).
2. **Option A — copy from cohort segmentation:**  
   Copy the same Kaggle CSVs from your cohort segmentation project:  
   `Data Science Projects/cohort segmentation/data/kaggle_data/*.csv`  
   → into  
   `Data Science Projects/web-analytics-tracking/data/kaggle_data/`
3. **Option B:** Download from [Kaggle](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop) and place the monthly CSVs (e.g. `2019-Oct.csv`, `2019-Nov.csv`, …) in `data/kaggle_data/`.
4. Dataset CSVs are in `.gitignore`, so they won’t be pushed to GitHub.

---

## How to run the funnel (public dataset)

From the project root (e.g. `Data Science Projects\web-analytics-tracking`):

```bash
python scripts/run_funnel.py
```

Or double-click **`run_funnel.bat`** (Windows).

This reads all CSVs in `data/kaggle_data/`, computes the **view → cart → purchase** funnel by day, and prints a table (viewed, added_to_cart, purchased, conversion %). To save results to CSV: `python scripts/run_funnel.py --out data/funnel_results.csv`.

**Other options:**

- **SQL**: Use `sql/04_public_dataset_funnel.sql` with DuckDB or BigQuery after loading the CSVs into a table named `events`.
- **QA checklist**: Run the checks in [qa-checklist.md](qa-checklist.md) on the same data (event volumes, funnel order, no duplicate transactions).

---

## Funnel on public data

For this dataset, the funnel is:

- **Sessions with view_item** (event_type = view)  
  → **Sessions with add_to_cart** (event_type = cart)  
  → **Sessions with purchase** (event_type = purchase)

Use the same logic as in `sql/01_funnel_summary.sql`: count distinct sessions per event type by day, then compute step-through rates. Apply the QA checklist to ensure data quality before reporting.

---

Once this works end-to-end, move on to [GA4 next steps](ga4-next-steps.md) to implement the same taxonomy in GA4 and BigQuery.
