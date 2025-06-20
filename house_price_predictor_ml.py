import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Page setup
st.set_page_config(page_title="City House Price Prediction (ML)", layout="centered")
st.title("🏠 House Price Prediction using Linear Regression")

# Define city-wise weights (used to generate synthetic training data)
city_weights = {
    "Hyderabad":      {"area": 0.05,  "bedroom": 10, "washroom": 5, "parking": 2},
    "Bangalore":      {"area": 0.06,  "bedroom": 12, "washroom": 6, "parking": 3},
    "Mumbai":         {"area": 0.08,  "bedroom": 15, "washroom": 7, "parking": 4},
    "Chennai":        {"area": 0.055, "bedroom": 11, "washroom": 6, "parking": 3},
    "Visakhapatnam":  {"area": 0.045, "bedroom": 9,  "washroom": 4, "parking": 2},
    "Pune":           {"area": 0.058, "bedroom": 11, "washroom": 5, "parking": 3},
}

# Generate synthetic training data
def generate_training_data(city):
    np.random.seed(42)
    data = []
    weights = city_weights[city]
    for _ in range(100):
        area = np.random.randint(500, 3000)
        bedroom = np.random.randint(1, 6)
        washroom = np.random.randint(1, 5)
        parking = np.random.randint(0, 3)
        price = (
            area * weights["area"] +
            bedroom * weights["bedroom"] +
            washroom * weights["washroom"] +
            parking * weights["parking"]
        ) + np.random.normal(0, 5)  # add noise
        data.append([area, bedroom, washroom, parking, price])
    df = pd.DataFrame(data, columns=["area", "bedroom", "washroom", "parking", "price"])
    return df

# Select city
city = st.selectbox("📍 Select City", list(city_weights.keys()))

# User Inputs
st.markdown("### 📝 Enter House Details:")
col1, col2 = st.columns(2)
with col1:
    area = st.number_input("🏡 Area (in sqft)", min_value=0, value=1000)
    bedroom = st.number_input("🛏️ Bedrooms", min_value=0, value=2)
with col2:
    washroom = st.number_input("🚿 Washrooms", min_value=0, value=2)
    parking = st.number_input("🚗 Parking Slots", min_value=0, value=1)

# Predict button
if st.button("🔮 Predict House Price"):
    # Train model using synthetic data for selected city
    df = generate_training_data(city)
    X = df[["area", "bedroom", "washroom", "parking"]]
    y = df["price"]
    model = LinearRegression()
    model.fit(X, y)

    # Predict
    input_data = [[area, bedroom, washroom, parking]]
    predicted_price = model.predict(input_data)[0]

    st.success(f"🏙️ City: {city}\n💰 Estimated House Price: ₹ {predicted_price:.2f} Lakhs")
