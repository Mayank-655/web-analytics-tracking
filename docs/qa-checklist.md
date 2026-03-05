# QA Checklist — Event Data Quality

Use this checklist to ensure event data is accurate and reliable for **funnel** and **A/B** analyses.

---

## 1. Event volume and presence

| Check | How | Pass criteria |
|-------|-----|----------------|
| **Page views exist** | Count `page_view` per day/source | Non-zero daily volume; trend matches expected traffic. |
| **No duplicate purchase** | Count `purchase` by `transaction_id` | One row per `transaction_id` (idempotent). |
| **Cart events present** | Count `add_to_cart`, `begin_checkout`, `purchase` | All three present; add_to_cart ≥ begin_checkout ≥ purchase. |
| **Key params non-null** | For each event, check required params | `page_location`, `item_id`/`item_name`, `value`, `transaction_id` (purchase) not null where applicable. |

---

## 2. Funnel consistency

| Check | How | Pass criteria |
|-------|-----|----------------|
| **Funnel order** | Per session: order of first occurrence of add_to_cart, begin_checkout, purchase | add_to_cart time ≤ begin_checkout time ≤ purchase time. |
| **Checkout ≤ Cart** | Sessions with `begin_checkout` | Sessions with begin_checkout have ≥1 add_to_cart (same session). |
| **Purchase ≤ Checkout** | Sessions with `purchase` | Sessions with purchase have begin_checkout (and add_to_cart) in that session. |
| **Value consistency** | purchase.value vs sum of items | purchase.value ≈ sum(item.price * item.quantity) for that event (within rounding). |

---

## 3. Completeness and schema

| Check | How | Pass criteria |
|-------|-----|----------------|
| **Items array** | add_to_cart, begin_checkout, purchase have `items` | `items` array present and non-empty when value > 0. |
| **Currency** | All monetary events | `currency` set (e.g. "USD"); same currency for value and items. |
| **Event names** | List distinct event names in raw data | Matches taxonomy (no typos, no legacy names unless documented). |

---

## 4. A/B and experimentation

| Check | How | Pass criteria |
|-------|-----|----------------|
| **Variant present** | Conversion events (e.g. purchase) | `experiment_id` and `variant_id` populated when user was in experiment. |
| **Balance** | Users per variant | Variant split roughly as designed (e.g. 50/50); no one variant missing. |
| **Same user, one variant** | Per user in experiment | Each user has a single variant_id for that experiment_id. |

---

## 5. Quick daily checks (summary)

1. **Volume**: page_view and purchase counts in expected range.
2. **Funnel**: add_to_cart ≥ begin_checkout ≥ purchase (counts).
3. **Duplicates**: No duplicate transaction_id for purchase.
4. **Nulls**: Required parameters for key events are not null.

Run these after deployment or GTM changes and before relying on data for funnel or A/B reports.
