import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

# Load dataset
df = pd.read_csv("house_price.csv")

# Prepare features and target
X = df.drop(["Id", "Price"], axis=1)
y = df["Price"]

# Categorical and numerical features
categorical_features = ["Location", "Condition", "Garage"]
numeric_features = [col for col in X.columns if col not in categorical_features]

# Preprocessing + model pipeline
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(drop="first"), categorical_features)
], remainder="passthrough")

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
pipeline.fit(X_train, y_train)

# Save model
with open("linear_regression_model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("✅ Model trained and saved as 'linear_regression_model.pkl'")
