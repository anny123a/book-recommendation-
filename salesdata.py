import pandas as pd
def get_sales_summary(df, isbn):

  df2 = pd.read_csv(df, header=0)

  # Fix columns and data types
  df2.columns = df2.iloc[0]
  df2 = df2[1:].reset_index(drop=True)
  df2['QTY'] = pd.to_numeric(df2['QTY'], errors='coerce')
  df2['TOTAL AMOUNT'] = pd.to_numeric(df2['TOTAL AMOUNT'], errors='coerce')


  isbn=isbn.strip()

  if isbn not in df2['ISBN'].unique():
    return "ISBN not found"
  else:
    # Filter rows for this ISBN
    df_isbn = df2[df2['ISBN'] == isbn].copy()

    # Convert DATE to datetime
    df_isbn['DATE'] = pd.to_datetime(df_isbn['DATE'])

    # Create Year-Month
    df_isbn['YEAR_MONTH'] = df_isbn['DATE'].dt.to_period('M')

    # Group by month: Quantity + Price sum
    monthly_summary = df_isbn.groupby('YEAR_MONTH').agg(
        MONTH_QTY=('QTY', 'sum'),
        MONTH_PRICE=('TOTAL AMOUNT', 'sum')
    )

    # Add Selling Price Per Piece = MONTH_PRICE / MONTH_QTY
    monthly_summary['SELLING_PRICE_PER_PIECE'] = (
        monthly_summary['MONTH_PRICE'] / monthly_summary['MONTH_QTY']
    )
    #print(monthly_summary)
    # sales_summary = monthly_summary.to_string(index=True)
    return monthly_summary




# df = "Sales (1).csv"
# id = "9781302953645"
# sales_summary = get_sales_summary(df, id)
# print(sales_summary)
