# GA4 next steps (after public dataset)

Once you’ve run the tracking plan and QA on the **public dataset**, do the following to use **GA4** with the same event taxonomy and checks.

---

## 1. Set up GA4

- Create a **GA4 property** (or use an existing one / demo property).
- Optional: Create a **BigQuery project** and link it to GA4 for **daily export** of raw events (recommended for SQL and QA).

---

## 2. Implement the tracking plan

Use **Google Tag Manager (GTM)** or **gtag.js** on your site (personal site, demo, or test page).

- **Events to implement** (from [tracking-plan.md](tracking-plan.md)):
  - `page_view` (often automatic in GA4/GTM)
  - `view_item` (product detail)
  - `view_item_list` (category/search)
  - `add_to_cart`, `remove_from_cart`
  - `begin_checkout`, `add_shipping_info`, `add_payment_info`
  - `purchase` (with `transaction_id`, `value`, `currency`, `items`)

- **Parameters**: Follow [event-taxonomy.md](event-taxonomy.md) (required vs optional) so GA4 and BigQuery match the plan.
- **A/B (optional)**: Add `experiment_id` and `variant_id` to conversion events when running tests.

---

## 3. Validate in GA4

- Use **DebugView** (or GA4 Realtime) to confirm events and parameters.
- Check **Reports** (e.g. Engagement → Events) for expected volumes and parameter presence.
- Run the same logic as the public-dataset funnel (e.g. cart → checkout → purchase) in GA4 explorations or in BigQuery.

---

## 4. BigQuery export (if enabled)

- In GA4: **Admin → Product links → BigQuery linking**; set up daily export.
- Tables: `events_YYYYMMDD` (and optionally `events_*` for date-range queries).
- **Reuse project SQL**: Adapt `sql/01_funnel_summary.sql`, `02_revenue_and_events.sql`, and `03_qa_duplicate_transactions.sql` to the GA4 export schema (`event_params`, `ecommerce`, etc.). Replace the placeholder project/dataset with your GA4 export project/dataset.

---

## 5. Run the same QA checklist

Apply [qa-checklist.md](qa-checklist.md) to GA4/BigQuery data:

- Event volume and presence (page_view, add_to_cart, purchase, etc.).
- Funnel consistency (cart ≤ checkout ≤ purchase; correct ordering).
- No duplicate `transaction_id` for purchase (use `03_qa_duplicate_transactions.sql`).
- Required parameters non-null where applicable.
- If you use A/B, variant presence and balance.

---

## Summary

| Step | Action |
|------|--------|
| 1 | GA4 property (+ optional BigQuery link) |
| 2 | Implement events and parameters from tracking plan (GTM / gtag) |
| 3 | Validate in DebugView and GA4 reports |
| 4 | Query BigQuery export with project SQL; adapt to GA4 schema |
| 5 | Run QA checklist on GA4/BigQuery data |

This keeps the same event taxonomy and data-quality bar you used on the public dataset, now applied to GA4 and BigQuery.
