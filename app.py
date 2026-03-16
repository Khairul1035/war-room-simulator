import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import re

# ==============================================================================
# 1. SETUP & OWNERSHIP
# ==============================================================================
st.set_page_config(page_title="GLOBAL STRATEGIC COMMAND", layout="wide")
RESEARCHER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# ==============================================================================
# 2. CUSTOM CSS (MODERN CORPORATE)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important; color: white; }
[data-testid="stSidebar"] * { color: white !important; }
div[data-testid="stMetric"] { background: white; border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.stButton>button { width: 100%; border-radius: 8px; font-weight: 600; border: 1px solid #CBD5E1; }
.stButton>button:hover { border-color: #2563EB; color: #2563EB; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. HELPERS & PDF ENGINE
# ==============================================================================
def clean_text(text):
    """Remove non-Latin-1 characters like emojis to prevent PDF errors"""
    if not text: return ""
    return re.sub(r'[^\x00-\x7F]+', '', str(text))

class StrategicPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", 'B', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "CONFIDENTIAL STRATEGIC REPORT - LEVEL 4 ACCESS", 0, 0, 'R')
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", 'I', 8)
        self.cell(0, 10, f"Page {self.page_no()} | Analysis by {RESEARCHER_NAME}", 0, 0, 'C')

def create_comprehensive_pdf(researcher, scenario, risk, oil, gold, fx, debt, df_risk, logs):
    pdf = StrategicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", 'B', 18)
    pdf.set_text_color(200, 0, 0)
    pdf.cell(0, 15, "NATIONAL STRATEGIC ANALYSIS REPORT", ln=True, align='C')
    pdf.set_font("Helvetica", '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, f"Lead Analyst: {clean_text(researcher)}", ln=True, align='C')
    pdf.cell(0, 5, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(10)

    # Executive Summary
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, " 1. EXECUTIVE SUMMARY", ln=True, fill=True)
    pdf.set_font("Helvetica", '', 10)
    pdf.ln(2)
    pdf.cell(0, 7, f"Active Scenario: {clean_text(scenario)}", ln=True)
    pdf.cell(0, 7, f"Risk Posture: {clean_text(risk)}", ln=True)
    pdf.cell(0, 7, f"Projected Brent Oil: USD {oil:,.2f}", ln=True)
    pdf.cell(0, 7, f"USD/MYR Exchange: RM {fx:,.4f}", ln=True)
    pdf.cell(0, 7, f"National Debt Exposure: RM {debt/1e12:.3f} Trillion", ln=True)
    pdf.ln(8)

    # State Risk Table
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, " 2. STATE-LEVEL RESOURCE RISK INVENTORY", ln=True, fill=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", 'B', 9)
    col_w = [50, 75, 30, 35]
    pdf.cell(col_w[0], 8, "Location", 1, 0, 'C', True)
    pdf.cell(col_w[1], 8, "Resource Domain", 1, 0, 'C', True)
    pdf.cell(col_w[2], 8, "Priority", 1, 0, 'C', True)
    pdf.cell(col_w[3], 8, "Stress Score", 1, 1, 'C', True)
    
    pdf.set_font("Helvetica", '', 8)
    for _, row in df_risk.iterrows():
        pdf.cell(col_w[0], 7, clean_text(row['State / Territory']), 1)
        pdf.cell(col_w[1], 7, clean_text(row['Strategic Domain']), 1)
        pdf.cell(col_w[2], 7, clean_text(row['Priority']), 1, 0, 'C')
        pdf.cell(col_w[3], 7, str(round(row['Stress Score'], 2)), 1, 1, 'C')
    pdf.ln(10)

    # Logs
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, " 3. INTELLIGENCE & COMMAND LOGS", ln=True, fill=True)
    pdf.set_font("Helvetica", '', 9)
    pdf.ln(2)
    for log in logs:
        pdf.multi_cell(0, 6, f"- {clean_text(log)}", border='B')
    
    return pdf.output()

# ==============================================================================
# 4. DATA ENGINE (REAL-TIME)
# ==============================================================================
@st.cache_data(ttl=300)
def get_market_data():
    try:
        oil = yf.Ticker("BZ=F").history(period="1mo")["Close"].dropna()
        gold = yf.Ticker("GC=F").history(period="1mo")["Close"].dropna()
        fx = yf.Ticker("MYR=X").history(period="1mo")["Close"].dropna()
        return {"oil": oil.iloc[-1], "gold": gold.iloc[-1], "fx": fx.iloc[-1], "oil_s": oil, "gold_s": gold, "fx_s": fx}
    except:
        return {"oil": 85.20, "gold": 5042.10, "fx": 4.72, "oil_s": pd.Series([85]*10), "gold_s": pd.Series([5040]*10), "fx_s": pd.Series([4.72]*10)}

def build_malaysia_data(mult):
    data = [
        ("W.P. Kuala Lumpur", "Financial Hub", "Tier 1", 3.139, 101.686),
        ("W.P. Putrajaya", "Governance HQ", "Tier 1", 2.926, 101.696),
        ("W.P. Labuan", "Offshore Finance & O&G", "Tier 2", 5.283, 115.230),
        ("Selangor", "Logistics & Industry", "Tier 1", 3.073, 101.518),
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
    df = pd.DataFrame(data, columns=["State / Territory", "Strategic Domain", "Priority", "lat", "lon"])
    df["Stress Score"] = df["Priority"].map({"Tier 1": 85, "Tier 2": 70, "Tier 3": 55}) * mult
    return df

# ==============================================================================
# 5. SESSION STATE & UI
# ==============================================================================
if "logs" not in st.session_state: st.session_state.logs = ["Command Center Online"]
if "oil_mult" not in st.session_state: st.session_state.oil_mult = 1.0
if "scenario" not in st.session_state: st.session_state.scenario = "Normal Baseline"
if "page" not in st.session_state: st.session_state.page = "Executive Dashboard"

# Load Data
snap = get_market_data()
oil_adj = round(snap["oil"] * st.session_state.oil_mult, 2)
fx_adj = round(snap["fx"] + (st.session_state.oil_mult - 1.0), 4)
debt_val = 1.525e12 + ((st.session_state.oil_mult - 1.0) * 85e9)
risk_lvl = "CRITICAL" if st.session_state.oil_mult >= 1.35 else "WATCH" if st.session_state.oil_mult >= 1.15 else "STABLE"
df_risk = build_malaysia_data(st.session_state.oil_mult)

# --- SIDEBAR ---
with st.sidebar:
    st.header("🛰️ STRATEGIC INTEL")
    st.write(f"Researcher: **{RESEARCHER_NAME}**")
    st.divider()
    st.metric("FEDERAL DEBT", f"RM {debt_val/1e12:.3f}T", f"{st.session_state.oil_mult*100-100:+.1f}% Impact")
    st.divider()
    st.session_state.page = st.radio("Navigation", ["Executive Dashboard", "Risk Page", "Command Logs"])
    st.divider()
    scen = st.selectbox("Strategic Scenario", ["Normal Baseline", "Cyber Disruption", "Hormuz Blockade", "Pre-Emptive Strike"])
    if st.button("Apply Parameters"):
        map_scen = {"Normal Baseline": 1.0, "Cyber Disruption": 1.15, "Hormuz Blockade": 1.45, "Pre-Emptive Strike": 1.25}
        st.session_state.oil_mult = map_scen[scen]
        st.session_state.scenario = scen
        st.session_state.logs.append(f"SCENARIO: {scen} activated.")
    
    st.divider()
    # PDF DOWNLOAD BUTTON
    try:
        report_data = create_comprehensive_pdf(RESEARCHER_NAME, st.session_state.scenario, risk_lvl, oil_adj, snap['gold'], fx_adj, debt_val, df_risk, st.session_state.logs)
        st.download_button("📄 DOWNLOAD FULL REPORT", data=report_data, file_name=f"Strategic_Report_{st.session_state.scenario}.pdf", mime="application/pdf")
    except Exception as e:
        st.error(f"PDF Error: {str(e)}")

# --- MAIN CONTENT ---
st.title("Strategic Outlook Dashboard: Malaysia")
st.caption(f"Director: {RESEARCHER_NAME} | Last Sync: {datetime.datetime.now().strftime('%H:%M')}")

# Metrics Row
cols = st.columns(4)
cols[0].metric("Brent Crude Oil", f"${oil_adj}", f"{(st.session_state.oil_mult-1)*100:+.1f}%")
cols[1].metric("Gold Price", f"${snap['gold']:.2f}", "Safe Haven")
cols[2].metric("USD/MYR Rate", f"RM {fx_adj}", "Risk Shock")
cols[3].metric("Strategic Risk", risk_lvl)

if st.session_state.page == "Executive Dashboard":
    st.subheader("Market Dynamics & Trends")
    c = st.columns(3)
    def plot(series, title, m=1.0):
        fig = go.Figure(go.Scatter(x=series.index, y=series.values*m, mode="lines", fill="tozeroy", line=dict(color="#2563EB", width=3)))
        fig.update_layout(height=220, margin=dict(l=0, r=0, t=30, b=0), title=title, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig
    c[0].plotly_chart(plot(snap["oil_s"], "Oil Price Trend", st.session_state.oil_mult), use_container_width=True)
    c[1].plotly_chart(plot(snap["gold_s"], "Gold Price Trend"), use_container_width=True)
    c[2].plotly_chart(plot(snap["fx_s"], "USD/MYR Trend"), use_container_width=True)
    
    st.info(f"Strategic Insight: The current scenario '{st.session_state.scenario}' places the federation at a {risk_lvl} risk level. Energy-dependent sectors (Tier 1) require immediate monitoring.")

elif st.session_state.page == "Risk Page":
    st.subheader("National Strategic Risk Map")
    fig = px.scatter_geo(df_risk, lat="lat", lon="lon", color="Priority", size="Stress Score", hover_name="State / Territory")
    fig.update_geos(lataxis_range=[0, 8], lonaxis_range=[98, 120], showcountries=True, countrycolor="#CBD5E1", fitbounds="locations")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Full Resource Inventory")
    st.dataframe(df_risk.drop(columns=['lat', 'lon']), use_container_width=True, hide_index=True)

elif st.session_state.page == "Command Logs":
    st.subheader("Chronological Command Activity")
    log_text = "\n".join(reversed(st.session_state.logs))
    st.code(log_text, language="bash")

st.divider()
st.caption(f"© 2026 GEOPOLITICAL RESEARCH PORTFOLIO | Researcher: {RESEARCHER_NAME}")
