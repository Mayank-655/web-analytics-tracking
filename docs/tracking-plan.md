# Tracking Plan — E-commerce (GA4-style)

## Scope

Define a minimal set of events and parameters to support:

- **Funnel analysis**: Landing → Browse → Add to cart → Checkout → Purchase
- **A/B tests**: Compare conversion by variant (e.g. CTA, layout)
- **Product and category performance**: What drives add_to_cart and purchase

---

## Key events

| Event name | When to fire | Business use |
|------------|--------------|--------------|
| `page_view` | Every page load (or SPA route change) | Traffic, landing pages, session depth |
| `view_item` | Product detail page viewed | Interest, product/category performance |
| `view_item_list` | Category or search results viewed | Discovery, list performance |
| `add_to_cart` | Item added to cart | Cart add rate, product/category contribution |
| `remove_from_cart` | Item removed from cart | Cart abandonment, product issues |
| `begin_checkout` | Checkout started (e.g. cart → checkout) | Checkout start rate |
| `add_shipping_info` | Shipping step completed | Funnel step, shipping impact |
| `add_payment_info` | Payment step completed | Funnel step, payment friction |
| `purchase` | Order completed (thank-you / confirmation) | Revenue, conversion, attribution |

---

## Event → Business questions mapping

| Business question | Primary events | Key parameters |
|-------------------|----------------|-----------------|
| Where do users land? | `page_view` (first in session) | `page_location`, `page_referrer` |
| Which products get the most views? | `view_item` | `item_id`, `item_name`, `item_category` |
| Add-to-cart rate by category? | `view_item`, `add_to_cart` | `item_category`, `item_id` |
| Cart → Checkout → Purchase funnel? | `add_to_cart`, `begin_checkout`, `purchase` | (all) |
| Revenue and AOV? | `purchase` | `value`, `currency`, `items` |
| Checkout drop-off by step? | `begin_checkout`, `add_shipping_info`, `add_payment_info`, `purchase` | `checkout_step` (optional) |
| A/B test: variant conversion? | All conversion events | `experiment_id`, `variant_id` (custom) |

---

## Required parameters (by event)

### All events (context)

- **`timestamp`** (or rely on GA4 collection time): When the event occurred.
- **User/session**: Handled by GA4 (client_id, session_id); for custom pipelines, include a stable `user_id` and `session_id` where available.

### page_view

- `page_location` (URL)
- `page_referrer` (optional but recommended)
- `page_title` (optional)

### view_item

- `item_id`, `item_name`, `item_category` (or `item_category2`, …)
- `price`, `quantity` (optional but recommended)

### view_item_list

- `item_list_id` (e.g. "search_results", "category_123")
- Optional: list of `items` (item_id, name, category, position)

### add_to_cart / remove_from_cart

- `currency`
- `value` (total value of added/removed items)
- `items`: array of `{ item_id, item_name, item_category, price, quantity }`

### begin_checkout / add_shipping_info / add_payment_info

- `currency`
- `value` (cart value at that step)
- `items` (cart contents)
- Optional: `checkout_step` (1, 2, 3) for step analysis

### purchase

- `transaction_id` (unique per order; idempotency)
- `value` (order total)
- `currency`
- `tax`, `shipping` (optional)
- `items`: array of `{ item_id, item_name, item_category, price, quantity }`

---

## A/B and experimentation

For experiments, add custom parameters (or GA4 custom dimensions) to conversion events:

- `experiment_id`: e.g. "homepage_cta_2024_01"
- `variant_id`: e.g. "control", "variant_a"

Same names across events so funnel and conversion can be broken down by variant.

---

## Out of scope (for this plan)

- Out-of-the-box form interactions (focus is e-commerce funnel)
- Offline/CRM imports (can be added later with same event names)
- Custom search events (can reuse `view_item_list` with `item_list_id = "search"` and a search-term parameter if needed)
