import streamlit as st
import yfinance as yf
import pandas as pd
import time
import datetime

# --- SETTINGS & OWNERSHIP ---
st.set_page_config(page_title="Strategic War Room", layout="wide")

# NAMA PEMILIK PROJEK (OWNERSHIP)
OWNER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- REAL-TIME DATA ENGINE (WITH CACHING TO PREVENT ERRORS) ---
@st.cache_data(ttl=600)
def get_live_data():
    try:
        # Menarik data sebenar dari Yahoo Finance
        oil_ticker = yf.Ticker("BZ=F")
        oil_data = oil_ticker.history(period="1d")
        gold_ticker = yf.Ticker("GC=F")
        gold_data = gold_ticker.history(period="1d")
        
        oil_price = oil_data['Close'].iloc[-1]
        gold_price = gold_data['Close'].iloc[-1]
        return round(oil_price, 2), round(gold_price, 2), "Live Connection"
    except:
        # Jika API Limit (Ralat Merah), sistem guna harga buffer supaya tidak rosak
        return 84.50, 2165.00, "Secure Offline Mode"

# --- SESSION STATE (Memory for the simulation) ---
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'oil_multiplier' not in st.session_state:
    st.session_state.oil_multiplier = 1.0

# --- HEADER SECTION ---
st.title("🔴 GLOBAL STRATEGIC CRISIS SIMULATOR")
st.markdown(f"**Lead Strategic Analyst:** {OWNER_NAME} | **System Status:** DEFCON 2")
st.divider()

# --- SIDEBAR (Real-Time Metrics) ---
oil_price, gold_price, status = get_live_data()
current_oil = round(oil_price * st.session_state.oil_multiplier, 2)

st.sidebar.header("📊 STRATEGIC DATA FEED")
st.sidebar.write(f"**Analyst:** {OWNER_NAME}")
st.sidebar.divider()
st.sidebar.metric("BRENT CRUDE OIL", f"${current_oil}", delta=f"{round(st.session_state.oil_multiplier*100-100, 1)}% Volatility")
st.sidebar.metric("GOLD (XAU/USD)", f"${gold_price}")
st.sidebar.write(f"Data Status: {status}")
st.sidebar.write(f"Sync: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- MAIN INTERACTIVE BOARD ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Interactive Command Console")
    st.info("Initiate a Strategic Trigger to simulate global repercussions.")
    
    # 3 Strategic Trigger Buttons
    c1, c2, c3 = st.columns(3)
    
    if c1.button("🔥 Scenario A: Cyber Escalation"):
        st.session_state.oil_multiplier = 1.15
        st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] Cyber-strike on Iran's electrical grid. Energy markets reacting.")
    
    if c2.button("🚧 Scenario B: Hormuz Blockade"):
        st.session_state.oil_multiplier = 1.45
        st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] Strait of Hormuz closed. Global oil transit disrupted.")
        
    if c3.button("🚀 Scenario C: Pre-emptive Strike"):
        st.session_state.oil_multiplier = 1.30
        st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] Kinetic strike on nuclear research sites. Regional mobilization active.")

    # Animation Feedback
    if st.session_state.oil_multiplier > 1.0:
        st.divider()
        st.warning("⚠️ ANALYSING STRATEGIC IMPACT...")
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)
        st.success("Impact Assessment Completed.")

with col2:
    st.subheader("Intelligence Log")
    if not st.session_state.logs:
        st.write("Awaiting operational command...")
    for log in reversed(st.session_state.logs):
        st.write(f"• {log}")

# --- MALAYSIA SPECIFIC IMPACT ---
st.divider()
st.subheader("🇲🇾 Malaysia National Security & Economic Assessment")
st.write(f"Report Prepared by Lead Analyst: **{OWNER_NAME}**")

m1, m2, m3 = st.columns(3)

# Logik kiraan harga RON95 berdasarkan kenaikan minyak dunia
ron95_price = round(2.05 * st.session_state.oil_multiplier, 2)

m1.metric("Petrol Price (RON95 Est.)", f"RM {ron95_price}", "Subsidy Pressure")
m2.metric("MYR/USD Exchange Rate", "4.81", "-0.15 Volatility")
m3.metric("Bursa Malaysia (KLCI)", "1,538", "-3.2% Impact")

st.divider()
st.caption(f"© 2024 Strategic Research Project | Lead Analyst: {OWNER_NAME} | Data Source: Yahoo Finance Real-Time API")
