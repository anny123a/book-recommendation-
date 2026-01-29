# import pandas as pd
# def get_sales_summary(df,isbn: str) -> pd.DataFrame:

#   df2 = pd.read_csv(df, header=0)
   
#   # Fix columns and data types
#   df2.columns = df2.iloc[0]
#   df2 = df2[1:].reset_index(drop=True)
   
#   df2['QTY'] = pd.to_numeric(df2['QTY'], errors='coerce')
#   df2['TOTAL AMOUNT'] = pd.to_numeric(df2['TOTAL AMOUNT'], errors='coerce')
#   isbn=isbn.strip()
#   if isbn not in df2['ISBN'].unique():
#     return "ISBN not found"
#   else:
#     # Filter rows for this ISBN
#     df_isbn = df2[df2['ISBN'] == isbn].copy()

#     # Convert DATE to datetime
#     df_isbn['DATE'] = pd.to_datetime(df_isbn['DATE'])

#     # Create Year-Month
#     df_isbn['YEAR_MONTH'] = df_isbn['DATE'].dt.to_period('M')

#     # Group by month: Quantity + Price sum
#     monthly_summary = df_isbn.groupby('YEAR_MONTH').agg(
#         MONTH_QTY=('QTY', 'sum'),
#         MONTH_PRICE=('TOTAL AMOUNT', 'sum')
#     )

#     # Add Selling Price Per Piece = MONTH_PRICE / MONTH_QTY
#     monthly_summary['SELLING_PRICE_PER_PIECE'] = (
#         monthly_summary['MONTH_PRICE'] / monthly_summary['MONTH_QTY']
#     )
#     # print(monthly_summary)
#     # sales_summary = monthly_summary.to_string(index=True)
    
#     return monthly_summary



# import pandas as pd

# def get_sales_summary(df, isbn: str,) -> pd.DataFrame:

#     # Read CSV
#     df2 = pd.read_csv(df, header=1)

#     # Fix numeric columns
#     df2['QTY'] = pd.to_numeric(df2['QTY'], errors='coerce')
#     df2['TOTAL AMOUNT'] = pd.to_numeric(df2['TOTAL AMOUNT'], errors='coerce')

#     # Convert ISBN to string (IMPORTANT FIX)
#     df2['ISBN'] = df2['ISBN'].astype(str).str.strip()
#     isbn = str(isbn).strip()
#     # Filter rows
#     df_isbn = df2[df2['ISBN'] == isbn].copy()
 

#     if df_isbn.empty:
        
#         return pd.DataFrame()

#     # Convert date column
#     df_isbn['DATE'] = pd.to_datetime(df_isbn['DATE'], errors='coerce')

#     # Create Year-Month
#     df_isbn['YEAR_MONTH'] = df_isbn['DATE'].dt.to_period('M')

#     # Group by month
#     monthly_summary = df_isbn.groupby('YEAR_MONTH').agg(
#         MONTH_QTY=('QTY', 'sum'),
#         MONTH_PRICE=('TOTAL AMOUNT', 'sum')
#     )

#     # Selling Price Per Piece
#     monthly_summary['SELLING_PRICE_PER_PIECE'] = (
#         monthly_summary['MONTH_PRICE'] / monthly_summary['MONTH_QTY']
#     )

#     return monthly_summary  


 
 
 
 
 
 
import pandas as pd

def get_sales_summary(df, isbn: str) -> pd.DataFrame:
    # Read CSV
    df2 = pd.read_csv(df, header=1)

    # Fix numeric columns
    df2['QTY'] = pd.to_numeric(df2['QTY'], errors='coerce')
    df2['TOTAL AMOUNT'] = pd.to_numeric(df2['TOTAL AMOUNT'], errors='coerce')

    # --- Normalize ISBNs ---
    def normalize_isbn(x):
        return (
            str(x)
            .replace('.0', '')
            .replace('-', '')
            .strip()
        )

    df2['ISBN'] = df2['ISBN'].apply(normalize_isbn)
    isbn = normalize_isbn(isbn)

    # Filter rows by ISBN
    df_isbn = df2[df2['ISBN'] == isbn].copy()

    # --- SAFE EMPTY RETURN ---
    if df_isbn.empty:
        # Return empty DataFrame WITH expected structure
        return pd.DataFrame(
            columns=[
                'MONTH_QTY',
                'MONTH_PRICE',
                'SELLING_PRICE_PER_PIECE'
            ]
        )

    # Convert date column
    df_isbn['DATE'] = pd.to_datetime(df_isbn['DATE'], errors='coerce')

    # Drop rows with invalid dates
    df_isbn = df_isbn.dropna(subset=['DATE'])

    if df_isbn.empty:
        return pd.DataFrame(
            columns=[
                'MONTH_QTY',
                'MONTH_PRICE',
                'SELLING_PRICE_PER_PIECE'
            ]
        )

    # Create Year-Month
    df_isbn['YEAR_MONTH'] = df_isbn['DATE'].dt.to_period('M')

    # Group by month
    monthly_summary = df_isbn.groupby('YEAR_MONTH').agg(
        MONTH_QTY=('QTY', 'sum'),
        MONTH_PRICE=('TOTAL AMOUNT', 'sum')
    )

    # Avoid division by zero
    monthly_summary['SELLING_PRICE_PER_PIECE'] = (
        monthly_summary['MONTH_PRICE'] / monthly_summary['MONTH_QTY'].replace(0, pd.NA)
    )

    return monthly_summary

 


# df = "Sales (1).csv"
# id ="9788861827288"
# #id = "9783961713745"
# # breakeven = 24.01

# sales_summary = get_sales_summary(df, id)
# print(sales_summary)
 
















 
        