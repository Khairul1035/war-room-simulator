import streamlit as st
import yfinance as yf
import pandas as pd
import time
import datetime
import random

# --- SETTINGS & OWNERSHIP ---
st.set_page_config(page_title="STRATEGIC COMMAND CENTER", layout="wide")
OWNER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- IMPROVED CSS (BETTER CONTRAST & READABILITY) ---
st.markdown("""
    <style>
    /* Background & Main Text */
    .main { background-color: #0b0f19; color: #ffffff; }
    p, span, label { color: #ffffff !important; font-weight: 400; }
    h1, h2, h3 { color: #ff3333 !important; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] { color: #00ffcc !important; font-family: 'Courier New', monospace; font-size: 2rem !important; }
    div[data-testid="stMetricDelta"] { color: #ff3333 !important; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d; }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span { color: #ffffff !important; }

    /* Buttons Styling - Tactical Look */
    .stButton>button { 
        width: 100%; 
        border-radius: 4px; 
        border: 1px solid #ff3333; 
        background-color: #21262d; 
        color: #ff3333 !important; 
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        background-color: #ff3333; 
        color: #ffffff !important; 
        box-shadow: 0 0 15px #ff3333;
    }

    /* Log Container */
    .log-box {
        background-color: #0d1117;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        color: #00ffcc;
        height: 200px;
        overflow-y: scroll;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data(ttl=300)
def get_live_data():
    try:
        oil = yf.Ticker("BZ=F").history(period="1d")['Close'].iloc[-1]
        gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        usd_myr = yf.Ticker("MYR=X").history(period="1d")['Close'].iloc[-1]
        return round(oil, 2), round(gold, 2), round(usd_myr, 2), "CONNECTED"
    except:
        return 88.40, 2180.00, 4.75, "BUFFER"

# --- SESSION STATE ---
if 'logs' not in st.session_state: st.session_state.logs = ["System initialized... Access granted."]
if 'oil_mult' not in st.session_state: st.session_state.oil_mult = 1.0
if 'protocol' not in st.session_state: st.session_state.protocol = "STANDBY"

# --- HEADER ---
st.markdown(f"<h1 style='text-align: center;'>🛰️ GLOBAL COMMAND & CONTROL CENTER</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00ffcc !important;'>DIRECTOR: {OWNER_NAME} | SECURITY: TOP SECRET | CLEARANCE: LEVEL 4</p>", unsafe_allow_html=True)

# --- SIDEBAR: GLOBAL TELEMETRY ---
oil, gold, usd_myr, status = get_live_data()
cur_oil = round(oil * st.session_state.oil_mult, 2)
st.sidebar.title("📡 TELEMETRY")
st.sidebar.metric("BRENT CRUDE OIL", f"${cur_oil}", f"{round(st.session_state.oil_mult*100-100, 1)}% Shock")
st.sidebar.metric("GOLD OUNCE", f"${gold}")
st.sidebar.metric("USD/MYR EXCHANGE", f"RM {round(usd_myr + (st.session_state.oil_mult-1),2)}")
st.sidebar.divider()

# --- NATIONAL DEBT TRACKER ---
base_debt = 1.5e12 
current_debt = base_debt + ((st.session_state.oil_mult - 1) * 85e9)
st.sidebar.subheader("🏦 NATIONAL DEBT")
st.sidebar.error(f"RM {current_debt/1e12:.4f} TRILLION")

# --- EMERGENCY PROTOCOLS ---
st.sidebar.divider()
if st.sidebar.button("⚔️ ACTIVATE MOBILIZATION"):
    st.session_state.protocol = "MOBILIZATION"
    st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] PROTOCOL: Armed Forces on standby.")
if st.sidebar.button("☢️ EVACUATION ORDER"):
    st.session_state.protocol = "EVACUATION"
    st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] PROTOCOL: Evacuating Putrajaya HQ.")

# --- INTEL DECRYPTION (FIXED LOGIC) ---
st.subheader("🔓 Intelligence Decryption Portal")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("DECRYPT: IRAN ASSETS"):
        st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] INTEL: Thermal spikes at Isfahan missile site.")
with c2:
    if st.button("DECRYPT: US/EU NAVY"):
        st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] INTEL: US Carrier Lincoln enters Strait of Hormuz.")
with c3:
    if st.button("DECRYPT: MY INTEL"):
        st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] INTEL: MKN detecting cyber probes on Putrajaya grid.")

# --- TACTICAL TRIGGERS ---
st.divider()
st.subheader("🕹️ Strategic Crisis Triggers")
t1, t2, t3 = st.columns(3)
if t1.button("⚡ EXECUTE CYBER OVERRIDE"):
    st.session_state.oil_mult = 1.15
    st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] ACTION: Cyber-attack successful. Iran C2 offline.")
if t2.button("🚧 BLOCKADE HORMUZ"):
    st.session_state.oil_mult = 1.50
    st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] ACTION: Hormuz blocked. Global oil shock active.")
if t3.button("🚀 PRE-EMPTIVE STRIKE"):
    st.session_state.oil_mult = 1.30
    st.session_state.logs.append(f"[{datetime.datetime.now().strftime('%H:%M')}] ACTION: Kinetic strike on enrichment facility.")

# --- DYNAMIC MAPPING ---
st.divider()
st.subheader("📍 National Strategic Resource & Risk Mapping")
if st.session_state.protocol != "STANDBY":
    st.error(f"⚠️ ACTIVE PROTOCOL: {st.session_state.protocol}")

state_data = {
    "Region / State": [
        "W.P. Kuala Lumpur", "W.P. Putrajaya", "W.P. Labuan", "Selangor", "Penang", 
        "Johor", "Sarawak", "Sabah", "Terengganu", "Kedah", "Perak", "Pahang", 
        "Melaka", "Negeri Sembilan", "Kelantan", "Perlis"
    ],
    "Key Resource": [
        "Financial Hub / Capital", "Governance HQ", "Offshore Finance / O&G", 
        "Industry & Logistics", "Global Semiconductors", "Ports / O&G Hub", 
        "Energy / O&G Export", "Palm Oil / O&G", "Petroleum Export", 
        "Rice (Food Security)", "Minerals / Industry", "Bauxite / Timber", 
        "Refineries / Tourism", "Aerospace / Tech", "Agriculture", "Border Trade"
    ]
}

df = pd.DataFrame(state_data)

def calculate_risk(row):
    m = st.session_state.oil_mult
    state = row["Region / State"]
    if m > 1.4:
        if state in ["W.P. Kuala Lumpur", "W.P. Putrajaya", "Penang", "Selangor", "Johor"]:
            return "🔴 CRITICAL"
        return "🟠 HIGH"
    elif m > 1.1:
        if state in ["Penang", "Sarawak", "Kedah", "W.P. Labuan"]:
            return "🟠 HIGH"
        return "🟡 MODERATE"
    else:
        return "🟢 STABLE"

df["Status"] = df.apply(calculate_risk, axis=1)
st.table(df) # Guna table untuk readability yang lebih baik

# --- AI & LOGS ---
st.divider()
a1, a2 = st.columns([1, 2])
with a1:
    st.subheader("🤖 AI ADVISORY")
    if st.session_state.oil_mult > 1.4:
        st.error(f"DIRECTOR {OWNER_NAME.split()[0]}: Financial collapse risk in KL. National debt surging. Initiate energy rationing.")
    elif st.session_state.oil_mult > 1.1:
        st.warning("ADVISORY: Penang E&E supply chain under strain. Ringgit pressure increasing.")
    else:
        st.success("STATUS: Strategic Federation stable. No immediate territorial threats.")

with a2:
    st.subheader("📜 COMMAND LOG (LATEST)")
    # Paparkan log dalam format yang lebih bersih
    for log in reversed(st.session_state.logs[-8:]):
        st.code(log, language="bash")

st.caption(f"© 2026 GEOPOLITICAL COMMAND | ANALYST: {OWNER_NAME} | DATA: LIVE FINANCIAL API")
