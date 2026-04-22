import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import streamlit as st

# =========================
# TITLE
# =========================
st.title("🧲 Dashboard Magnetometer (Rolling Measurement)")

# =========================
# UPLOAD FILE
# =========================
uploaded_file = st.file_uploader("Upload CSV Data", type=["csv"])

if uploaded_file is not None:
    
    # =========================
    # BACA DATA
    # =========================
    data = pd.read_csv(uploaded_file)
    data = data.dropna().reset_index(drop=True)

    # =========================
    # HITUNG B TOTAL
    # =========================
    data['B'] = np.sqrt(data['Bx']**2 + data['By']**2 + data['Bz']**2)

    # =========================
    # TAMPILKAN TABEL
    # =========================
    st.subheader("📊 Data Magnetik")
    st.dataframe(data)

    # =========================
    # AMBIL DATA
    # =========================
    x = data['x']
    y = data['y']
    z = data['B']

    # =========================
    # GRID
    # =========================
    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)
    xi, yi = np.meshgrid(xi, yi)

    zi = griddata((x, y), z, (xi, yi), method='linear')

    # =========================
    # PLOT
    # =========================
    fig, ax = plt.subplots()

    contour = ax.contourf(xi, yi, zi, cmap='jet')
    plt.colorbar(contour, ax=ax, label='Medan Magnet (nT)')
    ax.scatter(x, y, color='black')

    # label nilai
    for xi_val, yi_val, zi_val in zip(x, y, z):
        ax.text(xi_val, yi_val, f"{zi_val:.0f}",
                color='white', fontsize=8,
                ha='center', va='center')

    ax.set_title("Peta Anomali Magnetik")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # =========================
    # TAMPILKAN DI UI
    # =========================
    st.subheader("🗺️ Peta Magnetik")
    st.pyplot(fig)

else:
    st.info("Silakan upload file CSV terlebih dahulu")