import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import re

# =========================
# 1. PAGE CONFIG
# =========================
st.set_page_config(page_title="Strategic Outlook Dashboard", layout="wide")
RESEARCHER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# =========================
# 2. HELPERS
# =========================
def clean_text(text):
    """Membuang emoji dan aksara bukan Latin-1 supaya PDF tidak error"""
    if not text: return ""
    # Membuang emoji/simbol khas
    return re.sub(r'[^\x00-\x7F]+', '', str(text))

@st.cache_data(ttl=300)
def get_market_data():
    try:
        oil = yf.Ticker("BZ=F").history(period="1mo")["Close"].dropna()
        gold = yf.Ticker("GC=F").history(period="1mo")["Close"].dropna()
        fx = yf.Ticker("MYR=X").history(period="1mo")["Close"].dropna()
        return {"oil": oil.iloc[-1], "gold": gold.iloc[-1], "fx": fx.iloc[-1], "oil_s": oil, "gold_s": gold, "fx_s": fx}
    except:
        return {"oil": 85.0, "gold": 5040.0, "fx": 4.72, "oil_s": pd.Series([85]*10), "gold_s": pd.Series([5040]*10), "fx_s": pd.Series([4.72]*10)}

def build_malaysia_data(mult):
    data = [
        ("W.P. Kuala Lumpur", "Financial Hub", "Tier 1", 3.139, 101.686),
        ("W.P. Putrajaya", "Governance HQ", "Tier 1", 2.926, 101.696),
        ("W.P. Labuan", "Offshore Finance & O&G", "Tier 2", 5.283, 115.230),
        ("Selangor", "Industry & Logistics", "Tier 1", 3.073, 101.518),
        ("Pulau Pinang", "Semiconductors (E&E)", "Tier 1", 5.414, 100.328),
        ("Johor", "Manufacturing & Port", "Tier 2", 1.485, 103.761),
        ("Sarawak", "Energy & O&G Export", "Tier 1", 1.553, 110.359),
        ("Sabah", "Maritime & O&G", "Tier 2", 5.978, 116.075),
        ("Terengganu", "Petrochemical & O&G", "Tier 2", 5.311, 103.132),
        ("Kedah", "Food Security (Paddy)", "Tier 3", 6.118, 100.368),
        ("Perak", "Minerals & Industry", "Tier 2", 4.592, 101.090),
        ("Pahang", "Natural Resources", "Tier 2", 3.812, 103.325),
        ("Negeri Sembilan", "Industry & Aerospace", "Tier 3", 2.725, 101.9424),
        ("Melaka", "Maritime & Tourism", "Tier 3", 2.189, 102.250),
        ("Kelantan", "Agriculture & Border", "Tier 3", 6.125, 102.238),
        ("Perlis", "Agriculture & Border", "Tier 3", 6.444, 100.204)
    ]
    df = pd.DataFrame(data, columns=["Location", "Domain", "Priority", "lat", "lon"])
    df["Status"] = "CRITICAL" if mult >= 1.35 else "WATCH" if mult >= 1.15 else "STABLE"
    df["Stress"] = df["Priority"].map({"Tier 1": 85, "Tier 2": 70, "Tier 3": 55}) * mult
    return df

