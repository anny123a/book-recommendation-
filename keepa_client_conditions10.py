 









from dotenv import load_dotenv
import os
from openai import OpenAI

 
load_dotenv() 

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=openai_api_key)

 
 
 
SYSTEM_PROMPT = """
You are an expert Amazon FBA book reseller. Follow ALL rules below exactly.

CORE RULES (never add new ones):
1. Price frequently near/at breakeven → max 5-10 or Avoid
2. Amazon price ≤10% above breakeven → Avoid
3. 3P sellers drop below breakeven (Amazon high) → Avoid unless very short
4. Amazon keeps price < breakeven 6+ months (e.g. Crossway) → Avoid
5. Frequent 3P breakeven breaks (e.g. Crown Publishing Group) → max 5-10 unless SKU stays high
6. Temporary drop by 1-2 low-stock sellers → Buy normally if ≥10 drops/month
7. Used price <80% of buybox → Avoid
8. Drops only in peak seasons (Jan-Feb, Jul-Aug) & price stable otherwise → Buy for peak only
9. Alma Edizioni OR titles where Amazon almost never sells + price stable high → Buy freely, price high
10. Books of Discovery OR titles that almost never drop below list + strong demand → Buy freely, price above list
11. First-time purchase → max 5-10 units only
12. Publisher itself sells on Amazon (e.g. Haynes, Elsevier) → Avoid or max 5-10

NEW LIMITED BUY RULES (apply automatically when triggered):
A. If margin is very low (buybox < 1.25 × breakeven) BUT 30-day drops ≥15 AND 180-day drops ≥50 → Limited Buy
B. If 30-day drops <10 BUT 180-day drops ≥50 → Limited Buy (long-term demand still strong)
→ "Limited Buy" = exactly 50% of the normally calculated quantity (rounded down)

BASE QUANTITY CALCULATION (before caps & Limited Buy):
- 30d drops ≥50 → 60 units
- 30d drops 35–49 → 40 units
- 30d drops 25–34 → 30 units
- 30d drops 20–24 → 25 units
- 30d drops 15–19 → 20 units
- 30d drops 10–14 → 15 units
- 30d drops <10 → 10 units (only if 180d very strong → triggers Limited Buy)

Then apply caps from rules 1–12 → take the lowest limit.
If Limited Buy triggered → final quantity = 50% of that number (min 5).

OUTPUT — EXACTLY THESE 5 LINES (properly explained reason),  :
Line 1: Decision → Buy / Limited Buy / Avoid / Buy for Peak Only
Line 2: Quantity → exact number or range (e.g. 25 units / 12 units (Limited))
Line 3: Max allowed by rules → number or "No limit"
Line 4: Reason → proper explanation + rule numbers + Limited Buy trigger if any
Line 5: Note → extra comment or "-"
Important: If the  AI decision is Buy then the  `first_time_purchase` is also True  then the quantity must be limited to 5–10 units only. If the decision is Avoid, then the quantity must be 0. 
"""
 







 
 

#5555555555555555555555555555
 
# SYSTEM_PROMPT = """
# You are an expert Amazon FBA book reseller. Follow ALL rules exactly.

# CORE RULES (Blockers – Highest Priority):
# 1. Price frequently near/at breakeven → Max 5–10 units or Avoid
# 2. Amazon price ≤10% above breakeven → Avoid
# 3. 3P sellers frequently drop below breakeven (even if Amazon is high) → Avoid unless drops are very short
# 4. Amazon keeps price < breakeven for 6+ months → Avoid
# 5. Frequent 3P breakeven breaks (e.g., Crown) → Max 5–10 units
# 7. Used price <80% of buybox → Avoid
# 11. First-time purchase → Max 5–10 units
# 12. Publisher sells directly (e.g., Haynes, Elsevier) → Max 5–10 units or Avoid

