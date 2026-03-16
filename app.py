import streamlit as st
import yfinance as yf
import pandas as pd
import time
import datetime
import random

# --- SETTINGS & OWNERSHIP ---
st.set_page_config(page_title="Strategic War Room", layout="wide")
OWNER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- DATA ENGINE (WITH CACHING) ---
@st.cache_data(ttl=600)
def get_live_data():
    try:
        oil = yf.Ticker("BZ=F").history(period="1d")['Close'].iloc[-1]
        gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        return round(oil, 2), round(gold, 2), "Live Connection"
    except:
        return 84.50, 2165.00, "Buffer Mode"

# --- SESSION STATE ---
if 'logs' not in st.session_state: st.session_state.logs = []
if 'oil_mult' not in st.session_state: st.session_state.oil_mult = 1.0

# --- HEADER ---
st.title("🛰️ NATIONAL STRATEGIC & DEBT CONTROL CENTER")
st.markdown(f"**Lead Analyst:** {OWNER_NAME} | **Security:** Level 4 Data Integration")
st.divider()

# --- SIDEBAR: LIVE TELEMETRY ---
oil, gold, status = get_live_data()
cur_oil = round(oil * st.session_state.oil_mult, 2)
st.sidebar.header("📡 LIVE TELEMETRY")
st.sidebar.metric("BRENT CRUDE", f"${cur_oil}", f"{round(st.session_state.oil_mult*100-100, 1)}% Shock")
st.sidebar.metric("GOLD OUNCE", f"${gold}")
st.sidebar.divider()

# --- NEW: NATIONAL DEBT TRACKER ---
st.sidebar.header("🏦 NATIONAL DEBT TRACKER")
base_debt = 1500000000000 # Anggaran RM 1.5 Trillion
sim_debt = base_debt + ((st.session_state.oil_mult - 1) * 50000000000) # RM 50B hike for every 10% shock
st.sidebar.error(f"Est. Debt: RM {sim_debt/1e12:.3f} Trillion")
st.sidebar.caption("Includes estimated subsidy leakages & currency depreciation impact.")

# --- TACTICAL TRIGGER CONSOLE ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🕹️ Crisis Trigger Console")
    b1, b2, b3 = st.columns(3)
    if b1.button("⚡ Cyber Strike"):
        st.session_state.oil_mult = 1.10
        st.session_state.logs.append("Cyber-warfare disrupts regional energy grids.")
    if b2.button("🚧 Hormuz Blockade"):
        st.session_state.oil_mult = 1.45
        st.session_state.logs.append("Strait of Hormuz CLOSED. Energy supply chain halted.")
    if b3.button("🚀 Pre-emptive Strike"):
        st.session_state.oil_mult = 1.25
        st.session_state.logs.append("Kinetic military escalation detected in the Persian Gulf.")

with col2:
    st.subheader("🤖 AI CO-STRATEGIST ALERT")
    if st.session_state.oil_mult > 1.2:
        st.error(f"**ALERT:** Lead Analyst {OWNER_NAME.split()[0]}, currency depreciation is exceeding safety limits. Immediate fiscal tightening advised.")
    elif st.session_state.oil_mult > 1.0:
        st.warning("**ADVISORY:** Monitor fuel subsidy expenditure. Risk of inflation spillover to food sector is HIGH.")
    else:
        st.success("**STATUS:** Global markets stable. Monitor geopolitical chatter.")

# --- MALAYSIA GEOGRAPHICAL & SECTORAL RISK ---
st.divider()
st.subheader("📍 State-Level Industrial Risk Mapping")
risk_data = {
    "Region/State": ["Penang & Selangor", "Sarawak & Terengganu", "Johor", "Perak & Kedah", "Kuala Lumpur"],
    "Primary Industry": ["Semiconductors (E&E)", "Oil & Gas / Energy", "Logistics & Food Processing", "Agriculture (Paddy/Rubber)", "Financial Services"],
    "Conflict Impact": ["Supply chain delay (Critical)", "High Export Revenue / High Risk Area", "Freight cost surge", "Fertilizer cost hike (Food Security)", "Currency & Market Volatility"],
    "Risk Level": ["RED", "ORANGE", "RED", "YELLOW", "RED"]
}
st.table(pd.DataFrame(risk_data))

# --- ECONOMIC DEEP DIVE ---
st.divider()
st.subheader("📊 National Fiscal Strain Analysis")
myr_base = 4.72
sim_myr = round(myr_base + (st.session_state.oil_mult - 1), 2)
ron95_cost = round(2.05 * st.session_state.oil_mult, 2)

r1, r2, r3 = st.columns(3)
r1.metric("USD/MYR Exchange", f"RM {sim_myr}", f"{round(sim_myr-myr_base, 2)}")
r2.metric("Projected Debt Hike", f"+ RM {(sim_debt-base_debt)/1e9:.1f} Billion")
r3.metric("RON95 Market Value", f"RM {ron95_cost}")

# FOOTER
st.divider()
st.caption(f"© 2026 National Strategic Dashboard | Ownership: {OWNER_NAME} | OSINT & Financial API Integration")
