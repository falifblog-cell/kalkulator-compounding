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

# --- CSS TEMA ---
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
modal_awal = col1.number_input("💰 Modal Awal (RM)", value=1000.0, step=100.0)
topup_bulanan = col2.number_input("➕ Topup Bulanan (RM)", value=200.0, step=50.0)
tempoh_tahun = col3.number_input("⏳ Tempoh (Tahun)", value=10, step=1)

st.divider()

# --- 5. PILIHAN RETURN (DINAMIK) ---
st.subheader("2. Tetapan Pulangan (%)")

# Dua Pilihan Utama
jenis_kiraan = st.radio("Pilih cara kira % pulangan:", 
                        ["A. Set % Sendiri (Manual)", 
                         "B. Ikut Rekod Lepas (Average)"], 
                        horizontal=True)

kadar_pulangan = 0.0

# --- PILIHAN A: MANUAL ---
if "Manual" in jenis_kiraan:
    st.info("Masukkan anggaran pulangan tetap setiap tahun.")
    kadar_pulangan = st.slider("Anggaran Pulangan (%)", min_value=1.0, max_value=50.0, value=6.0, step=0.25)

# --- PILIHAN B: REKOD LEPAS (DINAMIK BUTTON) ---
else:
    # 1. Setup Session State (Ingatan Sementara)
    if 'bil_tahun' not in st.session_state:
        st.session_state.bil_tahun = 3 # Default mula dengan 3 tahun

    # 2. Butang Tambah / Tolak
    st.write("Berapa tahun rekod anda ada?")
    c_minus, c_text, c_plus = st.columns([1, 2, 1])
    
    with c_minus:
        if st.button("➖ Kurangkan"):
            if st.session_state.bil_tahun > 1:
                st.session_state.bil_tahun -= 1
    
    with c_text:
        st.markdown(f"<h4 style='text-align: center;'>{st.session_state.bil_tahun} Tahun</h4>", unsafe_allow_html=True)
    
    with c_plus:
        if st.button("➕ Tambah"):
            if st.session_state.bil_tahun < 5:
                st.session_state.bil_tahun += 1

    # 3. Paparkan Input Mengikut Bilangan Tahun
    st.write("---")
    inputs = []
    cols = st.columns(st.session_state.bil_tahun) # Auto pecah kolum ikut bilangan
    
    for i in range(st.session_state.bil_tahun):
        with cols[i]:
            val = st.number_input(f"Thn {i+1} (%)", value=5.0 + i, step=0.5, key=f"yr_{i}")
            inputs.append(val)
    
    # 4. Kira Average
    avg_rate = sum(inputs) / len(inputs)
    kadar_pulangan = avg_rate
    st.success(f"Purata Pulangan: **{avg_rate:.2f}%**")

st.divider()

# --- 6. KIRAAN & OUTPUT ---
if st.button("🚀 Jana Kekayaan Saya", type="primary"):
    
    data_tahun = []
    data_nilai = []
    data_modal = []
    
    current_balance = modal_awal
    total_invested = modal_awal
    
    data_tahun.append(0)
    data_nilai.append(current_balance)
    data_modal.append(total_invested)
    
    for t in range(1, int(tempoh_tahun) + 1):
        topup_tahunan = topup_bulanan * 12
        interest = (current_balance + topup_tahunan) * (kadar_pulangan / 100)
        current_balance = current_balance + topup_tahunan + interest
        total_invested += topup_tahunan
        
        data_tahun.append(t)
        data_nilai.append(current_balance)
        data_modal.append(total_invested)

    # --- PAPARAN HASIL ---
    st.subheader(f"📊 Hasil Selepas {tempoh_tahun} Tahun")
    
    untung_bersih = current_balance - total_invested
    roi = (untung_bersih / total_invested) * 100
    
    m1, m2, m3 = st.columns(3)
    m1.metric("💰 Nilai Akhir Portfolio", f"RM {current_balance:,.2f}")
    m2.metric("💸 Modal Dikeluarkan", f"RM {total_invested:,.2f}")
    m3.metric("📈 Untung Bersih (Interest)", f"RM {untung_bersih:,.2f}", f"{roi:.1f}%")
    
    df = pd.DataFrame({
        "Tahun": data_tahun,
        "Nilai Portfolio (RM)": data_nilai,
        "Modal Asal (RM)": data_modal
    })
    df = df.set_index("Tahun")
    
    st.write("### 📉 Graf Pertumbuhan Aset")
    st.line_chart(df, color=["#00CC96", "#EF553B"])
    
    with st.expander("Lihat Jadual Terperinci Tahunan"):
        st.dataframe(df)
