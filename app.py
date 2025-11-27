 


import streamlit as st
from keepa_services import fetch_keepa_data
from keepa_client_conditions11 import analyze_prices
import numpy as np
from keepa_client_conditions10 import generate_purchase_decision

# Your existing functions
# fetch_keepa_data()
# analyze_prices()
# generate_purchase_decision()

st.set_page_config(page_title="Book Purchase Decision", layout="centered")



st.title("📘 Book Purchase Decision System")

st.write("Enter the details below:")

# --- User Inputs ---
isbn = st.text_input("Enter ISBN ID")
breakeven = st.text_input("Enter Breakeven Price (BE)")
first_time_purchase = st.checkbox("First Time Purchase?", value=False)

if st.button("Analyze Book"):
    if not isbn or not breakeven:
        st.error("Please fill all fields")
    else:
        try:
            breakeven = float(breakeven)

            # Fetch Keepa data
            keepa_product = fetch_keepa_data(isbn)

            # Run analysis
            result = analyze_prices(keepa_product, breakeven, first_time_purchase)

            # Generate final decision
            decision = generate_purchase_decision(result)

            # Display results
            st.success("Analysis Completed")

            st.subheader("📌 FINAL DECISION")
            st.write(decision)

            st.subheader("📊 ANALYZED DATA")
            st.json(result)

        except Exception as e:
            st.error(f"Error: {e}")
