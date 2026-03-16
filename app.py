import streamlit as st
import yfinance as yf
import pandas as pd
import time
import datetime
import random

# --- SETTINGS & OWNERSHIP ---
st.set_page_config(page_title="GLOBAL COMMAND CENTER", layout="wide")
OWNER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- CUSTOM CSS (BETRULKAN: unsafe_allow_html) ---
st.markdown("""
    <style>
    .main { background-color: #060606; }
    .stMetric { background-color: #111; border: 1px solid #222; padding: 10px; border-radius: 5px; box-shadow: 0 0 10px #00ff0033; }
    .stButton>button { width: 100%; border-radius: 0px; border: 1px solid #ff0000; background-color: #1a0000; color: #ff0000; font-weight: bold; }
    .stButton>button:hover { background-color: #ff0000; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data(ttl=300)
def get_live_data():
    try:
        oil = yf.Ticker("BZ=F").history(period="1d")['Close'].iloc[-1]
        gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        usd_myr = yf.Ticker("MYR=X").history(period="1d")['Close'].iloc[-1]
        return round(oil, 2), round(gold, 2), round(usd_myr, 2), "SECURE LINE ACTIVE"
    except:
        return 84.50, 2165.00, 4.73, "LOCAL BUFFER ACTIVE"

# --- SESSION STATE ---
if 'logs' not in st.session_state: st.session_state.logs = []
if 'oil_mult' not in st.session_state: st.session_state.oil_mult = 1.0
if 'protocol' not in st.session_state: st.session_state.protocol = "NORMAL"

# --- HEADER ---
st.markdown(f"<h1 style='text-align: center; color: red; letter-spacing: 5px; margin-bottom: 0;'>🛰️ GLOBAL COMMAND & CONTROL CENTER</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #888; margin-top: 0;'>DIRECTOR: {OWNER_NAME} | ACCESS: TOP SECRET | CLEARANCE: LEVEL 4</p>", unsafe_allow_html=True)

# --- SIDEBAR: GLOBAL TELEMETRY ---
oil, gold, usd_myr, status = get_live_data()
cur_oil = round(oil * st.session_state.oil_mult, 2)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2560/2560500.png", width=80)
st.sidebar.title("📡 TELEMETRY")
st.sidebar.metric("BRENT CRUDE", f"${cur_oil}", f"{round(st.session_state.oil_mult*100-100, 1)}% Shock")
st.sidebar.metric("GOLD OUNCE", f"${gold}")
st.sidebar.metric("USD/MYR (LIVE)", f"RM {usd_myr}")
st.sidebar.divider()

# --- NATIONAL DEBT TRACKER ---
base_debt = 1.5e12 
current_debt = base_debt + ((st.session_state.oil_mult - 1) * 75e9)
st.sidebar.subheader("🏦 FISCAL DEBT TRACKER")
st.sidebar.error(f"RM {current_debt/1e12:.4f} TRILLION")

# --- EMERGENCY PROTOCOL ACTIONS ---
st.sidebar.divider()
st.sidebar.subheader("🚨 EMERGENCY PROTOCOLS")
if st.sidebar.button("⚔️ NATIONAL MOBILIZATION"):
    st.session_state.protocol = "MOBILIZATION"
    st.session_state.logs.append("PROTOCOL: National Armed Forces (ATM) mobilizing to high-alert status.")
if st.sidebar.button("☢️ EVACUATION PROTOCOL"):
    st.session_state.protocol = "EVACUATION"
    st.session_state.logs.append("PROTOCOL: Strategic evacuation of Putrajaya and KL financial districts initiated.")

# --- INTEL DECRYPTION ---
st.subheader("🔓 Intelligence Decryption Portal")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("DECRYPT: IRAN ASSETS"):
        st.session_state.logs.append("INTEL: Satellite detects Kaman-22 drones deployment at Bandar Abbas.")
with c2:
    if st.button("DECRYPT: US/EU NAVY"):
        st.session_state.logs.append("INTEL: UK Royal Navy Destroyer joining US Strike Group in Gulf of Oman.")
with c3:
    if st.button("DECRYPT: MY INTEL"):
        st.session_state.logs.append("INTEL: Special Branch monitoring potential cyber-threats to Putrajaya data centers.")

# --- TACTICAL TRIGGERS ---
st.divider()
st.subheader("🕹️ Strategic Crisis Triggers")
t1, t2, t3 = st.columns(3)
if t1.button("⚡ EXECUTE CYBER OVERRIDE"):
    st.session_state.oil_mult = 1.15
    st.session_state.logs.append("CYBER: Malware injected into Iranian SCADA networks.")
if t2.button("🚧 BLOCKADE HORMUZ"):
    st.session_state.oil_mult = 1.50
    st.session_state.logs.append("BLOCKADE: Global oil transit ceased. Sovereign debt spiking.")
if t3.button("🚀 PRE-EMPTIVE STRIKE"):
    st.session_state.oil_mult = 1.30
    st.session_state.logs.append("KINETIC: Targeted strikes on missile silos in Natanz.")

# --- DYNAMIC MAPPING ---
st.divider()
st.subheader("📍 National Strategic Resource & Risk Mapping")
if st.session_state.protocol != "NORMAL":
    st.error(f"CURRENT PROTOCOL: {st.session_state.protocol} ACTIVE")

state_data = {
    "Region / State": [
        "W.P. Kuala Lumpur", "W.P. Putrajaya", "W.P. Labuan", "Selangor", "Penang", 
        "Johor", "Sarawak", "Sabah", "Terengganu", "Kedah", "Perak", "Pahang", 
        "Melaka", "Negeri Sembilan", "Kelantan", "Perlis"
    ],
    "Key Resource": [
        "Financial Hub / Capital", "Governance / Putrajaya HQ", "O&G Hub / Offshore Finance", 
        "Industry & Logistics", "Global Semiconductors (E&E)", "Ports / O&G / Industry", 
        "Energy / O&G / Timber", "Palm Oil / O&G", "O&G Export Terminal", 
        "Rice (Food Security)", "Minerals / Industry", "Timber / Bauxite", 
        "Refineries / Tourism", "Aerospace / Manufacturing", "Agriculture / Mineral", 
        "Border Trade / Agriculture"
    ]
}

df = pd.DataFrame(state_data)

def calculate_risk(row):
    m = st.session_state.oil_mult
    state = row["Region / State"]
    if m > 1.4:
        if state in ["W.P. Kuala Lumpur", "W.P. Putrajaya", "Penang", "Selangor", "Johor"]:
            return "🔴 CRITICAL"
        return "🟠 HIGH RISK"
    elif m > 1.1:
        if state in ["Penang", "Sarawak", "W.P. Labuan", "Kedah"]:
            return "🟠 HIGH"
        return "🟡 MODERATE"
    else:
        return "🟢 STABLE"

df["Strategic Risk Status"] = df.apply(calculate_risk, axis=1)
st.dataframe(df, use_container_width=True, hide_index=True)

# --- AI CO-STRATEGIST & LOGS ---
st.divider()
a1, a2 = st.columns([1, 2])
with a1:
    st.subheader("🤖 AI CO-STRATEGIST")
    if st.session_state.oil_mult > 1.4:
        st.error(f"DIRECTOR {OWNER_NAME.split()[0]}: Financial systems in KL are failing. Fuel subsidies at breaking point. Debt is RM {current_debt/1e12:.3f}T. Initiate Gold Standard backing.")
    elif st.session_state.oil_mult > 1.1:
        st.warning(f"ADVISORY: Supply chain disruption in Penang E&E. Food security risk in Kedah. Ringgit pressure increasing.")
    else:
        st.success("STATUS: Strategic Federation stable. Monitoring US/Iran missile activity.")

with a2:
    st.subheader("📜 COMMAND LOG (LATEST)")
    for log in reversed(st.session_state.logs[-5:]):
        st.text(f"» {log}")

st.caption(f"© 2026 GEOPOLITICAL WAR ROOM | ANALYST: {OWNER_NAME} | DATA: LIVE FINANCIAL API")