# =========================
# 3. PDF ENGINE (REPAIRED)
# =========================
def create_comprehensive_pdf(researcher, scenario, risk, oil, gold, fx, debt, df_risk, logs):
    pdf = FPDF()
    pdf.add_page()
    
    # Clean text inputs
    researcher = clean_text(researcher)
    scenario = clean_text(scenario)
    risk = clean_text(risk)

    # Header
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(190, 10, "NATIONAL STRATEGIC ANALYSIS REPORT", ln=True, align='C')
    pdf.set_font("Helvetica", '', 10)
    pdf.cell(190, 10, f"Researcher: {researcher} | Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(10)

    # Section 1: Executive Summary
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(190, 10, " 1. EXECUTIVE SUMMARY", ln=True, fill=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.cell(0, 8, f"Selected Scenario: {scenario}", ln=True)
    pdf.cell(0, 8, f"Global Risk Posture: {risk}", ln=True)
    pdf.cell(0, 8, f"- Projected Brent Oil: USD {oil:,.2f}", ln=True)
    pdf.cell(0, 8, f"- USD/MYR Exchange: RM {fx:,.4f}", ln=True)
    pdf.cell(0, 8, f"- National Debt Exposure: RM {debt/1e12:.3f}T", ln=True)
    pdf.ln(5)

    # Section 2: Detailed State Risk Table
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(190, 10, " 2. STATE-LEVEL STRATEGIC RISK INVENTORY", ln=True, fill=True)
    pdf.set_font("Helvetica", 'B', 9)
    # Table Header
    pdf.cell(50, 8, "Location", 1)
    pdf.cell(70, 8, "Strategic Domain", 1)
    pdf.cell(30, 8, "Priority", 1)
    pdf.cell(40, 8, "Stress Score", 1, ln=True)
    
    # Table Rows
    pdf.set_font("Helvetica", '', 8)
    for _, row in df_risk.iterrows():
        pdf.cell(50, 7, clean_text(row['Location']), 1)
        pdf.cell(70, 7, clean_text(row['Domain']), 1)
        pdf.cell(30, 7, clean_text(row['Priority']), 1)
        pdf.cell(40, 7, str(round(row['Stress'], 2)), 1, ln=True)
    pdf.ln(5)

    # Section 3: Intelligence Logs
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(190, 10, " 3. RECENT COMMAND LOGS", ln=True, fill=True)
    pdf.set_font("Helvetica", '', 9)
    for log in logs[-15:]: 
        pdf.multi_cell(0, 6, f"- {clean_text(log)}")
    
    return pdf.output()

# =========================
# 4. APP LOGIC
# =========================
if "logs" not in st.session_state: st.session_state.logs = ["System Online"]
if "oil_mult" not in st.session_state: st.session_state.oil_mult = 1.0
if "scenario_name" not in st.session_state: st.session_state.scenario_name = "Normal Baseline"
if "selected_page" not in st.session_state: st.session_state.selected_page = "Executive Dashboard"

snap = get_market_data()
oil_adj = round(snap["oil"] * st.session_state.oil_mult, 2)
fx_adj = round(snap["fx"] + (st.session_state.oil_mult - 1.0), 4)
debt_val = 1.525e12 + ((st.session_state.oil_mult - 1.0) * 85e9)
risk_status = "CRITICAL" if st.session_state.oil_mult >= 1.35 else "WATCH" if st.session_state.oil_mult >= 1.15 else "STABLE"
df_risk = build_malaysia_data(st.session_state.oil_mult)

with st.sidebar:
    st.title("🛰️ COMMAND")
    st.write(f"Researcher: \n**{RESEARCHER_NAME}**")
    st.divider()
    st.metric("DEBT EXPOSURE", f"RM {debt_val/1e12:.3f}T")
    
    st.divider()
    st.session_state.selected_page = st.radio("Navigation", ["Executive Dashboard", "Risk Page"])
    
    st.divider()
    scen = st.selectbox("Scenario", ["Normal Baseline", "Cyber Disruption", "Trade Route Stress", "Hormuz Blockade", "Pre-Emptive Strike"])
    if st.button("Apply Changes"):
        mapping = {"Normal Baseline": 1.0, "Cyber Disruption": 1.12, "Trade Route Stress": 1.22, "Hormuz Blockade": 1.45, "Pre-Emptive Strike": 1.25}
        st.session_state.scenario_name = scen
        st.session_state.oil_mult = mapping[scen]
        st.session_state.logs.append(f"Scenario {scen} activated.")

    st.divider()
    # DOWNLOAD BUTTON (REPAIRED)
    try:
        report_data = create_comprehensive_pdf(
            RESEARCHER_NAME, st.session_state.scenario_name, risk_status, 
            oil_adj, snap['gold'], fx_adj, debt_val, df_risk, st.session_state.logs
        )
        st.download_button(
            label="📄 DOWNLOAD FULL REPORT (PDF)", 
            data=report_data, 
            file_name=f"Strategic_Report_{datetime.datetime.now().strftime('%Y%m%d')}.pdf", 
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"PDF Engine Error: {str(e)}")

# --- UI MAIN ---
st.title("Strategic Outlook Dashboard")
cols = st.columns(4)
cols[0].metric("Brent Oil", f"${oil_adj}")
cols[1].metric("Gold Price", f"${snap['gold']:.2f}")
cols[2].metric("USD/MYR", f"RM {fx_adj}")
cols[3].metric("Risk Level", risk_status)

if st.session_state.selected_page == "Executive Dashboard":
    st.subheader("Market Analytics")
    c = st.columns(3)
    def line(series, title, m=1.0):
        fig = go.Figure(go.Scatter(x=series.index, y=series.values*m, mode="lines", fill="tozeroy", line=dict(color="#2563EB", width=3)))
        fig.update_layout(height=220, margin=dict(l=0, r=0, t=30, b=0), title=title)
        return fig
    c[0].plotly_chart(line(snap["oil_s"], "Oil Trend", st.session_state.oil_mult), use_container_width=True)
    c[1].plotly_chart(line(snap["gold_s"], "Gold Trend"), use_container_width=True)
    c[2].plotly_chart(line(snap["fx_s"], "FX Trend"), use_container_width=True)

elif st.session_state.selected_page == "Risk Page":
    st.subheader("State-Level Risk Mapping")
    fig = px.scatter_geo(df_risk, lat="lat", lon="lon", color="Status", size="Stress", hover_name="Location")
    fig.update_geos(lataxis_range=[0, 8], lonaxis_range=[99, 119], fitbounds="locations")
    st.plotly_chart(fig, use_container_width=True)
    st.table(df_risk.drop(columns=["lat", "lon"]))

st.divider()
st.caption(f"© 2026 Dashboard by {RESEARCHER_NAME}")
