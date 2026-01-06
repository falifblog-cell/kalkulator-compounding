import streamlit as st
import pandas as pd

# --- 1. SETUP PAGE ---
st.set_page_config(page_title="Magic Compounding Calculator", page_icon="✨", layout="centered")

# --- 2. SIDEBAR (TEMA) ---
with st.sidebar:
    st.header("⚙️ Tetapan")
    tema = st.radio("Pilih Tema:", ["🌙 Mode Gelap (Dark)", "☀️ Mode Cerah (Light)"])
    
    st.divider()
    st.info("Kalkulator ini membantu anda melihat potensi simpanan jangka masa panjang.")

# --- CSS TEMA (Dark/Light) ---
if tema == "☀️ Mode Cerah (Light)":
    st.markdown("""
        <style>
            .stApp { background-color: #ffffff; color: #000000; }
            .stNumberInput input { color: #000000 !important; background-color: #f0f2f6 !important; }
            .stMarkdown, .stText, p, label, .stMetricLabel { color: #000000 !important; }
            div[data-testid="stMetricValue"] { color: #000000 !important; }
        </style>
    """, unsafe_allow_html=True)

# --- 3. TAJUK ---
st.title("✨ Magic of Compounding")
st.caption("Lihat bagaimana wang kecil menjadi bukit dengan kuasa faedah kompaun.")

# --- 4. INPUT MODAL ---
st.subheader("1. Tetapan Modal")
col1, col2, col3 = st.columns(3)

# Default values
modal_awal = col1.number_input("💰 Modal Awal (RM)", value=1000.0, step=100.0)
topup_bulanan = col2.number_input("➕ Topup Bulanan (RM)", value=200.0, step=50.0)
tempoh_tahun = col3.number_input("⏳ Tempoh (Tahun)", value=10, step=1)

st.divider()

# --- 5. PILIHAN RETURN (PENTING) ---
st.subheader("2. Tetapan Pulangan (%)")

# Radio button bertindak sebagai suis. Pilih satu, yang lain sorok.
jenis_kiraan = st.radio("Pilih cara kira % pulangan:", 
                        ["A. Set % Sendiri (Manual)", "B. Kira Ikut Rekod Lepas (Average)"], 
                        horizontal=True)

kadar_pulangan = 0.0

# --- PILIHAN A: MANUAL ---
if "Manual" in jenis_kiraan:
    st.info("Masukkan anggaran pulangan tetap setiap tahun (Contoh: ASB 5%, Saham 10%).")
    kadar_pulangan = st.slider("Anggaran Pulangan (%)", 1.0, 30.0, 6.0, 0.5)

# --- PILIHAN B: REKOD LEPAS (AVERAGE) ---
else:
    st.warning("Masukkan rekod pulangan portfolio anda untuk 3 tahun lepas.")
    
    # Guna Expander supaya nampak macam "Add Button"
    # Dia kemas, tak panjang berjela.
    c1, c2, c3 = st.columns(3)
    y1 = c1.number_input("Tahun 1 (%)", value=12.0)
    y2 = c2.number_input("Tahun 2 (%)", value=5.0)
    y3 = c3.number_input("Tahun 3 (%)", value=8.0)
    
    # Logic Kira Average
    avg_rate = (y1 + y2 + y3) / 3
    kadar_pulangan = avg_rate
    
    st.write("---")
    st.success(f"Purata Pulangan (Average): **{avg_rate:.2f}%**")

st.divider()

# --- 6. KIRAAN & OUTPUT ---
if st.button("🚀 Jana Kekayaan Saya", type="primary"):
    
    # Logik Matematik Compounding
    data_tahun = []
    data_nilai = []
    data_modal = []
    
    current_balance = modal_awal
    total_invested = modal_awal
    
    # Tahun 0 (Permulaan)
    data_tahun.append(0)
    data_nilai.append(current_balance)
    data_modal.append(total_invested)
    
    # Loop untuk setiap tahun
    for t in range(1, int(tempoh_tahun) + 1):
        topup_tahunan = topup_bulanan * 12
        
        # Formula: (Duit Sedia Ada + Topup) * (Interest)
        interest = (current_balance + topup_tahunan) * (kadar_pulangan / 100)
        current_balance = current_balance + topup_tahunan + interest
        total_invested += topup_tahunan
        
        data_tahun.append(t)
        data_nilai.append(current_balance)
        data_modal.append(total_invested)

    # --- PAPARAN HASIL ---
    st.subheader(f"📊 Hasil Selepas {tempoh_tahun} Tahun")
    
    # Metric Besar
    untung_bersih = current_balance - total_invested
    roi = (untung_bersih / total_invested) * 100
    
    m1, m2, m3 = st.columns(3)
    m1.metric("💰 Nilai Akhir Portfolio", f"RM {current_balance:,.2f}")
    m2.metric("💸 Modal Dikeluarkan", f"RM {total_invested:,.2f}")
    m3.metric("📈 Untung Bersih (Interest)", f"RM {untung_bersih:,.2f}", f"{roi:.1f}%")
    
    # Graf
    df = pd.DataFrame({
        "Tahun": data_tahun,
        "Nilai Portfolio (RM)": data_nilai,
        "Modal Asal (RM)": data_modal
    })
    df = df.set_index("Tahun")
    
    st.write("### 📉 Graf Pertumbuhan Aset")
    st.line_chart(df, color=["#00CC96", "#EF553B"]) # Hijau (Untung) & Merah (Modal)
    
    # Table (Disorok dalam expander supaya tak semak)
    with st.expander("Lihat Jadual Terperinci Tahunan"):
        st.dataframe(df)
