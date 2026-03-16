import streamlit as st
import yfinance as yf
import pandas as pd
import time
import datetime
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Strategic War Room", layout="wide")
OWNER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- DATA ENGINE ---
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
if 'missile_stats' not in st.session_state: st.session_state.missile_stats = None

# --- HEADER ---
st.title("🛰️ GLOBAL STRATEGIC & ECONOMIC COMMAND CENTER")
st.markdown(f"**Lead Analyst:** {OWNER_NAME} | **Focus:** Malaysia Macro-Risk Assessment")
st.divider()

# --- SIDEBAR: REAL-TIME FEED ---
oil, gold, status = get_live_data()
cur_oil = round(oil * st.session_state.oil_mult, 2)
st.sidebar.header("📡 LIVE TELEMETRY")
st.sidebar.metric("BRENT CRUDE", f"${cur_oil}", f"{round(st.session_state.oil_mult*100-100, 1)}% Shock")
st.sidebar.metric("GOLD OUNCE", f"${gold}")
st.sidebar.divider()
st.sidebar.write("**Global Threat Level:**")
st.sidebar.error("DEFCON 2" if st.session_state.oil_mult > 1.2 else "DEFCON 3")

# --- TOP SECTION: MILITARY BALANCE ---
st.subheader("⚔️ Regional Military Power Balance")
a1, a2, a3 = st.columns(3)
with a1:
    st.write("**🇮🇷 IRAN (Offense)**")
    st.progress(0.85)
    st.caption("Ballistic Missiles: 3,000+ | Strategic Depth: High")
with a2:
    st.write("**🇺🇸 US 5TH FLEET**")
    st.progress(0.95)
    st.caption("Carrier Groups: 2 | Tomahawk Capacity: 800+")
with a3:
    st.write("**🇮🇱 ISRAEL (Defense)**")
    st.progress(0.90)
    st.caption("Interception Rate: 94% | Nuclear Capability: Undisclosed")

# --- INTERACTIVE TRIGGER CONSOLE ---
st.divider()
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("🕹️ Tactical Trigger Console")
    b1, b2, b3 = st.columns(3)
    if b1.button("⚡ Cyber Escalation"):
        st.session_state.oil_mult = 1.10
        st.session_state.logs.append("Cyber-warfare detected. Global banking systems on alert.")
    if b2.button("🚧 Hormuz Blockade"):
        st.session_state.oil_mult = 1.45
        st.session_state.logs.append("Strait of Hormuz blocked. Global supply chain collapse.")
    if b3.button("🚀 Pre-emptive Strike"):
        st.session_state.oil_mult = 1.25
        launched = random.randint(200, 500)
        st.session_state.logs.append(f"Full-scale missile barrage. {launched} units launched.")

with c2:
    st.subheader("📜 Intelligence Feed")
    for log in reversed(st.session_state.logs):
        st.write(f"› {log}")

# --- NEW SECTION: MALAYSIA DEEP IMPACT ANALYSIS ---
st.divider()
st.header("🇲🇾 Malaysia National Risk Assessment")
st.info(f"Report ID: MY-STRIKE-{datetime.datetime.now().strftime('%Y%m%d')}")

# Calculating Simulated Economic Data
myr_base = 4.72
sim_myr = round(myr_base + (st.session_state.oil_mult - 1), 2)
inflation_rate = round(2.5 + (st.session_state.oil_mult - 1) * 20, 1)
debt_burden = "High" if sim_myr > 4.80 else "Stable"

r1, r2, r3 = st.columns(3)
r1.metric("USD/MYR Exchange", f"RM {sim_myr}", f"{round(sim_myr-myr_base, 2)} vs Base")
r2.metric("Projected Inflation (CPI)", f"{inflation_rate}%", "Supply Shock")
r3.metric("RON95 Price (w/o Subsidy)", f"RM {round(2.05 * st.session_state.oil_mult, 2)}", "Fiscal Strain")

# DEEP ANALYSIS TABLE
st.subheader("📊 Sectoral & Structural Risk Analysis")
impact_data = {
    "Domain": ["Sovereign Debt", "Food Security", "Semiconductor Industry", "Aviation & Tourism", "Oil & Gas (Petronas)"],
    "Direct Effect": [
        "Higher cost to service external debt.",
        "Imported inflation on wheat & fertilizer.",
        "Supply chain delay for E&E exports.",
        "Increased jet fuel costs & route diversions.",
        "Increased revenue but higher subsidy burden."
    ],
    "Risk Level": ["CRITICAL" if sim_myr > 4.85 else "MODERATE", "HIGH", "MODERATE", "HIGH", "STABLE"]
}
st.table(pd.DataFrame(impact_data))

# INDUSTRY WINNERS & LOSERS
w1, w2 = st.columns(2)
with w1:
    st.success("📈 Likely Beneficiaries: Oil & Gas Service Providers, Defense Contractors, Gold Miners.")
with w2:
    st.error("📉 Likely Vulnerable: Airlines, Consumer Goods, Construction (Material costs), Manufacturing.")

st.divider()
st.caption(f"© 2024 Strategic Research Portfolio | Lead Analyst: {OWNER_NAME} | Source: Yahoo Finance & Macro-logic Engine")
