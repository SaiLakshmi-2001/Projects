import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# City-wise pricing rates
city_rates = {
    "Hyderabad":      {"area": 0.05,  "bedroom": 10, "washroom": 5, "parking": 2},
    "Bangalore":      {"area": 0.06,  "bedroom": 12, "washroom": 6, "parking": 3},
    "Mumbai":         {"area": 0.08,  "bedroom": 15, "washroom": 7, "parking": 4},
    "Chennai":        {"area": 0.055, "bedroom": 11, "washroom": 6, "parking": 3},
    "Visakhapatnam":  {"area": 0.045, "bedroom": 9,  "washroom": 4, "parking": 2},
    "Pune":           {"area": 0.058, "bedroom": 11, "washroom": 5, "parking": 3},
}

# Create synthetic training data
data = []
for city, rates in city_rates.items():
    for i in range(100):
        area = 500 + i * 10
        bedroom = i % 5 + 1
        washroom = i % 3 + 1
        parking = i % 2
        price = (area * rates["area"] +
                 bedroom * rates["bedroom"] +
                 washroom * rates["washroom"] +
                 parking * rates["parking"])
        data.append([city, area, bedroom, washroom, parking, price])

df = pd.DataFrame(data, columns=["city", "area", "bedroom", "washroom", "parking", "price"])

# One-hot encode city
df = pd.get_dummies(df, columns=["city"], drop_first=True)

# Split data
X = df.drop("price", axis=1)
y = df["price"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model and feature names
with open("house_price_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model_features.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("✅ Model trained and saved using pickle.")
