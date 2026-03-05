"""
Run the view → cart → purchase funnel on the Kaggle eCommerce CSV data.

Reads all *.csv from data/kaggle_data/, aggregates by day, and prints
(and optionally saves) the funnel: viewed, added_to_cart, purchased + conversion rates.

Usage (from project root):
  python scripts/run_funnel.py
  python scripts/run_funnel.py --out data/funnel_results.csv
"""

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "kaggle_data"


def parse_event_time(s: str) -> datetime | None:
    if not s:
        return None
    s = str(s).strip()
    if s.endswith(" UTC"):
        s = s.replace(" UTC", "")
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def load_events(csv_dir: Path):
    """Yield (event_date, user_id, user_session, event_type) from all CSVs."""
    csv_dir = csv_dir.resolve()
    if not csv_dir.is_dir():
        raise FileNotFoundError(f"Data directory not found: {csv_dir}")
    files = sorted(csv_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No *.csv files in {csv_dir}")
    for path in files:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = parse_event_time(row.get("event_time"))
                if not ts:
                    continue
                event_type = (row.get("event_type") or "").strip().lower()
                if event_type not in ("view", "cart", "purchase"):
                    continue
                user_id = (row.get("user_id") or "").strip()
                session = (row.get("user_session") or "").strip()
                if not user_id or not session:
                    continue
                yield ts.date(), user_id, session, event_type


def run_funnel(csv_dir: Path):
    """
    Build per-session flags then aggregate by date.
    Returns list of dicts: event_date, viewed, added_to_cart, purchased, view_to_cart_pct, cart_to_purchase_pct, view_to_purchase_pct.
    """
    # (date, user_id, session) -> set of event_types
    session_events: dict[tuple, set[str]] = defaultdict(set)
    for event_date, user_id, session, event_type in load_events(csv_dir):
        key = (event_date, user_id, session)
        session_events[key].add(event_type)

    # By date: count distinct sessions that had each step
    daily = defaultdict(lambda: {"viewed": set(), "cart": set(), "purchase": set()})
    for (event_date, user_id, session), types in session_events.items():
        session_key = (user_id, session)
        if "view" in types:
            daily[event_date]["viewed"].add(session_key)
        if "cart" in types:
            daily[event_date]["cart"].add(session_key)
        if "purchase" in types:
            daily[event_date]["purchase"].add(session_key)

    rows = []
    for event_date in sorted(daily.keys()):
        d = daily[event_date]
        viewed = len(d["viewed"])
        added_to_cart = len(d["cart"])
        purchased = len(d["purchase"])
        view_to_cart = round(100.0 * added_to_cart / viewed, 2) if viewed else None
        cart_to_purchase = round(100.0 * purchased / added_to_cart, 2) if added_to_cart else None
        view_to_purchase = round(100.0 * purchased / viewed, 2) if viewed else None
        rows.append({
            "event_date": str(event_date),
            "viewed": viewed,
            "added_to_cart": added_to_cart,
            "purchased": purchased,
            "view_to_cart_pct": view_to_cart,
            "cart_to_purchase_pct": cart_to_purchase,
            "view_to_purchase_pct": view_to_purchase,
        })
    return rows


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Run funnel (view → cart → purchase) on data/kaggle_data/*.csv")
    ap.add_argument("--data-dir", default=DATA_DIR, type=Path, help="Directory containing CSV files")
    ap.add_argument("--out", "-o", default=None, help="Optional: save results to this CSV path")
    args = ap.parse_args()
    data_dir = args.data_dir if args.data_dir.is_absolute() else (PROJECT_ROOT / args.data_dir)
    out_path = Path(args.out) if args.out else None
    if out_path and not out_path.is_absolute():
        out_path = PROJECT_ROOT / out_path

    print("Loading events from", data_dir, "...")
    rows = run_funnel(data_dir)
    if not rows:
        print("No event data found. Check that data/kaggle_data/ contains CSV files with event_time, event_type, user_id, user_session.")
        return 1

    # Print table
    print()
    print("Funnel by date (view → cart → purchase)")
    print("-" * 90)
    print(f"{'Date':<12} {'Viewed':>8} {'Add to cart':>12} {'Purchased':>10} {'View→Cart %':>12} {'Cart→Buy %':>12} {'View→Buy %':>10}")
    print("-" * 90)
    for r in rows:
        v2c = f"{r['view_to_cart_pct']}%" if r["view_to_cart_pct"] is not None else "—"
        c2p = f"{r['cart_to_purchase_pct']}%" if r["cart_to_purchase_pct"] is not None else "—"
        v2p = f"{r['view_to_purchase_pct']}%" if r["view_to_purchase_pct"] is not None else "—"
        print(f"{r['event_date']:<12} {r['viewed']:>8} {r['added_to_cart']:>12} {r['purchased']:>10} {v2c:>12} {c2p:>12} {v2p:>10}")
    print("-" * 90)
    total_viewed = sum(r["viewed"] for r in rows)
    total_cart = sum(r["added_to_cart"] for r in rows)
    total_purchased = sum(r["purchased"] for r in rows)
    print(f"{'TOTAL':<12} {total_viewed:>8} {total_cart:>12} {total_purchased:>10}")
    print()

    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["event_date", "viewed", "added_to_cart", "purchased", "view_to_cart_pct", "cart_to_purchase_pct", "view_to_purchase_pct"])
            w.writeheader()
            w.writerows(rows)
        print("Results saved to", out_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
