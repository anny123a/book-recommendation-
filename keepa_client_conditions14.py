
import pandas as pd
from dotenv import load_dotenv
import os
from openai import OpenAI
from datetime import datetime, timedelta
from typing import Dict, Tuple

load_dotenv() 

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

SYSTEM_PROMPT = """
You are an expert Amazon FBA book reseller. Follow ALL rules below exactly.

CORE RULES (never add new ones):
1  If 30-day drops are greater than 10 and 180-day drops are greater than 50, then Buy. If both drops are 0, then Avoid.
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
A. If margin is very low (buybox < 1.25 × breakeven) BUT 30-day drops ≥10 AND 180-day drops ≥50 → Limited Buy
B. If 30-day drops less than 10 BUT 180-day drops ≥50 → Limited Buy (long-term demand still strong)
→ "Limited Buy" = exactly 50% of the normally calculated quantity (rounded down)

SEASONAL ADJUSTMENT RULES:
- If ordering period covers ONLY non-peak season → use base quantity
- If ordering period covers peak season (even partially) → multiply base quantity by peak multiplier
- Peak multiplier is calculated based on historical sales increase during peak vs non-peak
- For multi-season coverage: allocate quantity proportionally based on days in each season

BASE QUANTITY CALCULATION (before caps & Limited Buy):
- Calculate quantity needed for the EXACT ordering period (day_count days)
- Use past sales data to determine daily sales rate for each season
- Formula: Base Quantity = (days_in_non_peak × non_peak_daily_rate) + (days_in_peak × peak_daily_rate)
- Consider seasonal adjustments: multiply peak season days by the historical peak multiplier
- 30d drops <10 → 5 units (only if 180d very strong → triggers Limited Buy)

Then apply caps from rules 1–12 → take the lowest limit.
If Limited Buy triggered → final quantity = 50% of that number (min 5).

OUTPUT — EXACTLY THESE 7 LINES (properly explained reason):
Line 1: Decision → Buy / Limited Buy / Avoid / Buy for Peak Only
Line 2: Quantity → exact number for day_count days (with seasonal adjustment if applicable)
Line 3: Days of Stock → should equal day_count (the ordering period)
Line 4: Max allowed by rules → number or "No limit"
Line 5: Seasonal Adjustment → breakdown of calculation (X days non-peak + Y days peak with Z× multiplier)
Line 6: Reason → proper explanation + rule numbers + Limited Buy trigger(explain the real reason why Limited Buy is triggered) + seasonal calculation details
Line 7: Note → extra comment or "-"

Important: 
- Quantity MUST cover exactly day_count days based on seasonal daily sales rates
- Days of Stock should equal the ordering period (day_count)
- If the AI decision is Buy and `first_time_purchase` is True, then the quantity must be limited to 5–10 units only. 
- If the decision is Avoid, then the quantity must be 0 and Days of Stock is 0.
- Consider seasonal sales patterns when calculating quantities
"""


from season import get_season_info, get_next_season_change, analyze_seasonal_coverage, calculate_peak_multiplier


def get_current_season_status(current_date: datetime) -> Dict:
    """
    Get detailed information about the current season status from today's perspective.
    """
    current_season = get_season_info(current_date)
    next_change_date, next_season = get_next_season_change(current_date)
    days_until_next_season = (next_change_date - current_date).days
    
    # Get the season after next
    later_change_date, later_season = get_next_season_change(next_change_date)
    days_until_later_season = (later_change_date - current_date).days
    
    return {
        "current_date": current_date.strftime("%Y-%m-%d"),
        "current_season": current_season,
        "next_season": next_season,
        "next_season_change_date": next_change_date.strftime("%Y-%m-%d"),
        "days_until_next_season": days_until_next_season,
        "later_season": later_season,
        "later_season_change_date": later_change_date.strftime("%Y-%m-%d"),
        "days_until_later_season": days_until_later_season
    }


