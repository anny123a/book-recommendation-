# import os
# import requests
# from fastapi import HTTPException
# from dotenv import load_dotenv


# load_dotenv()
# KEEPA_API_KEY = os.getenv("KEEPA_API_KEY")
# PRODUCT_URL = "https://api.keepa.com/product"


# def isbn13_to_isbn10(isbn13: str) -> str:
#     """Convert ISBN-13 to ISBN-10 if needed"""
#     if not isbn13.startswith("978"):
#         return isbn13
#     digits = isbn13[3:-1]
#     s = sum((10 - i) * int(x) for i, x in enumerate(digits))
#     check = 11 - (s % 11)
#     check_digit = "X" if check == 10 else str(check % 11)
#     return digits + check_digit



# def fetch_keepa_data(isbn: str):
#     """
#     Fetch product + stats from Keepa API.
#     """
#     if not KEEPA_API_KEY:
#         raise HTTPException(status_code=500, detail="Keepa API Key missing")
#     asin = isbn13_to_isbn10(isbn) if len(isbn) == 13 else isbn
#     params = {"key": KEEPA_API_KEY, "domain": 1, "asin": asin, "history": 1}
#     r = requests.get(PRODUCT_URL, params=params)
#     if r.status_code != 200:
#         raise HTTPException(status_code=500, detail=f"Keepa error: {r.text}")
#     data = r.json()
#     if not data.get("products"):
#         raise HTTPException(status_code=404, detail="No Keepa product found")

#     product = data["products"][0]
    
#     return product


# # File: app/services/keepa_services.py (Fetch Keepa data)
# import os
# import requests
# from fastapi import HTTPException
# from dotenv import load_dotenv

# load_dotenv()
# # Hardcode API key for this setup (use env in production)
# KEEPA_API_KEY = "bn9mv753eq9ftvbfbojkppjfpgaep2eeqqrhplks0smefut0eec4eg9162nboqnv"
# PRODUCT_URL = "https://api.keepa.com/product"

# def isbn13_to_isbn10(isbn13: str) -> str:
#     """
#     Convert ISBN-13 to ISBN-10 if needed (for Keepa query as ASIN).
#     """
#     if len(isbn13) != 13 or not isbn13.startswith("978"):
#         return isbn13
#     digits = isbn13[3:-1]
#     s = sum((10 - i) * int(x) for i, x in enumerate(digits))
#     check = 11 - (s % 11)
#     check_digit = "X" if check == 10 else str(check)
#     return digits + check_digit

# def fetch_keepa_data(isbn: str):
#     """
#     Fetch product history and stats from Keepa API.
#     Uses ISBN converted to ISBN-10 if needed.
#     Includes history, stats, buybox for full data.
#     """
#     if not KEEPA_API_KEY:
#         raise HTTPException(status_code=500, detail="Keepa API Key missing")
#     asin = isbn13_to_isbn10(isbn) if len(isbn) == 13 else isbn
#     params = {
#         "key": KEEPA_API_KEY, 
#         "domain": 1,  # US
#         "asin": asin, 
#         "history": 1,  # Price/Sales history
#         "stats": 1,    # Stats like offers
#         "buybox": 1    # Buy box details
#     }
#     r = requests.get(PRODUCT_URL, params=params)
#     if r.status_code != 200:
#         raise HTTPException(status_code=500, detail=f"Keepa error: {r.text}")
#     data = r.json()
#     if not data.get("products"):
#         raise HTTPException(status_code=404, detail="No Keepa product found for ISBN")
    
#     product = data["products"][0]
#     return product

# excel file

# File: app/services/keepa_services.py
import os
import requests
import pandas as pd
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# Hardcode API key for this setup (use env in production)
KEEPA_API_KEY = os.getenv("KEEPA_API_KEY")
# KEEPA_API_KEY = "bn9mv753eq9ftvbfbojkppjfpgaep2eeqqrhplks0smefut0eec4eg9162nboqnv"
PRODUCT_URL = "https://api.keepa.com/product"


def isbn13_to_isbn10(isbn13: str) -> str:
    """
    Convert ISBN-13 to ISBN-10 if needed (for Keepa query as ASIN).
    """
    if len(isbn13) != 13 or not isbn13.startswith("978"):
        return isbn13
    digits = isbn13[3:-1]
    s = sum((10 - i) * int(x) for i, x in enumerate(digits))
    check = 11 - (s % 11)
    check_digit = "X" if check == 10 else str(check)
    return digits + check_digit


