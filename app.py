import streamlit as st
import yfinance as yf
import pandas as pd
import time
import datetime

# --- SETTINGS & OWNERSHIP ---
st.set_page_config(page_title="Strategic War Room", layout="wide")
YOUR_NAME = "YOUR NAME HERE" # <--- CHANGE THIS

# --- REAL-TIME DATA ENGINE ---
def get_live_data():
    oil = yf.Ticker("BZ=F").history(period="1d")['Close'].iloc[-1]
    gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
    return round(oil, 2), round(gold, 2)

# --- SESSION STATE (The "Game" Memory) ---
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'oil_multiplier' not in st.session_state:
    st.session_state.oil_multiplier = 1.0

# --- HEADER ---
st.title("🔴 GLOBAL STRATEGIC CRISIS SIMULATOR")
st.markdown(f"**Lead Strategic Analyst:** {YOUR_NAME} | **System Status:** DEFCON 2")
st.divider()

# --- SIDEBAR (Real-Time Metrics) ---
oil_price, gold_price = get_live_data()
current_oil = round(oil_price * st.session_state.oil_multiplier, 2)

st.sidebar.header("📊 LIVE DATA FEED")
st.sidebar.metric("BRENT CRUDE OIL", f"${current_oil}", delta=f"{round(st.session_state.oil_multiplier*100-100, 1)}% Shock")
st.sidebar.metric("GOLD (XAU/USD)", f"${gold_price}")
st.sidebar.write(f"Last Sync: {datetime.datetime.now().strftime('%H:%M:%S')}")

# --- THE GAME BOARD ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Interactive Command Console")
    st.info("Select a Strategic Trigger to simulate global repercussions.")
    
    # Game Buttons
    c1, c2, c3 = st.columns(3)
    if c1.button("🔥 Scenario A: Cyber Strike"):
        st.session_state.oil_multiplier = 1.10
        st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] Cyber-attack on Iran Power Grid. Oil spikes 10%.")
    
    if c2.button("🚧 Scenario B: Hormuz Blockade"):
        st.session_state.oil_multiplier = 1.40
        st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] Strait of Hormuz Closed. Global supply chain collapse.")
        
    if c3.button("🚀 Scenario C: Pre-emptive Strike"):
        st.session_state.oil_multiplier = 1.25
        st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] Kinetic strike on Nuclear Sites. Full-scale mobilization.")

    # Animation Simulation
    st.write("---")
    if st.session_state.oil_multiplier > 1.0:
        st.warning("⚠️ CRITICAL IMPACT DETECTED")
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        st.success("Simulation Calculation Complete.")

with col2:
    st.subheader("Intelligence Log")
    for log in reversed(st.session_state.logs):
        st.write(log)

# --- MALAYSIA IMPACT SECTION ---
st.divider()
st.subheader("🇲🇾 Malaysia National Impact Assessment")
m1, m2, m3 = st.columns(3)
m1.metric("Petrol Price (RON95)", "RM2.05", "Floating Risk")
m2.metric("MYR/USD Exchange", "4.75", "-0.12")
m3.metric("Stock Market (KLCI)", "1,540", "-2.5%")

st.caption(f"Project Ownership: {YOUR_NAME} | Source: Yahoo Finance Real-time API")
