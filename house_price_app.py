import streamlit as st

# Page config
st.set_page_config(page_title="House Price Predictor", layout="centered")

# Title
st.title("🏠 House Price Prediction ")
st.markdown("Enter any of the fields below to estimate house price:")

# Input columns
col1, col2 = st.columns(2)
with col1:
    area = st.number_input("🏡 House Area (sqft)", min_value=0, value=0)
    bedroom = st.number_input("🛏️ Bedrooms", min_value=0, value=0)
with col2:
    washroom = st.number_input("🚿 Washrooms", min_value=0, value=0)
    parking = st.number_input("🚗 Parking Slots", min_value=0, value=0)

# Formula for price prediction (in Lakhs)
def predict_price(area, bedroom, washroom, parking):
    price = (area * 0.05) + (bedroom * 12) + (washroom * 8) + (parking * 4)
    return round(price, 2)

# Button to predict
if st.button("Predict House Price"):
    price = predict_price(area, bedroom, washroom, parking)
    st.success(f"💰 Estimated House Price: ₹ {price} Lakhs")
