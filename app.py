import streamlit as st
import yfinance as yf
import pandas as pd
import time
import datetime
import random

# --- SETTINGS & OWNERSHIP ---
st.set_page_config(page_title="Strategic Intelligence Dashboard", layout="wide")
OWNER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- MODERN CORPORATE CSS (8px Spacing System & Bloomberg Palette) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
    /* Global Styles */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        background-color: #F5F7FA;
        color: #1F2937;
    }
    
    /* Sidebar Styling (Dark Corporate) */
    [data-testid="stSidebar"] {
        background-color: #0B1F33 !important;
        border-right: 1px solid #E5E7EB;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #D6E2F0 !important;
        font-size: 14px;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    /* Card System */
    .data-card {
        background-color: #FFFFFF;
        border: 1px solid #E3E8EF;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 24px;
        transition: all 0.2s ease;
    }
    .data-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    /* Metrics Styling */
    .metric-title { color: #6B7280; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .metric-value { color: #111827; font-size: 24px; font-weight: 700; margin: 4px 0; }
    .metric-delta-pos { color: #16A34A; font-size: 13px; font-weight: 500; }
    .metric-delta-neg { color: #DC2626; font-size: 13px; font-weight: 500; }

    /* Button Design (Soft Corporate) */
    .stButton>button {
        width: 100%;
        background-color: #FFFFFF;
        color: #1F2937;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #F3F4F6;
        border-color: #D1D5DB;
    }
    
    /* Primary Action Button (Blue) */
    div.stButton > button:first-child {
        border: none;
    }
    
    /* Intelligence Table */
    .stTable {
        background-color: white;
        border-radius: 8px;
        overflow: hidden;
    }

    /* Status Indicators */
    .status-active { color: #16A34A; font-size: 12px; font-weight: 600; }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data(ttl=300)
def get_live_data():
    try:
        oil = yf.Ticker("BZ=F").history(period="1d")['Close'].iloc[-1]
        gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        usd_myr = yf.Ticker("MYR=X").history(period="1d")['Close'].iloc[-1]
        return round(oil, 2), round(gold, 2), round(usd_myr, 2), "Active"
    except:
        return 88.42, 2184.10, 4.74, "Cached"

# --- SESSION STATE ---
if 'logs' not in st.session_state: st.session_state.logs = []
if 'oil_mult' not in st.session_state: st.session_state.oil_mult = 1.0
if 'protocol' not in st.session_state: st.session_state.protocol = "STANDBY"

# --- SIDEBAR (Dark Corporate) ---
with st.sidebar:
    st.markdown(f"### STRATEGIC INTEL")
    st.markdown(f"**DIRECTOR:**  \n{OWNER_NAME}")
    st.divider()
    
    # Debt Tracker in Sidebar
    base_debt = 1.5e12 
    current_debt = base_debt + ((st.session_state.oil_mult - 1) * 85e9)
    st.markdown("FEDERAL DEBT TRACKER")
    st.markdown(f"## RM {current_debt/1e12:.4f}T")
    st.caption("Includes emergency fiscal buffers.")
    
    st.divider()
    st.markdown("EMERGENCY PROTOCOLS")
    if st.button("National Mobilization"):
        st.session_state.protocol = "MOBILIZATION"
        st.session_state.logs.append(f"{datetime.datetime.now().strftime('%H:%M')} - ATM Level 1 Alert")
    if st.button("Evacuation Order"):
        st.session_state.protocol = "EVACUATION"
        st.session_state.logs.append(f"{datetime.datetime.now().strftime('%H:%M')} - Putrajaya Evacuation initiated")

# --- MAIN CONTENT ---
# Header
st.markdown(f"<h3 style='margin-bottom: 0;'>Global Strategic Intelligence Dashboard</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #6B7280; font-size: 14px;'>Lead Analyst: {OWNER_NAME} | {datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')}</p>", unsafe_allow_html=True)

# 1. TOP STRATEGIC METRICS (Horizontal Layout)
oil, gold, usd_myr, status = get_live_data()
cur_oil = round(oil * st.session_state.oil_mult, 2)
shock_val = round(st.session_state.oil_mult*100-100, 1)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""<div class="data-card">
        <div class="metric-title">Brent Crude Oil</div>
        <div class="metric-value">${cur_oil}</div>
        <div class="{'metric-delta-pos' if shock_val <= 0 else 'metric-delta-neg'}">{'+' if shock_val > 0 else ''}{shock_val}% Volatility</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class="data-card">
        <div class="metric-title">Gold (XAU/USD)</div>
        <div class="metric-value">${gold}</div>
        <div class="status-active">● Market Active</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""<div class="data-card">
        <div class="metric-title">USD/MYR Exchange</div>
        <div class="metric-value">RM {round(usd_myr + (st.session_state.oil_mult-1), 2)}</div>
        <div class="metric-delta-neg">Impacted by Risk</div>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""<div class="data-card">
        <div class="metric-title">National Inflation (CPI)</div>
        <div class="metric-value">{round(2.5 + (st.session_state.oil_mult-1)*15, 1)}%</div>
        <div class="status-active" style="color:#F59E0B">● Warning Phase</div>
    </div>""", unsafe_allow_html=True)

# 2. OPERATIONAL ACTIONS (Card-based Layout)
st.markdown("#### Strategic Operations & Intelligence")
col_actions, col_triggers = st.columns([1, 1])

with col_actions:
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px; font-weight:600; color:#4B5563;'>DECRYPTION CHANNELS</p>", unsafe_allow_html=True)
    ac1, ac2, ac3 = st.columns(3)
    if ac1.button("Decrypt Iran"): st.session_state.logs.append("SIGINT: Iran IRGC communication intercepted.")
    if ac2.button("Decrypt US Navy"): st.session_state.logs.append("OSINT: US 5th Fleet movement confirmed.")
    if ac3.button("Decrypt MY Intel"): st.session_state.logs.append("MKN: Domestic energy reserve report.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_triggers:
    st.markdown('<div class="data-card" style="border-left: 4px solid #DC2626;">', unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px; font-weight:600; color:#DC2626;'>CRISIS TRIGGERS</p>", unsafe_allow_html=True)
    tr1, tr2, tr3 = st.columns(3)
    if tr1.button("Cyber Override"): st.session_state.oil_mult = 1.12
    if tr2.button("Hormuz Blockade"): st.session_state.oil_mult = 1.45
    if tr3.button("Pre-emptive Strike"): st.session_state.oil_mult = 1.28
    st.markdown('</div>', unsafe_allow_html=True)

# 3. INTELLIGENCE TABLE & LOGS
st.markdown("#### Regional Resource Risk Mapping")
c_table, c_logs = st.columns([2, 1])

with c_table:
    state_data = {
        "State / Territory": ["W.P. Kuala Lumpur", "W.P. Putrajaya", "Penang", "Sarawak", "Selangor", "Johor", "Kedah"],
        "Strategic Domain": ["Financial Hub", "Governance", "Semiconductors", "Energy/O&G", "Logistics", "Manufacturing", "Food Security"],
        "Impact Level": ["High" if st.session_state.oil_mult > 1.2 else "Stable"] * 7
    }
    df = pd.DataFrame(state_data)
    st.table(df)

with c_logs:
    st.markdown("<p style='font-size:13px; font-weight:600; color:#4B5563;'>COMMAND LOGS</p>", unsafe_allow_html=True)
    log_content = "\n".join(reversed(st.session_state.logs[-8:]))
    st.code(log_content if log_content else "Awaiting system input...", language="bash")

# AI ADVISORY CALLOUT
if st.session_state.oil_mult > 1.1:
    st.warning(f"**AI ADVISORY:** Geopolitical risk is affecting the USD/MYR exchange rate. Current fiscal debt trajectory: RM {current_debt/1e12:.2f}T. Lead Analyst {OWNER_NAME.split()[0]} is advised to review energy subsidies.")

st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 12px; margin-top: 40px;'>Strategic Command Terminal | Powered by Live Data API | Proprietary & Confidential</p>", unsafe_allow_html=True)