def generate_purchase_decision(
    details: dict, 
    pastsales: pd.DataFrame, 
    first_time_purchase: bool,
    start_date: str,
    end_date: str
) -> Tuple[str, Dict]:
    """
    Generate a purchase decision based on book data, past sales, first-time purchase status,
    and seasonal considerations.
    
    Args:
        details: Dictionary containing book analysis data
        pastsales: DataFrame with historical sales data
        first_time_purchase: Boolean indicating if this is a first-time purchase
        start_date: Order start date in format 'YYYY-MM-DD'
        end_date: Order end date in format 'YYYY-MM-DD'
    
    Returns:
        Tuple of (decision string, seasonal info dict)
    """
    # # Parse dates
    # start = datetime.strptime(start_date, "%Y-%m-%d")
    # end = datetime.strptime(end_date, "%Y-%m-%d")
    
    # # Analyze seasonal coverage
    # seasonal_info = analyze_seasonal_coverage(start, end)
    
    # # Calculate peak multiplier from historical data
    # peak_multiplier = calculate_peak_multiplier(pastsales)
    
    # # Convert pastsales DataFrame to a readable string format
    # sales_summary = pastsales.to_string(index=False)
    
    # # Calculate average monthly sales for context
    # avg_monthly_sales = pastsales['MONTH_QTY'].mean()
    # avg_daily_sales = avg_monthly_sales / 30
    
    # # Calculate seasonal average daily sales
    # pastsales['date'] = pd.to_datetime(pastsales['YEAR_MONTH'] + '-01')
    # pastsales['season'] = pastsales['date'].apply(get_season_info)
    
    # peak_avg_monthly = pastsales[pastsales['season'] == 'Peak Season']['MONTH_QTY'].mean()
    # non_peak_avg_monthly = pastsales[pastsales['season'] == 'Non-Peak Season']['MONTH_QTY'].mean()
    
    # peak_avg_daily = peak_avg_monthly / 30 if peak_avg_monthly > 0 else avg_daily_sales
    # non_peak_avg_daily = non_peak_avg_monthly / 30 if non_peak_avg_monthly > 0 else avg_daily_sales


    # Parse dates
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Analyze seasonal coverage
    seasonal_info = analyze_seasonal_coverage(start, end)

    # Calculate peak multiplier from historical data
    peak_multiplier = calculate_peak_multiplier(pastsales)

    # Convert pastsales DataFrame to a readable string format
    sales_summary = pastsales.to_string(index=True)  # Changed to index=True since YEAR_MONTH is the index

    # Calculate average monthly sales for context
    avg_monthly_sales = pastsales['MONTH_QTY'].mean()
    avg_daily_sales = avg_monthly_sales / 30

    # Calculate seasonal average daily sales - reset index first
    df_season = pastsales.reset_index()
    df_season['date'] = pd.to_datetime(df_season['YEAR_MONTH'].astype(str) + '-01')
    df_season['season'] = df_season['date'].apply(get_season_info)

    peak_avg_monthly = df_season[df_season['season'] == 'Peak Season']['MONTH_QTY'].mean()
    non_peak_avg_monthly = df_season[df_season['season'] == 'Non-Peak Season']['MONTH_QTY'].mean()

    peak_avg_daily = peak_avg_monthly / 30 if peak_avg_monthly > 0 else avg_daily_sales
    non_peak_avg_daily = non_peak_avg_monthly / 30 if non_peak_avg_monthly > 0 else avg_daily_sales
    
    user_prompt = f"""
Analyze this book data and make a purchasing decision strictly according to the rules:

Book Analysis Details:
{details}

Past Sales Data:
{sales_summary}

Sales Statistics:
- Average Monthly Sales: {avg_monthly_sales:.2f} units
- Average Daily Sales: {avg_daily_sales:.2f} units
- Peak Season Avg Daily Sales: {peak_avg_daily:.2f} units
- Non-Peak Season Avg Daily Sales: {non_peak_avg_daily:.2f} units
- Peak Multiplier: {peak_multiplier:.2f}x

Seasonal Analysis:
- Ordering Period: {seasonal_info['start_date']} to {seasonal_info['end_date']} ({seasonal_info['total_days']} days)
- Current Season: {seasonal_info['current_season']} ({seasonal_info['days_in_current_season']} days)
- Next Season: {seasonal_info['next_season']} (starts {seasonal_info['next_season_change_date']}, {seasonal_info['days_in_next_season']} days in ordering period)
- Covers Peak Season: {seasonal_info['covers_peak']}

QUANTITY CALCULATION FORMULA:
If ordering period is in non-peak only: 
  Quantity = {non_peak_avg_daily:.2f} × {seasonal_info['total_days']} = {non_peak_avg_daily * seasonal_info['total_days']:.0f} units

If ordering period covers both seasons:
  Non-peak portion: {non_peak_avg_daily:.2f} × {seasonal_info['days_in_current_season']} = {non_peak_avg_daily * seasonal_info['days_in_current_season']:.0f} units
  Peak portion: {peak_avg_daily:.2f} × {seasonal_info['days_in_next_season']} = {peak_avg_daily * seasonal_info['days_in_next_season']:.0f} units
  Total: {(non_peak_avg_daily * seasonal_info['days_in_current_season'] + peak_avg_daily * seasonal_info['days_in_next_season']):.0f} units

First Time Purchase: {first_time_purchase}

CRITICAL: 
- Calculate quantity to cover EXACTLY {seasonal_info['total_days']} days (day_count)
- Use the appropriate daily sales rate for each season period
- Days of Stock should equal {seasonal_info['total_days']} days
- Then apply rule caps and Limited Buy reductions if triggered
- Provide your decision in exactly 7 lines as specified in the system prompt
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    return response.choices[0].message.content.strip(), seasonal_info










# # Main execution
# if __name__ == "__main__":
#     from keepa_services import fetch_keepa_data
#     from keepa_client_conditions11 import analyze_prices
#     from salesdata import get_sales_summary


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
#             breakeven = k # Example breakeven price
#             print(isbn)

#             # Today's date and order date range
#             today = datetime.now()
#             start_date = "2025-12-10"
#             end_date = "2025-12-20"
            
#             print("=========================================")
#             print("\nISBN:", isbn)
#             print("Breakeven Price:", breakeven)
#             print(f"Today's Date: {today.strftime('%Y-%m-%d')}")
#             print(f"Order Period: {start_date} to {end_date}")
            
#             # Get current season status
#             current_status = get_current_season_status(today)
            
#             print("\n" + "="*50)
#             print("CURRENT SEASON STATUS (From Today)")
#             print("="*50)
#             print(f"Today's Date: {current_status['current_date']}")
#             print(f"Current Season: {current_status['current_season']}")
#             print(f"Days Left in Current Season: {current_status['days_until_next_season']}")
#             print(f"\nUpcoming Season: {current_status['next_season']}")
#             print(f"Next Season Change: {current_status['next_season_change_date']}")
#             print(f"\nLater Season: {current_status['later_season']}")
#             print(f"Days Left Until Later Season: {current_status['days_until_later_season']}")
            
#             # Fetch Keepa data
#             keepa_product = fetch_keepa_data(isbn)
#             df = "Sales (1).csv"
            
#             sales_summary = get_sales_summary(df, isbn)
#             print(sales_summary)

            
#             # Past sales data
#             pastsales =  sales_summary
            
#             first_time_purchase = False # USER  INPUT
            
#             # Analyze prices
#             result = analyze_prices(keepa_product, breakeven, first_time_purchase)
            
#             # Generate purchase decision with seasonal analysis
#             decision, seasonal_info = generate_purchase_decision(
#                 result, 
#                 pastsales, 
#                 first_time_purchase,
#                 start_date,
#                 end_date
#             )
            
#             print("\n" + "="*50)
#             print("ORDER PERIOD SEASONAL ANALYSIS")
#             print("="*50)
#             print(f"Start Date: {seasonal_info['start_date']}")
#             print(f"End Date: {seasonal_info['end_date']}")
#             print(f"Total Days in Ordering Period: {seasonal_info['total_days']}")
#             print(f"\nCurrent Season: {seasonal_info['current_season']}")
#             print(f"Next Season Change Date: {seasonal_info['next_season_change_date']} to {seasonal_info['next_season']}")
#             print(f"Days in Current Season: {seasonal_info['days_in_current_season']}")
#             print(f"Days in Next Season: {seasonal_info['days_in_next_season']}")
#             print(f"\nLater Season Change Date: {seasonal_info['later_season']} starts in {seasonal_info['days_until_later_season']} days")
#             print(f"\nCovers Peak Season: {seasonal_info['covers_peak']}")
            
#             print("\n" + "="*50)
#             print("FINAL DECISION")
#             print("="*50)
#             print(decision)
#             print("======"*70)
#             # print("\nANALYZED DATA:\n", result)
    