def fetch_keepa_data(isbn: str):
    """
    Fetch product history and stats from Keepa API.
    Uses ISBN converted to ISBN-10 if needed.
    Includes history, stats, buybox for full data.
    """
    if not KEEPA_API_KEY:
        raise HTTPException(status_code=500, detail="Keepa API Key missing")
    asin = isbn13_to_isbn10(isbn) if len(isbn) == 13 else isbn
    # params = {
    #     "key": KEEPA_API_KEY,
    #     "domain": 1,  # US
    #     "asin": asin,
    #     "history": 1,  # Price/Sales history
    #     "stats": 1,    # Stats like offers
    #     "buybox": 1    # Buy box details
    # }
    params = {
        "key": KEEPA_API_KEY,
        "domain": 1,
        "asin": asin,
        "history": 1,
        "stats": 1,
        "buybox": 1,
        #"offers": 1,
        #"update": 1, 
    }
    r = requests.get(PRODUCT_URL, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Keepa error: {r.text}")
    data = r.json()
    #print('Data - ',data)
    if not data.get("products"):
        raise HTTPException(status_code=404, detail="No Keepa product found for ISBN")
    
    product = data["products"][0]
    #print('Product - ',product)
    return product



print("H"*44)



# data=fetch_keepa_data("9788861827288")
# print(data)



 






























































# import os
# import requests
# import pandas as pd
# from fastapi import HTTPException
# from dotenv import load_dotenv

# load_dotenv()

# # Hardcoded API key (⚠️ Only for testing — store in .env for production)
# KEEPA_API_KEY = "bn9mv753eq9ftvbfbojkppjfpgaep2eeqqrhplks0smefut0eec4eg9162nboqnv"
# PRODUCT_URL = "https://api.keepa.com/product"


# def isbn13_to_isbn10(isbn13: str) -> str:
#     """Convert ISBN-13 to ISBN-10 if needed (for Keepa query as ASIN)."""
#     if len(isbn13) != 13 or not isbn13.startswith("978"):
#         return isbn13
#     digits = isbn13[3:-1]
#     s = sum((10 - i) * int(x) for i, x in enumerate(digits))
#     check = 11 - (s % 11)
#     check_digit = "X" if check == 10 else str(check)
#     isbn10 = digits + check_digit
#     print(f"[ISBN Conversion] {isbn13} → {isbn10}")
#     return isbn10


# def fetch_keepa_data(isbn: str):
#     """
#     Fetch product history and stats from Keepa API.
#     """
#     print(f"\n=== Fetching Keepa Data for ISBN/ASIN: {isbn} ===")

#     if not KEEPA_API_KEY:
#         raise HTTPException(status_code=500, detail="Keepa API Key missing")

#     # Convert ISBN-13 to ISBN-10 if applicable
#     asin = isbn13_to_isbn10(isbn) if len(isbn) == 13 else isbn
#     print(f"[ASIN Used for Keepa] {asin}")

#     params = {
#         "key": KEEPA_API_KEY,
#         "domain": 1,   # Amazon.com (US)
#         "asin": asin,
#         "history": 1,
#         "stats": 1,
#         "buybox": 1,
#     }

#     print("[Request Params]", params)

#     r = requests.get(PRODUCT_URL, params=params)
#     print(f"[HTTP Status] {r.status_code}")

#     if r.status_code != 200:
#         raise HTTPException(status_code=500, detail=f"Keepa error: {r.text}")

#     data = r.json()
#     print("DATA-----",data )
#     print("[Response Keys]", list(data.keys()))

#     if not data.get("products"):
#         raise HTTPException(status_code=404, detail="No Keepa product found for ISBN")

#     product = data["products"][0]

#     # Print key product info for debugging
#     print("\n[Product Info]")
#     print("Title:", product.get("title", "N/A"))
#     print("ASIN:", product.get("asin"))
#     print("Category:", product.get("category", "N/A"))
#     print("Has Stats:", "stats" in product)
#     print("Has CSV Data:", "csv" in product)

#     return product


# # Example test run (comment this out in production)
# if __name__ == "__main__":
#     print("=" * 50)
#     try:
#         test_isbn = "9780800636838"  # Example ISBN (Clean Code)
#         product_data = fetch_keepa_data(test_isbn)
#         print("\n✅ Fetch complete. Product title:", product_data.get("title", "Unknown"))
#     except Exception as e:
#         print("❌ Error:", e)
