import streamlit as st
import pickle
import pandas as pd

# Load model and features
with open("house_price_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model_features.pkl", "rb") as f:
    features = pickle.load(f)

st.set_page_config(page_title="City House Price Predictor", layout="centered")
st.title("🏠 City-Based House Price Prediction (ML with Pickle)")

# City selection
cities = ["Hyderabad", "Bangalore", "Mumbai", "Chennai", "Visakhapatnam", "Pune"]
city = st.selectbox("📍 Select City", cities)

# Inputs
st.markdown("### 📝 Enter House Details:")
col1, col2 = st.columns(2)
with col1:
    area = st.number_input("🏡 House Area (in sqft)", min_value=0, value=0)
    bedroom = st.number_input("🛏️ Bedrooms", min_value=0, value=0)
with col2:
    washroom = st.number_input("🚿 Washrooms", min_value=0, value=0)
    parking = st.number_input("🚗 Parking Slots", min_value=0, value=0)

# Predict
if st.button("🔮 Predict House Price"):
    if area == 0 and bedroom == 0 and washroom == 0 and parking == 0:
        st.warning("⚠️ Please enter at least one detail to calculate the price.")
    else:
        # Prepare input
        input_dict = {
            "area": area,
            "bedroom": bedroom,
            "washroom": washroom,
            "parking": parking,
        }
        # Add encoded city columns
        for col in features:
            if col.startswith("city_"):
                input_dict[col] = 1 if f"city_{city}" == col else 0

        input_df = pd.DataFrame([input_dict])
        input_df = input_df.reindex(columns=features, fill_value=0)

        # Predict
        predicted_price = model.predict(input_df)[0]
        st.success(f"🏙️ City: **{city}**\n💰 Estimated House Price: ₹ **{round(predicted_price, 2)} Lakhs**")



