import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF

# ==============================================================================
# 1. PAGE CONFIGURATION & OWNERSHIP
# ==============================================================================
st.set_page_config(
    page_title="Malaysia Strategic Outlook Dashboard",
    page_icon="📊",
    layout="wide"
)

RESEARCHER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# ==============================================================================
# 2. MODERN CORPORATE CSS
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F8FAFC; color: #1E293B; }
div[data-testid="stMetric"] { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 15px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important; }
[data-testid="stSidebar"] * { color: #F1F5F9 !important; }
.policy-box { background: #FFFFFF; border-left: 5px solid #2563EB; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-top: 20px; }
.footer-note { color: #64748B; font-size: 0.85rem; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. SESSION STATE
# ==============================================================================
if "logs" not in st.session_state: st.session_state.logs = []
if "oil_mult" not in st.session_state: st.session_state.oil_mult = 1.00
if "scenario_name" not in st.session_state: st.session_state.scenario_name = "Normal Baseline"
if "selected_page" not in st.session_state: st.session_state.selected_page = "Executive Dashboard"

# ==============================================================================
# 4. DATA ENGINES & HELPERS
# ==============================================================================
@st.cache_data(ttl=300)
def get_market_data():
    try:
        oil = yf.Ticker("BZ=F").history(period="1mo")["Close"].dropna()
        gold = yf.Ticker("GC=F").history(period="1mo")["Close"].dropna()
        fx = yf.Ticker("MYR=X").history(period="1mo")["Close"].dropna()
        return {"oil_now": oil.iloc[-1], "gold_now": gold.iloc[-1], "fx_now": fx.iloc[-1], "oil_series": oil, "gold_series": gold, "fx_series": fx}
    except:
        return {"oil_now": 85.0, "gold_now": 5040.0, "fx_now": 4.72, "oil_series": pd.Series([85]*10), "gold_series": pd.Series([5040]*10), "fx_series": pd.Series([4.72]*10)}

def get_risk_label(mult):
    if mult >= 1.35: return "CRITICAL"
    elif mult >= 1.15: return "WATCH"
    return "STABLE"

def build_full_malaysia_data(mult):
    label = get_risk_label(mult)
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
    df = pd.DataFrame(data, columns=["State / Territory", "Strategic Domain", "Priority", "lat", "lon"])
    df["Risk Status"] = label
    df["Stress Score"] = df["Priority"].map({"Tier 1": 85, "Tier 2": 70, "Tier 3": 55}) * mult
    return df

# PDF Generation Function - FIXED FOR BYTES SUPPORT
def create_pdf(researcher, scenario, risk, oil, gold, fx, debt):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "Strategic Outlook Report: Malaysia", ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(190, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Researcher: {researcher}", ln=True)
    pdf.cell(0, 10, f"Operating Scenario: {scenario}", ln=True)
    pdf.cell(0, 10, f"Risk Posture: {risk}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "Strategic Metrics:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 10, f"- Brent Crude Oil: USD {oil:,.2f}", ln=True)
    pdf.cell(0, 10, f"- Gold Price: USD {gold:,.2f}", ln=True)
    pdf.cell(0, 10, f"- USD/MYR Rate: RM {fx:,.4f}", ln=True)
    pdf.cell(0, 10, f"- Federal Debt Exposure: RM {debt/1e12:.3f}T", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "Policy Insight:", ln=True)
    pdf.set_font("Arial", 'I', 11)
    insight = "Higher energy costs and currency volatility suggest immediate surveillance of national supply chains. Strategic reserves and fiscal buffers should be monitored closely."
    pdf.multi_cell(0, 10, insight)
    
    # Return as bytes instead of string to fix Streamlit Error
    return bytes(pdf.output())

# ==============================================================================
# 5. SIDEBAR & LOGIC
# ==============================================================================
snap = get_market_data()
oil_adj = round(snap["oil_now"] * st.session_state.oil_mult, 2)
fx_adj = round(snap["fx_now"] + (st.session_state.oil_mult - 1.0), 4)
debt_val = 1.525e12 + ((st.session_state.oil_mult - 1.0) * 85e9)
risk_status = get_risk_label(st.session_state.oil_mult)

with st.sidebar:
    st.markdown(f"### Lead Researcher\n**{RESEARCHER_NAME}**")
    st.divider()
    st.markdown(f"## RM {debt_val/1e12:.3f}T")
    st.caption("Federal Debt Exposure")
    
    st.divider()
    st.session_state.selected_page = st.radio("Navigation", ["Executive Dashboard", "Risk Page", "Operations Page"])
    
    st.divider()
    scen = st.selectbox("Strategic Scenario", ["Normal Baseline", "Cyber Disruption", "Trade Route Stress", "Hormuz Blockade", "Pre-Emptive Strike"])
    if st.button("Apply Scenario"):
        mapping = {"Normal Baseline": 1.0, "Cyber Disruption": 1.12, "Trade Route Stress": 1.22, "Hormuz Blockade": 1.45, "Pre-Emptive Strike": 1.25}
        st.session_state.scenario_name = scen
        st.session_state.oil_mult = mapping[scen]

    st.divider()
    # PDF DOWNLOAD LOGIC - FIXED
    try:
        pdf_bytes = create_pdf(RESEARCHER_NAME, st.session_state.scenario_name, risk_status, oil_adj, snap['gold_now'], fx_adj, debt_val)
        st.download_button(
            label="📄 Download PDF Report", 
            data=pdf_bytes, 
            file_name=f"Strategic_Report_{st.session_state.scenario_name}.pdf", 
            mime="application/pdf"
        )
    except Exception as e:
        st.error("Error generating PDF. Please ensure all data is loaded.")

# ==============================================================================
# 6. MAIN INTERFACE
# ==============================================================================
st.title("Malaysia Strategic Outlook Dashboard")
st.caption(f"Last Sync: {datetime.datetime.now().strftime('%H:%M')} | Data: Real-Time via Financial APIs")

# Metrics
m = st.columns(4)
m[0].metric("Brent Oil", f"${oil_adj}", f"{(st.session_state.oil_mult-1)*100:.1f}%")
m[1].metric("Gold Price", f"${snap['gold_now']:.2f}", "Live")
m[2].metric("USD/MYR", f"RM {fx_adj}", "Risk Adjusted")
m[3].metric("Inflation (Proj)", f"{round(2.5 + (st.session_state.oil_mult-1)*15, 1)}%", "CPI Pressure")

# PAGE: EXECUTIVE
if st.session_state.selected_page == "Executive Dashboard":
    st.subheader("Market Trend Analysis")
    c = st.columns(3)
    def line(series, title, m=1.0):
        fig = go.Figure(go.Scatter(x=series.index, y=series.values*m, mode="lines", fill="tozeroy", line=dict(color="#2563EB", width=3)))
        fig.update_layout(height=200, margin=dict(l=0, r=0, t=30, b=0), title=title, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        fig.update_xaxes(visible=False); fig.update_yaxes(gridcolor="#E2E8F0")
        return fig
    c[0].plotly_chart(line(snap["oil_series"], "Oil Trend", st.session_state.oil_mult), use_container_width=True)
    c[1].plotly_chart(line(snap["gold_series"], "Gold Trend"), use_container_width=True)
    c[2].plotly_chart(line(snap["fx_series"], "FX Trend"), use_container_width=True)
    
    st.markdown(f"""
    <div class="policy-box">
        <h4>Strategic Insight</h4>
        The current scenario <b>{st.session_state.scenario_name}</b> suggests a risk posture of <b style="color:{'red' if risk_status=='CRITICAL' else '#2563EB'}">{risk_status}</b>. 
        Fiscal pressure on the federal debt (RM {debt_val/1e12:.3f}T) requires immediate surveillance.
    </div>
    """, unsafe_allow_html=True)

# PAGE: RISK
elif st.session_state.selected_page == "Risk Page":
    st.subheader("National Strategic Risk Map")
    df = build_full_malaysia_data(st.session_state.oil_mult)
    fig = px.scatter_geo(df, lat="lat", lon="lon", color="Risk Status", size="Stress Score", 
                         hover_name="State / Territory", color_discrete_map={"STABLE":"#16A34A", "WATCH":"#F59E0B", "CRITICAL":"#DC2626"})
    fig.update_geos(lataxis_range=[0, 9], lonaxis_range=[98, 121], showcountries=True, countrycolor="#CBD5E1", fitbounds="locations")
    fig.update_layout(height=550, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df.drop(columns=["lat", "lon"]), use_container_width=True, hide_index=True)

st.divider()
st.markdown(f"<div class='footer-note'>© 2026 Malaysia Strategic Outlook Dashboard | Researcher: {RESEARCHER_NAME}</div>", unsafe_allow_html=True)
