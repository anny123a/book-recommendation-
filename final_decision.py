
from keepa_services import fetch_keepa_data
from keepa_client_conditions11 import analyze_prices
from salesdata import get_sales_summary
from  keepa_client_conditions14 import generate_purchase_decision
from datetime import datetime
from keepa_client_conditions14 import get_current_season_status




# isbn = '9783961713745' # user input  
# breakeven = 65.06  # user input 
# df = "Sales (1).csv" # upload sales data file 
# print(isbn)

# # Today's date and order date range
# today = datetime.now()
# start_date = "2025-12-10" # user input
# end_date = "2025-12-20"   # user input



# # Get current season status
# current_status = get_current_season_status(today)
# # Fetch Keepa data
# keepa_product = fetch_keepa_data(isbn)
# sales_summary = get_sales_summary(df, isbn)
# print(sales_summary)
# # Past sales data
# pastsales =  sales_summary
# first_time_purchase = False # USER  INPUT
# # Analyze prices
# result = analyze_prices(keepa_product, breakeven, first_time_purchase)
# # Generate purchase decision with seasonal analysis
# decision, seasonal_info = generate_purchase_decision(
# result, 
# pastsales, 
# first_time_purchase,
# start_date,
# end_date
# )
# print(decision)





from datetime import datetime
from typing import Tuple, Dict

def run_full_analysis(
    isbn: str,
    breakeven: float,
    sales_csv_path: str,
    start_date: str,
    end_date: str,
    first_time_purchase: bool = False
) -> Tuple[Dict, Dict]:
    """
    Full workflow:
    1. Read sales CSV
    2. Fetch Keepa data
    3. Analyze prices
    4. Generate purchase decision
    5. Return (decision, seasonal_info)
    """

    # --- Parse dates ---
    today = datetime.now()

    # --- Get season status ---
    current_status = get_current_season_status(today)
    #print("Current Season Status:", current_status)

    # --- Fetch Keepa product data ---
    keepa_product = fetch_keepa_data(isbn)
    print("Keepa Product Data fetched for ISBN:", isbn)

    # --- Load past sales data for this ISBN ---
    sales_summary = get_sales_summary(sales_csv_path, isbn)

    # --- Analyze prices ---
    price_result = analyze_prices(
        keepa_product,
        breakeven,
        first_time_purchase
    )

    # --- Generate final decision ---
    decision, seasonal_info = generate_purchase_decision(
        price_result,
        sales_summary,
        first_time_purchase,
        start_date,
        end_date
    )

    return decision, seasonal_info



isbn = "9788861827288"
breakeven = 24.01
df = "Sales (1).csv"
start_date = "2026-01-10"
end_date = "2026-01-20"
first_time_purchase = False

decision, seasonal_info = run_full_analysis(
    isbn=isbn,
    breakeven=breakeven,
    sales_csv_path=df,
    start_date=start_date,
    end_date=end_date,
    first_time_purchase=first_time_purchase,
)

print("Purchase Decision:", decision)
print("Seasonal Info:", seasonal_info)
