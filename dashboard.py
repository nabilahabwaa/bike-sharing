import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page title
st.set_page_config(page_title="Bike Sharing Analysis Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

all_df = load_data()

# SIDEBAR
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.header("Filter Waktu")
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe berdasarkan Rentang Waktu
main_df = all_df[(all_df["dteday"] >= pd.to_datetime(start_date)) & 
                (all_df["dteday"] <= pd.to_datetime(end_date))]

# --- HEADER ---
st.title("🚲 Bike Sharing Data Analysis Dashboard")

# --- GRAFIK 1: CASUAL VS REGISTERED PER JAM ---
st.subheader("Tren Penyewaan: Casual vs Registered (per Jam)")

# Hitung rata-rata per jam
hourly_users = main_df.groupby('hr')[['casual', 'registered']].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(12, 6))
# Garis untuk Casual
sns.lineplot(data=hourly_users, x='hr', y='casual', label='Casual', marker='o', color='red', ax=ax1)
# Garis untuk Registered
sns.lineplot(data=hourly_users, x='hr', y='registered', label='Registered', marker='o', color='blue', ax=ax1)

ax1.set_xlabel("Jam (0-23)")
ax1.set_ylabel("Rata-rata Jumlah Penyewaan")
ax1.set_xticks(range(0, 24))
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()
st.pyplot(fig1)

st.divider()

# --- GRAFIK 2: TOTAL PENYEWAAN BERDASARKAN CUACA ---
st.subheader("Total Penyewaan Berdasarkan Kondisi Cuaca")

# Kita buat lebih simpel biar nggak error KeyError lagi
weather_rent = main_df.groupby('weathersit')['cnt'].sum().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(data=weather_rent, x='weathersit', y='cnt', palette='viridis', ax=ax2)

ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Total Penyewaan")
st.pyplot(fig2)
