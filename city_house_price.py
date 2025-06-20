import streamlit as st

# Page setup
st.set_page_config(page_title="City-wise House Price Predictor", layout="centered")
st.title("🏠 City-wise House Price Prediction ")

# Define city-wise pricing weights
city_rates = {
    "Hyderabad":      {"area": 0.05, "bedroom": 10, "washroom": 5, "parking": 2},
    "Bangalore":      {"area": 0.06, "bedroom": 12, "washroom": 6, "parking": 3},
    "Mumbai":         {"area": 0.08, "bedroom": 15, "washroom": 7, "parking": 4},
    "Chennai":        {"area": 0.055, "bedroom": 11, "washroom": 6, "parking": 3},
    "Visakhapatnam":  {"area": 0.045, "bedroom": 9, "washroom": 4, "parking": 2},
    "Pune":           {"area": 0.058, "bedroom": 11, "washroom": 5, "parking": 3},
}

# Select city
city = st.selectbox("Select City", list(city_rates.keys()))

# Input columns
col1, col2 = st.columns(2)
with col1:
    area = st.number_input("🏡 House Area (sqft)", min_value=0, value=0)
    bedroom = st.number_input("🛏️ Bedrooms", min_value=0, value=0)
with col2:
    washroom = st.number_input("🚿 Washrooms", min_value=0, value=0)
    parking = st.number_input("🚗 Parking Slots", min_value=0, value=0)

# Price calculation function
def calculate_price(city, area, bedroom, washroom, parking):
    rates = city_rates[city]
    price = (
        area * rates["area"] + 
        bedroom * rates["bedroom"] + 
        washroom * rates["washroom"] + 
        parking * rates["parking"]
    )
    return round(price, 2)

# Prediction button
if st.button("Predict House Price"):
    price = calculate_price(city, area, bedroom, washroom, parking)
    st.success(f"🏙️ City: {city}\n💰 Estimated Price: ₹ {price} Lakhs")
