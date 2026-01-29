
from datetime import datetime, timedelta
from typing import Tuple, Dict
import pandas as pd




def get_season_info(date: datetime) -> str:
    """
    Determine which season a given date falls into.
    
    Peak Season: 16th Dec – 15th Feb
    Non-Peak Season: 16th Feb – 15th Jun
    Peak Season: 16th Jun – 15th Sep
    Non-Peak Season: 16th Sep – 15th Dec
    """
    month = date.month
    day = date.day
    
    # Convert to comparable format (month * 100 + day)
    date_val = month * 100 + day
    
    if (date_val >= 1216) or (date_val <= 215):
        return "Peak Season"
    elif (date_val >= 216) and (date_val <= 615):
        return "Non-Peak Season"
    elif (date_val >= 616) and (date_val <= 915):
        return "Peak Season"
    else:  # 916 to 1215
        return "Non-Peak Season"


def get_next_season_change(date: datetime) -> Tuple[datetime, str]:
    """Get the next season change date and the season it will change to."""
    year = date.year
    month = date.month
    day = date.day
    
    # Season change dates
    season_changes = [
        (datetime(year, 2, 16), "Non-Peak Season"),
        (datetime(year, 6, 16), "Peak Season"),
        (datetime(year, 9, 16), "Non-Peak Season"),
        (datetime(year, 12, 16), "Peak Season"),
    ]
    
    # Add next year's first change
    season_changes.append((datetime(year + 1, 2, 16), "Non-Peak Season"))
    
    for change_date, season in season_changes:
        if date < change_date:
            return change_date, season
    
    return season_changes[0]


def analyze_seasonal_coverage(start_date: datetime, end_date: datetime) -> Dict:
    """
    Analyze which seasons the ordering period covers and calculate days in each.
    Note: Includes both start_date and end_date (inclusive counting)
    """
    # Total days is inclusive of both start and end dates
    total_days = (end_date - start_date).days + 1
    
    current_season = get_season_info(start_date)
    next_change_date, next_season = get_next_season_change(start_date)
    
    # Calculate days in current season (up to but NOT including the change date)
    if end_date < next_change_date:
        # Entire period is in current season
        days_in_current_season = total_days
        days_in_next_season = 0
    else:
        # Period spans into next season
        # Days from start_date to day before next_change_date
        days_in_current_season = (next_change_date - start_date).days
        # Remaining days from next_change_date to end_date (inclusive)
        days_in_next_season = (end_date - next_change_date).days + 1
    
    # Get the season after next if needed
    later_change_date, later_season = get_next_season_change(next_change_date)
    days_until_later_season = (later_change_date - start_date).days
    
    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "total_days": total_days,
        "current_season": current_season,
        "days_in_current_season": days_in_current_season,
        "next_season": next_season,
        "next_season_change_date": next_change_date.strftime("%Y-%m-%d"),
        "days_in_next_season": days_in_next_season,
        "later_season": later_season,
        "days_until_later_season": days_until_later_season,
        "covers_peak": "Peak Season" in [current_season, next_season]
    }


# def calculate_peak_multiplier(pastsales: pd.DataFrame) -> float:
#     """
#     Calculate the peak vs non-peak sales multiplier from historical data.
#     """
#     # Add season column to sales data
#     pastsales['date'] = pd.to_datetime(pastsales['YEAR_MONTH'] + '-01')
#     pastsales['season'] = pastsales['date'].apply(get_season_info)
    
#     # Calculate average sales for each season
#     peak_sales = pastsales[pastsales['season'] == 'Peak Season']['MONTH_QTY'].mean()
#     non_peak_sales = pastsales[pastsales['season'] == 'Non-Peak Season']['MONTH_QTY'].mean()
    
#     if non_peak_sales > 0:
#         multiplier = peak_sales / non_peak_sales
#     else:
#         multiplier = 2.0  # Default assumption
    
#     return max(1.5, min(3.0, multiplier))  # Clamp between 1.5x and 3x


# def calculate_peak_multiplier(pastsales: pd.DataFrame) -> float:
#     """
#     Calculate the peak vs non-peak sales multiplier from historical data.
#     """
#     # Reset index to access YEAR_MONTH as a column
#     df = pastsales.reset_index()
    
#     # Convert YEAR_MONTH string to datetime
#     df['date'] = pd.to_datetime(df['YEAR_MONTH'].astype(str) + '-01')
#     df['season'] = df['date'].apply(get_season_info)

#     # Calculate average sales for each season
#     peak_sales = df[df['season'] == 'Peak Season']['MONTH_QTY'].mean()
#     non_peak_sales = df[df['season'] == 'Non-Peak Season']['MONTH_QTY'].mean()

#     if non_peak_sales > 0:
#         multiplier = peak_sales / non_peak_sales
#     else:
#         multiplier = 2.0  # Default assumption

#     return max(1.5, min(3.0, multiplier))  # Clamp between 1.5x and 3x







# for empty past sales data


def calculate_peak_multiplier(pastsales: pd.DataFrame) -> float:
    """
    Calculate the peak vs non-peak sales multiplier from historical data.
    Returns default multiplier if no historical data available.
    """
    # Handle empty DataFrame
    if pastsales.empty:
        return 2.0  # Default multiplier for first-time purchases
    
    # Reset index to access YEAR_MONTH as a column
    df = pastsales.reset_index()
    
    # Convert YEAR_MONTH string to datetime
    df['date'] = pd.to_datetime(df['YEAR_MONTH'].astype(str) + '-01')
    df['season'] = df['date'].apply(get_season_info)

    # Calculate average sales for each season
    peak_sales = df[df['season'] == 'Peak Season']['MONTH_QTY'].mean()
    non_peak_sales = df[df['season'] == 'Non-Peak Season']['MONTH_QTY'].mean()

    if non_peak_sales > 0:
        multiplier = peak_sales / non_peak_sales
    else:
        multiplier = 2.0  # Default assumption

    return max(1.5, min(3.0, multiplier))  # Clamp between 1.5x and 3x
