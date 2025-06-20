import streamlit as st
import pandas as pd
import pickle

# Load trained model
with open("linear_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="🏡 House Price Predictor", layout="centered")
st.title("🏠 House Price Prediction (with Linear Regression)")

# User input
st.subheader("📋 Enter House Details")

locations = ['Downtown', 'Suburban', 'Countryside']
conditions = ['Excellent', 'Good', 'Fair']
garages = ['Yes', 'No']

col1, col2 = st.columns(2)
with col1:
    area = st.number_input("Area (sqft)", min_value=500, max_value=10000, value=1500)
    bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3)
    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=2)

with col2:
    floors = st.number_input("Floors", min_value=1, max_value=5, value=2)
    year = st.number_input("Year Built", min_value=1900, max_value=2025, value=2000)
    location = st.selectbox("Location", locations)
    condition = st.selectbox("Condition", conditions)
    garage = st.selectbox("Garage", garages)

# Prediction button
if st.button("🔮 Predict House Price"):
    input_df = pd.DataFrame([{
        "Area": area,
        "Bedrooms": bedrooms,
        "Bathrooms": bathrooms,
        "Floors": floors,
        "YearBuilt": year,
        "Location": location,
        "Condition": condition,
        "Garage": garage
    }])

    prediction = model.predict(input_df)[0]
    st.success(f"💰 Estimated House Price: ₹ {round(prediction):,}")


