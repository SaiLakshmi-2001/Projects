import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Set Streamlit page
st.set_page_config(page_title="PCA Visualization App", layout="wide")

st.title("🌸 PCA on Iris Dataset")
st.markdown("""
This app performs **Principal Component Analysis (PCA)** on the classic Iris dataset and shows how the dimensionality is reduced from 4D to 2D.
""")

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

# Display dataset
st.subheader("📊 Original Dataset (First 10 Rows)")
df = pd.DataFrame(X, columns=feature_names)
df['target'] = [target_names[i] for i in y]
st.dataframe(df.head(10))

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Sidebar: Select number of PCA components
st.sidebar.header("⚙️ PCA Settings")
n_components = st.sidebar.slider("Number of Principal Components", 2, min(4, X.shape[1]), 2)

# Apply PCA
pca = PCA(n_components=n_components)
X_pca = pca.fit_transform(X_scaled)

# Show explained variance
st.subheader("📈 Explained Variance Ratio")
explained_var = pca.explained_variance_ratio_
for i, var in enumerate(explained_var):
    st.write(f"Principal Component {i+1}: {var:.2f}")

st.write(f"**Total Variance Retained:** {np.sum(explained_var):.2f}")

# 2D Scatter plot
if n_components == 2:
    st.subheader("📉 PCA 2D Scatter Plot")

    fig, ax = plt.subplots()
    colors = ['red', 'green', 'blue']
    for i, target_name in enumerate(target_names):
        ax.scatter(X_pca[y == i, 0], X_pca[y == i, 1], 
                   label=target_name, alpha=0.7, color=colors[i])
    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")
    ax.set_title("PCA Result (2D)")
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("2D plot only available when number of components = 2.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and sklearn.")
