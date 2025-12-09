 
#old code

# import streamlit as st
# from keepa_services import fetch_keepa_data
# from keepa_client_conditions11 import analyze_prices
# import numpy as np
# from keepa_client_conditions10 import generate_purchase_decision

# # Your existing functions
# # fetch_keepa_data()
# # analyze_prices()
# # generate_purchase_decision()

# st.set_page_config(page_title="Book Purchase Decision", layout="centered")



# st.title("📘 Book Purchase Decision System")

# st.write("Enter the details below:")

# # --- User Inputs ---
# isbn = st.text_input("Enter ISBN ID")
# breakeven = st.text_input("Enter Breakeven Price (BE)")
# first_time_purchase = st.checkbox("First Time Purchase?", value=False)

# if st.button("Analyze Book"):
#     if not isbn or not breakeven:
#         st.error("Please fill all fields")
#     else:
#         try:
#             breakeven = float(breakeven)

#             # Fetch Keepa data
#             keepa_product = fetch_keepa_data(isbn)

#             # Run analysis
#             result = analyze_prices(keepa_product, breakeven, first_time_purchase)

#             # Generate final decision
#             decision = generate_purchase_decision(result)

#             # Display results
#             st.success("Analysis Completed")

#             st.subheader("📌 FINAL DECISION")
#             st.write(decision)

#             st.subheader("📊 ANALYZED DATA")
#             st.json(result)

#         except Exception as e:
#             st.error(f"Error: {e}")













#new code 


 
import streamlit as st
from datetime import datetime
from keepa_services import fetch_keepa_data
from keepa_client_conditions11 import analyze_prices
from salesdata import get_sales_summary
from keepa_client_conditions14 import generate_purchase_decision, get_current_season_status

st.set_page_config(page_title="Book Analyzer Tool", layout="wide")

st.title("📚 Amazon FBA Book Analyzer (Keepa + Sales + Seasons)")

# -----------------------
# USER INPUT SECTION
# -----------------------
st.header("🔧 Input Parameters")

isbn = st.text_input("Enter ISBN:", "9780664238261")
breakeven = st.number_input("Enter Breakeven Price:", min_value=1.0, value=166.84)

start_date = st.date_input("Order Start Date:", datetime(2025, 12, 10))
end_date = st.date_input("Order End Date:", datetime(2025, 12, 20))

uploaded_sales = st.file_uploader("Upload Sales CSV File", type=["csv"])

run_button = st.button("🚀 Run Analysis")

# -----------------------------------------
# PROCESS WHEN BUTTON CLICKED
# -----------------------------------------
if run_button:

    if uploaded_sales is None:
        st.error("❗ Please upload a sales CSV file before running.")
        st.stop()

    today = datetime.now()

    # ===========================================================
    # SUMMARY OF INPUT SECTION (with Peak Season + Total Days)
    # ===========================================================
    st.subheader("📝 Summary of Inputs")
    st.write(f"**ISBN:** {isbn}")
    st.write(f"**Breakeven Price:** {breakeven}")
    st.write(f"**Today's Date:** {today.strftime('%Y-%m-%d')}")
    st.write(f"**Order Period:** {start_date} → {end_date}")

    # -----------------------------------------
    # CURRENT SEASON STATUS
    # -----------------------------------------
    current_status = get_current_season_status(today)

    # -----------------------------------------
    # FETCH KEEPA DATA
    # -----------------------------------------
    keepa_product = fetch_keepa_data(isbn)

    # -----------------------------------------
    # SALES DATA SUMMARY
    # -----------------------------------------
    sales_summary = get_sales_summary(uploaded_sales, isbn)
    pastsales = sales_summary
    first_time_purchase = False

    # -----------------------------------------
    # PRICE ANALYSIS
    # -----------------------------------------
    price_analysis = analyze_prices(keepa_product, breakeven, first_time_purchase)

    # -----------------------------------------
    # SEASONAL PURCHASE DECISION
    # -----------------------------------------
    decision, seasonal_info = generate_purchase_decision(
        price_analysis,
        pastsales,
        first_time_purchase,
        str(start_date),
        str(end_date),
    )

    # ===========================================================
    # EXTRA SUMMARY → Covers Peak Season + Total Days in Period
    # ===========================================================
    st.markdown("### 📌 Additional Summary (Season-Based)")
    st.write(f"**Covers Peak Season:** {seasonal_info['covers_peak']}")
    st.write(f"**Total Days in Ordering Period:** {seasonal_info['total_days']}")

    st.write("---")

    # -----------------------------------------
    # DETAILED SEASON STATUS
    # -----------------------------------------
    st.header("🌤 Current Season Status (From Today)")
    st.write(current_status)

    # -----------------------------------------
    # KEEP PA DATA
    # -----------------------------------------
    st.header("📊 Keepa Data Status")
    st.success("Keepa data fetched successfully.")

    # -----------------------------------------
    # SALES DATA
    # -----------------------------------------
    st.header("📈 Sales Summary")
    st.write(sales_summary)

    # -----------------------------------------
    # PRICE ANALYSIS
    # -----------------------------------------


    # -----------------------------------------
    # SEASONAL ANALYSIS
    # -----------------------------------------
    st.header("🗓 Seasonal Analysis for Order Period")
    st.write(seasonal_info)

    # -----------------------------------------
    # FINAL DECISION
    # -----------------------------------------
    st.header("🎯 Final Purchase Decision")
    st.success(decision)

    st.write("---")
    st.write("Analysis Completed ✔")

    st.header("💲 Price Analysis")
    st.write(price_analysis)
