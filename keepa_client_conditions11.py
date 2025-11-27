from datetime import datetime
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def minutes_to_datetime(keepa_minutes: int) -> datetime:
    return datetime.utcfromtimestamp((keepa_minutes + 21564000) * 60)


def get_price_history(keepa_product: dict, index: int) -> list:
    """
    Returns list of (time_minutes, price_cents) tuples from keepa product csv index.
    If missing/invalid returns [].
    """
    if 'csv' not in keepa_product or len(keepa_product['csv']) <= index:
        logger.debug("No csv data at index %s", index)
        return []

    price_list = keepa_product['csv'][index]
    if not price_list or len(price_list) < 2 or len(price_list) % 2 != 0:
        logger.debug("Invalid price list at index %s (len=%s)", index, len(price_list) if price_list else None)
        return []

    # convert to list of tuples (time_minutes, price_cents)
    try:
        return [(price_list[i], price_list[i + 1]) for i in range(0, len(price_list), 2)]
    except Exception:
        logger.exception("Failed to parse price_list at index %s", index)
        return []


def monthly_price_avg(price_history: list) -> dict:
    """
    Accepts keepa-style [(minutes, price_cents), ...]
    Returns dict month->avg_price_dollars (rounded to 2 decimals) for months >= 2024-01-01.
    """
    if not price_history:
        return {}

    df = pd.DataFrame(price_history, columns=["time", "price"])
    # convert minutes -> datetime
    df["datetime"] = df["time"].apply(minutes_to_datetime)

    # filter to >= 2024-01-01 (mirrors your original code)
    df = df[df["datetime"] >= datetime(2024, 1, 1)]

    if df.empty:
        return {}

    df["price"] = df["price"] / 100.0  # cents -> dollars
    df = df[df["price"] >= 0]  # ignore negative placeholders
    df["month"] = df["datetime"].dt.to_period("M").astype(str)

    return df.groupby("month")["price"].mean().round(2).to_dict()


def get_latest_price(price_history: list) -> float:
    """
    Return the latest (most recent) non-negative price in dollars, rounded to 2 decimals.
    If none available, return None.
    """
    if not price_history:
        return None

    df = pd.DataFrame(price_history, columns=["time", "price"])
    # drop negative placeholders
    df = df[df["price"] >= 0]
    if df.empty:
        return None

    df["price"] = df["price"] / 100.0
    latest = df.iloc[-1]["price"]
    return round(latest, 2)


# ----------------- MAIN ANALYSIS -----------------
def analyze_prices(keepa_product: dict, breakeven_price: float,first_time_purchase: bool = False) -> dict:
    """
    Returns a JSON-friendly dict containing:
      - history counts + samples (including sales)
      - latest prices
      - monthly averages (including monthly_used_avg top-level)
      - drops, offers metadata, and is_safe flag
    """

    indices = {
        "buy_box": 18,
        "amazon": 0,
        "used": 2,
        "sales": 3,
        "list_price": 12
    }

    # fetch raw histories
    histories = {key: get_price_history(keepa_product, idx) for key, idx in indices.items()}

    # stats convenience
    stats = keepa_product.get("stats", {})

    # latest prices (improved to ignore negative placeholders)
    latest_buy_box = stats.get("buyBoxPrice", 0)
    latest_buy_box = stats.get("buyBoxPrice")

    if latest_buy_box not in (None, -1):
        latest_buy_box = round(latest_buy_box / 100, 2)
    else:
        latest_buy_box = None

    #print("latest_buy_box", latest_buy_box)
     

     

    
    # latest_buy_box2 = get_latest_price(histories["buy_box"])
    # print("latest_buy_box2",latest_buy_box2)
    latest_used = get_latest_price(histories["used"])
    latest_list_price = get_latest_price(histories["list_price"])
    latest_amazon = get_latest_price(histories["amazon"])
    # latest amazon price
    

    


    # monthly averages
    buy_box_monthly = monthly_price_avg(histories["buy_box"])
    used_monthly = monthly_price_avg(histories["used"])
    list_price_monthly = monthly_price_avg(histories["list_price"])
    amazon_monthly = monthly_price_avg(histories["amazon"])
    sales_monthly = monthly_price_avg(histories["sales"])
    #print("sales_monthly",sales_monthly)

    # drops
    drops_30 = stats.get("salesRankDrops30", 0)
    drops_90 = stats.get("salesRankDrops90", 0)
    drops_180 = stats.get("salesRankDrops180", 0)

    # sales rank
    sales_rank = keepa_product.get("salesRanks", {}).get("BOOKS", "N/A")

    # publisher fallback
    publisher = (
        keepa_product.get("manufacturer") or
        keepa_product.get("brand") or
        keepa_product.get("label") or
        "Unknown"
    )

    # offers
    offers = keepa_product.get("offers", [])
    offer_count_new = stats.get("offerCountNew", stats.get("offerCountFBA", 0))
    offer_count_used = stats.get("offerCountUsed", stats.get("offerCountFBM", 0))
    amazon_stock = stats.get("stockAmazon", None)
    third_party_prices = [o.get("price", 0) / 100 for o in offers if not o.get("isPrime")]

    category_tree = keepa_product.get("categoryTree", [])
    product_group = keepa_product.get("productGroup", "Unknown")

    # safety flag
    is_safe = (latest_buy_box and latest_buy_box >= breakeven_price * 1.10)
    



    # JSON-friendly samples: keep first 5 entries as lists [time, price]
    history_samples = {k: [list(x) for x in (v[:5] if v else [])] for k, v in histories.items()}

    # Build final result
    result = {
        "asin": keepa_product.get("asin"),
        "title": keepa_product.get("title"),
        "breakeven_price": breakeven_price,

        # counts for each history (includes sales)
        "history_counts": {k: len(v) for k, v in histories.items()},

        # samples for quick inspection (JSON-friendly)
        "history_samples": history_samples,

        # publisher / category / rank
        "publisher": publisher,
        "product_group": product_group,
        "category_tree": category_tree,
        #"sales_rank": sales_rank,

        # offers and meta
        "offer_count_new": offer_count_new,
        "offer_count_used": offer_count_used,
        #"amazon_stock": amazon_stock,
        #"third_party_prices": third_party_prices,
        #"offers": offers,

        # latest prices
        "latest_prices": {
            "buy_box": latest_buy_box,
            "used": latest_used,
            "list_price": latest_list_price,
            "amazon": latest_amazon
        },

        # monthly averages (kept grouped) + explicit monthly_used_avg at top-level
        "monthly_prices": {
            "buy_box": buy_box_monthly,
            "used": used_monthly,
            "amazon": amazon_monthly,
            "list_price": list_price_monthly,
            "sales": sales_monthly
        },
        # "monthly_used_avg": used_monthly,   # explicit field you asked for

        # drops
        "drops": {
            "30d": drops_30,
            "90d": drops_90,
            "180d": drops_180
        },

        # safety flag
        "is_safe": is_safe,
        "first_time_purchase": first_time_purchase
    }

    return result

















# from keepa_services import fetch_keepa_data

# import json
# isbn = "9788861827240"  # Example ISBN
# breakeven = 49.90  # Example breakeven price
# keepa_product = fetch_keepa_data(isbn)
# first_time_purchase= True
# result = analyze_prices(keepa_product, breakeven,first_time_purchase)

# print(result)