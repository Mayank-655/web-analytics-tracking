# Event Taxonomy

## Naming convention

- **Snake_case** for event and parameter names (GA4-style).
- **Consistent names** across client, GA4, and any export/BigQuery so reports and SQL stay aligned.

## Event hierarchy

```
Session
├── page_view (1+ per session)
├── view_item (0+)
├── view_item_list (0+)
├── add_to_cart (0+)
├── remove_from_cart (0+)
├── begin_checkout (0 or 1 per funnel)
│   ├── add_shipping_info (0 or 1)
│   └── add_payment_info (0 or 1)
└── purchase (0 or 1 per order; 1+ per session if multiple orders)
```

## Required parameters (summary)

| Event | Required | Recommended optional |
|-------|----------|------------------------|
| `page_view` | `page_location` | `page_referrer`, `page_title` |
| `view_item` | `item_id`, `item_name` | `item_category`, `price`, `quantity` |
| `view_item_list` | `item_list_id` | `items` (list) |
| `add_to_cart` | `currency`, `value`, `items` | — |
| `remove_from_cart` | `currency`, `value`, `items` | — |
| `begin_checkout` | `currency`, `value`, `items` | `checkout_step` |
| `add_shipping_info` | `currency`, `value`, `items` | `checkout_step` |
| `add_payment_info` | `currency`, `value`, `items` | `checkout_step` |
| `purchase` | `transaction_id`, `value`, `currency`, `items` | `tax`, `shipping` |

## Item object (for cart/checkout/purchase)

Each `items` element should include:

- `item_id` (string)
- `item_name` (string)
- `item_category` (string; category or category1)
- `price` (number)
- `quantity` (integer)

Optional: `item_category2`, `item_brand`, `index` (position in list).

## User and session context

- **GA4**: Provides `user_pseudo_id` (client_id), `session_id`; first-party `user_id` if set.
- **Custom pipelines**: Send a stable `user_id` (logged-in) and `session_id` so funnel and attribution are consistent.
- **Privacy**: Avoid sending PII in event/parameter names or values; use hashing or server-side linking if needed.

## Custom dimensions (for A/B and segmentation)

Suggested GA4 custom dimensions (or equivalent in export):

- `experiment_id` (event-scoped)
- `variant_id` (event-scoped)
- `user_type` (user-scoped): e.g. "new", "returning", "guest"

These can be set on key events and used in funnel and A/B analyses.
