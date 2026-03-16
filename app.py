import streamlit as st
import yfinance as yf
import pandas as pd
import time
import datetime
import random

# --- SETTINGS & OWNERSHIP ---
st.set_page_config(page_title="GLOBAL COMMAND CENTER", layout="wide")
OWNER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- CUSTOM CSS FOR ESPIONAGE FEEL ---
st.markdown("""
    <style>
    .main { background-color: #060606; }
    .stMetric { background-color: #111; border: 1px solid #222; padding: 10px; border-radius: 5px; box-shadow: 0 0 10px #00ff0033; }
    .stButton>button { width: 100%; border-radius: 0px; border: 1px solid #ff0000; background-color: #1a0000; color: #ff0000; font-weight: bold; }
    .stButton>button:hover { background-color: #ff0000; color: white; }
    div[data-testid="stExpander"] { background-color: #111; border: 1px solid #333; }
    </style>
    """, unsafe_allow_globals=True)

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

# --- HEADER ---
st.markdown(f"<h1 style='text-align: center; color: red; letter-spacing: 5px; margin-bottom: 0;'>🛰️ GLOBAL COMMAND & CONTROL CENTER</h1>", unsafe_allow_globals=True)
st.markdown(f"<p style='text-align: center; color: #888; margin-top: 0;'>DIRECTOR: {OWNER_NAME} | ACCESS: TOP SECRET | CLEARANCE: LEVEL 4</p>", unsafe_allow_globals=True)

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
st.sidebar.caption("Projected increase based on subsidy & currency shock.")

# --- INTEL DECRYPTION BUTTONS ---
st.subheader("🔓 Intelligence Decryption Portal")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("DECRYPT: MIDDLE EAST ASSETS"):
        st.session_state.logs.append("INTEL: Iranian missile silos in Isfahan showing increased thermal signatures.")
with c2:
    if st.button("DECRYPT: US/EU RESPONSE"):
        st.session_state.logs.append("INTEL: US B-2 Bombers on standby at Diego Garcia. EU implementing oil price cap.")
with c3:
    if st.button("DECRYPT: MALAYSIA DEFENSE"):
        st.session_state.logs.append("INTEL: ATM (Malaysian Armed Forces) increasing surveillance in South China Sea.")

# --- TACTICAL CRISIS TRIGGERS ---
st.divider()
st.subheader("🕹️ Strategic Crisis Triggers")
t1, t2, t3 = st.columns(3)
if t1.button("⚡ EXECUTE CYBER OVERRIDE"):
    st.session_state.oil_mult = 1.15
    st.session_state.logs.append("CYBER: SCADA infiltration successful. Iranian energy distribution disrupted.")
if t2.button("🚧 ACTIVATE HORMUZ BLOCKADE"):
    st.session_state.oil_mult = 1.50
    st.session_state.logs.append("BLOCKADE: Global oil transit through Hormuz halted. DEFCON 1 initiated.")
if t3.button("🚀 INITIATE PRE-EMPTIVE STRIKE"):
    st.session_state.oil_mult = 1.30
    st.session_state.logs.append("KINETIC: Aerial strike on uranium enrichment facilities confirmed.")

# --- DYNAMIC MAPPING OF ALL 16 REGIONS ---
st.divider()
st.subheader("📍 National Strategic Resource & Risk Mapping (Full Federation)")

state_data = {
    "State / Territory": [
        "W.P. Kuala Lumpur", "W.P. Putrajaya", "W.P. Labuan", "Selangor", "Penang", 
        "Johor", "Sarawak", "Sabah", "Terengganu", "Kedah", "Perak", "Pahang", 
        "Melaka", "Negeri Sembilan", "Kelantan", "Perlis"
    ],
    "Strategic Resource": [
        "National Financial Hub / Capital", "Administrative HQ / Governance", "Offshore Finance / O&G Hub", 
        "Industrial & Logistics Center", "Global Semiconductor Hub (E&E)", "Manufacturing / O&G / Port", 
        "Oil & Gas / Energy / Timber", "Palm Oil / Oil & Gas", "Oil & Gas (Export Terminal)", 
        "Paddy Production (Food Security)", "Mineral Resources / Industrial", "Bauxite / Timber / Agriculture", 
        "Energy Refineries / Tourism", "Aerospace / Manufacturing", "Mineral Deposits / Agriculture", 
        "Border Trade / Agriculture"
    ]
}

df = pd.DataFrame(state_data)

# Logik Penentuan Risiko Dinamik mengikut Multiplier
def calculate_risk(row):
    m = st.session_state.oil_mult
    state = row["State / Territory"]
    if m > 1.4: # Senario Perang Besar (DEFCON 1)
        if state in ["W.P. Kuala Lumpur", "W.P. Putrajaya", "Penang", "Selangor", "Johor"]:
            return "🔴 CRITICAL (High Priority)"
        return "🟠 HIGH RISK"
    elif m > 1.1: # Senario Ketegangan (DEFCON 2)
        if state in ["Penang", "Sarawak", "Terengganu", "Kedah"]:
            return "🟠 HIGH (Supply Chain/Energy)"
        return "🟡 MODERATE"
    else:
        return "🟢 STABLE"

df["Live Status"] = df.apply(calculate_risk, axis=1)

# Paparkan Jadual
st.dataframe(df, use_container_width=True, hide_index=True)

# --- AI CO-STRATEGIST & LOGS ---
st.divider()
a1, a2 = st.columns([1, 2])
with a1:
    st.subheader("🤖 AI CO-STRATEGIST")
    if st.session_state.oil_mult > 1.4:
        st.error(f"DIRECTOR {OWNER_NAME.split()[0]}: Total disruption detected in Putrajaya's administrative lines. Financial markets in KL in freefall. Activate emergency gold reserves.")
    elif st.session_state.oil_mult > 1.1:
        st.warning(f"ADVISORY: Risk to Kedah's food security due to fertilizer cost. Logistics in Penang/Labuan under strain.")
    else:
        st.success("STATUS: Federal Territories stable. No immediate territorial threat detected.")

with a2:
    st.subheader("📜 COMMAND LOG (LATEST)")
    for log in reversed(st.session_state.logs[-5:]): # Tunjuk 5 log terakhir
        st.text(f"» {log}")

st.divider()
st.caption(f"© 2026 STRATEGIC DATA COMMAND | OWNERSHIP: {OWNER_NAME} | REAL-TIME DATA VIA FINANCIAL API")
