
import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Inisialisasi session state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Waktu", "Kelembaban", "pH", "Nitrogen", "Fosfor", "Kalium"])
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Sidebar untuk login
with st.sidebar:
    st.title("🔐 Login SoilSense")
    username = st.text_input("ID Anda")
    password = st.text_input("Password", type="password")
    login = st.button("Login")

    if login:
        if username == "penkom" and password == "soilsense":
            st.session_state.authenticated = True
        else:
            st.error("ID atau password salah")

# Jika sudah login, tampilkan aplikasi utama
if st.session_state.authenticated:
    st.markdown(
        """
        <div style="background-color:#fff7f7;padding:20px 30px;border-radius:18px;margin-bottom:20px;">
            <h2 style="margin-bottom:0;color:#245b4e;">🌱 SoilSense</h2>
            <p style="margin-top:4px;font-size:14px;">Selamat datang di SoilSense! Pantau kondisi tanah secara real-time dan akurat.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tombol update data
    st.button("⭮ Perbarui Data", on_click=lambda: st.session_state.data.insert(0, {
        "Waktu": datetime.now().strftime("%H:%M:%S"),
        "Kelembaban": round(random.uniform(30, 70), 2),
        "pH": round(random.uniform(5.5, 7.5), 2),
        "Nitrogen": round(random.uniform(30, 80), 2),
        "Fosfor": round(random.uniform(20, 50), 2),
        "Kalium": round(random.uniform(100, 180), 2),
    }, allow_duplicates=False))

    st.markdown("---")

    # Tampilkan layout grafik dan tabel berdampingan
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📊 Grafik Parameter Tanah")
        if not st.session_state.data.empty:
            st.line_chart(st.session_state.data.set_index("Waktu")[["Kelembaban", "pH", "Nitrogen", "Fosfor", "Kalium"]])
        else:
            st.info("Belum ada data untuk ditampilkan.")

    with col2:
        st.subheader("📋 Tabel Data")
        st.dataframe(st.session_state.data)

    st.markdown("---")
    
    # Analisis dan Rekomendasi
    st.markdown("### 🧪 Analisis Parameter")
    if not st.session_state.data.empty:
        latest = st.session_state.data.iloc[0]
        analisis = []
        rekomendasi = []

        if latest["Kelembaban"] < 35:
            analisis.append("Kelembaban rendah (tanah kering)")
        elif latest["Kelembaban"] > 65:
            analisis.append("Kelembaban tinggi (tanah terlalu basah)")
        else:
            analisis.append("Kelembaban ideal")

        if latest["pH"] < 6.0:
            analisis.append("pH rendah (tanah asam)")
            rekomendasi.append("Tambahkan kapur dolomit.")
        elif latest["pH"] > 7.5:
            analisis.append("pH tinggi (tanah basa)")
            rekomendasi.append("Gunakan bahan organik.")
        else:
            analisis.append("pH optimal")
            rekomendasi.append("pH tidak perlu disesuaikan.")

        if latest["Nitrogen"] < 40:
            analisis.append("Nitrogen rendah")
            rekomendasi.append("Gunakan pupuk urea atau ZA.")
        else:
            analisis.append("Nitrogen cukup")

        if latest["Fosfor"] < 25:
            analisis.append("Fosfor rendah")
            rekomendasi.append("Gunakan pupuk SP-36 atau TSP.")
        else:
            analisis.append("Fosfor cukup")

        if latest["Kalium"] < 120:
            analisis.append("Kalium rendah")
            rekomendasi.append("Gunakan pupuk KCl atau pupuk kandang.")
        else:
            analisis.append("Kalium cukup")

        st.success(" • ".join(analisis))

        st.markdown("### 💡 Rekomendasi Pemupukan")
        for r in rekomendasi:
            st.write(f"- {r}")
    else:
        st.info("Belum ada data untuk dianalisis.")