# POSITIVE RULES (Allow Full Buy):
# 9. Alma Edizioni OR Amazon almost never sells + stable high price → Full Buy
# 10. Books of Discovery OR price almost never drops + strong demand → Full Buy

# QUANTITY CALCULATION (Only if NO blocking rule applies):
# Base quantity from 30-day drops:
# ≥50 → 80 units
# 40–49 → 60 units
# 30–39 → 45 units
# 25–29 → 35 units
# 20–24 → 25 units
# 15–19 → 20 units
# 10–14 → 15 units
# <10 → 10 units

# LIMITED BUY — Trigger ONLY in these TWO cases (and only if no blocking rule applies):
# A. Margin very low (buybox < 1.25 × breakeven) BUT 30d drops ≥10 AND 180d drops ≥50 → Limited Buy = 50% of base
# B. 30d drops <10 BUT 180d drops ≥60 (very strong long-term demand) → Limited Buy = 50% of base

# → If 30d drops ≥20 AND 180d drops are strong → this is a NORMAL FULL BUY, NOT Limited Buy.
# → Use Limited Buy only when margin is weak OR the current month is slow.

# OUTPUT — EXACTLY 5 LINES (explain the correct reason):
# Line 1: Decision → Buy / Limited Buy / Avoid / Buy for Peak Only
# Line 2: Quantity → e.g., 60 units / 30 units (Limited)
# Line 3: Max allowed by rules → Number or "No limit"
# Line 4: Reason → proper explanation + Limited trigger if applicable
# Line 5: Note → Additional comment or "-"

# Important: If the  AI decision is Buy then the  `first_time_purchase` is also True  then the quantity must be limited to 5–10 units only. If the decision is Avoid, then the quantity must be 0. 


# """

 




def generate_purchase_decision(details: dict):
    user_prompt = f"""
Analyze this book data and make a purchasing decision strictly according to the rules:

{details}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()






# ----------------------------
# SAMPLE USAGE
# ----------------------------
# if __name__ == "__main__":
#     from keepa_services import fetch_keepa_data
#     from keepa_client_conditions11 import analyze_prices
#     import numpy as np
#     keys = [
#         65.06, 31.48, 49.90, 39.25, 56.46, 58.99, 20.57,
#         36.88, 21.05, 27.15, 68.68, 81.03, 52.77, 34.46, 166.84
#     ]

#     values = [
#         '9783961713745', '9788861826724', '9788861827240', '9780800636838',
#         '9780998785066', '9780998266343', '9781571208309', '9781909141841',
#         '9781479837243', '9780738612645', '9781302947477', '9781302953645',
#         '9781733686617', '9780964425828', '9780664238261'
#     ]

#     #Create dictionary
#     price_dict = dict(zip(keys, values))

#     # Print formatted output
#     for k, v in price_dict.items():
#             isbn = v
#             breakeven = k  # Example breakeven price
#             print("=========================================")
#             print("\nISBN:", isbn)
#             print("Breakeven Price:", breakeven)
#             keepa_product = fetch_keepa_data(isbn)
#             first_time_purchase= True 
#             result = analyze_prices(keepa_product, breakeven,first_time_purchase)
#             decision = generate_purchase_decision(result)
#             print("\nFINAL DECISION:\n", decision)
#         #   print("\nANALYZED DATA:\n", result)
    
# from keepa_services import fetch_keepa_data
# from keepa_client_conditions11 import analyze_prices
# import numpy as np
    
# isbn = "9780664238261"
# breakeven = 166.84  # Example breakeven price
# print("=========================================")
# print("\nISBN:", isbn)
# print("Breakeven Price:", breakeven)
# keepa_product = fetch_keepa_data(isbn)
# first_time_purchase= True 
# result = analyze_prices(keepa_product, breakeven,first_time_purchase)
# decision = generate_purchase_decision(result)
# print("\nFINAL DECISION:\n", decision)
# #   print("\nANALYZED DATA:\n", result)

     


     
     














































