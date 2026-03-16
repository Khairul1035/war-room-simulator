import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Malaysia Strategic Outlook Dashboard",
    page_icon="📊",
    layout="wide"
)

RESEARCHER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# ==============================================================================
# 2. CUSTOM CSS (Corporate & Intelligence UI)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F5F7FA;
    color: #1F2937;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.2rem;
    padding-left: 1.4rem;
    padding-right: 1.4rem;
}

/* Sidebar Dark Theme */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1F33 0%, #102A43 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * {
    color: #D9E2EC !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: #16324F !important;
    color: #F8FAFC !important;
    border: 1px solid #2F4F6F !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* General Action Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #D1D5DB;
    background: #FFFFFF;
    color: #1F2937;
    font-weight: 600;
    padding: 0.60rem 0.90rem;
    transition: all 0.2s ease;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}
.stButton > button:hover {
    border-color: #2563EB;
    color: #2563EB;
    background: #F8FBFF;
    transform: translateY(-1px);
}

/* Metrics & Cards */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 14px 18px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
}

.card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    margin-bottom: 1rem;
}

.dark-card {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #DCE3EA !important;
    border-radius: 16px !important;
    padding: 18px !important;
}

.dark-card .value {
    font-size: 2.15rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
}

.info-banner {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: #1D4ED8;
    padding: 0.95rem 1rem;
    border-radius: 12px;
    font-size: 0.93rem;
    margin-bottom: 1rem;
}

.chip {
    display: inline-block;
    padding: 0.30rem 0.70rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 800;
}
.chip-stable { background: #ECFDF3; color: #166534; }
.chip-watch { background: #FFF7ED; color: #C2410C; }
.chip-critical { background: #FEF2F2; color: #B91C1C; }

.policy-box {
    background: #FFFFFF;
    border-left: 6px solid #2563EB;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
}

.footer-note {
    color: #64748B;
    font-size: 0.85rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. SESSION STATE INITIALIZATION
# ==============================================================================
state_defaults = {
    "logs": [],
    "scenario_name": "Normal Baseline",
    "oil_mult": 1.00,
    "selected_page": "Executive Dashboard",
    "shock_oil_pct": 0,
    "shock_usd_pct": 0,
    "shock_supply": "Low"
}

for key, val in state_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ==============================================================================
# 4. HELPER FUNCTIONS & LOGIC
# ==============================================================================
def add_log(message):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"{ts} | {message}")

def set_scenario(name):
    mapping = {"Normal Baseline": 1.0, "Cyber Disruption": 1.12, "Trade Route Stress": 1.22, "Hormuz Blockade": 1.45, "Pre-Emptive Strike": 1.25}
    st.session_state.scenario_name = name
    st.session_state.oil_mult = mapping[name]
    add_log(f"Scenario updated to {name}.")

def reset_scenario():
    st.session_state.scenario_name = "Normal Baseline"
    st.session_state.oil_mult = 1.0
    st.session_state.shock_oil_pct = 0
    st.session_state.shock_usd_pct = 0
    st.session_state.shock_supply = "Low"
    add_log("System reset to Baseline.")

def get_risk_label(mult):
    if mult >= 1.30: return "Critical"
    if mult >= 1.10: return "Watch"
    return "Stable"

def risk_chip(label):
    css_class = f"chip-{'stable' if label=='Stable' else 'watch' if label=='Watch' else 'critical'}"
    return f'<span class="chip {css_class}">{label}</span>'

def run_shock_simulation(base_oil, base_fx, oil_pct, usd_pct, supply_level):
    oil_factor = 1 + (oil_pct / 100.0)
    usd_factor = 1 + (usd_pct / 100.0)
    supply_map = {"Low": 0.00, "Medium": 0.06, "High": 0.14}
    total_mult = oil_factor * (1 + supply_map[supply_level])
    
    res = {
        "oil": round(base_oil * total_mult, 2),
        "fx": round(base_fx * usd_factor + (total_mult - 1.0), 4),
        "cpi": round(2.5 + (total_mult - 1.0) * 18 + (usd_pct * 0.03), 1),
        "debt": 1.525e12 + ((total_mult - 1.0) * 85e9),
        "risk": get_risk_label(total_mult)
    }
    return res

def generate_policy_insight(scenario, risk, oil, fx, cpi, shock_mode=False):
    insights = {
        "Critical": ["High-stress macro risk environment detected.", "Energy-sensitive and import-reliant sectors at risk.", "Priority: Strengthen inflation surveillance and logistics."],
        "Watch": ["Moderate stress conditions detected.", "Rising pressure on household costs and importer sentiment.", "Priority: Maintain market watch and review supply resilience."],
        "Stable": ["Baseline environment stable.", "Manageable operating conditions.", "Priority: Continue routine monitoring."]
    }
    selected = insights[risk]
    return {"headline": selected[0], "summary": selected[1], "policy": selected[2], "note": "Simulation-driven." if shock_mode else "Dashboard conditions."}

# ==============================================================================
# 5. DATA ENGINES
# ==============================================================================
@st.cache_data(ttl=300)
def get_market_snapshot():
    try:
        oil = yf.Ticker("BZ=F").history(period="1mo")["Close"].dropna()
        gold = yf.Ticker("GC=F").history(period="1mo")["Close"].dropna()
        fx = yf.Ticker("MYR=X").history(period="1mo")["Close"].dropna()
        return {"oil_now": oil.iloc[-1], "oil_prev": oil.iloc[-2], "gold_now": gold.iloc[-1], "gold_prev": gold.iloc[-2], "fx_now": fx.iloc[-1], "fx_prev": fx.iloc[-2], "oil_series": oil, "gold_series": gold, "fx_series": fx}
    except:
        idx = pd.date_range(end=pd.Timestamp.today(), periods=10)
        s = pd.Series([85.0]*10, index=idx)
        return {"oil_now": 85.0, "oil_prev": 84.5, "gold_now": 5040.0, "gold_prev": 5035.0, "fx_now": 4.20, "fx_prev": 4.21, "oil_series": s, "gold_series": s*60, "fx_series": s/20}

def build_state_risk_data(mult):
    data = [
        ("Johor", "Logistics", "Tier 2", 1.8, 103.7), ("Kedah", "Agriculture", "Tier 3", 6.1, 100.4),
        ("Pulau Pinang", "Semiconductors", "Tier 1", 5.4, 100.3), ("Sarawak", "Energy/O&G", "Tier 1", 2.9, 113.0),
        ("Selangor", "Logistics/Finance", "Tier 1", 3.1, 101.5), ("W.P. Kuala Lumpur", "Finance", "Tier 1", 3.14, 101.6),
        ("W.P. Putrajaya", "Governance", "Tier 1", 2.93, 101.6)
    ]
    df = pd.DataFrame(data, columns=["State / Territory", "Strategic Domain", "Priority", "lat", "lon"])
    df["Risk Status"] = get_risk_label(mult)
    df["Stress Score"] = df["Priority"].map({"Tier 1": 85, "Tier 2": 70, "Tier 3": 55}) * mult
    return df

# ==============================================================================
# 6. PLOTLY VISUALS
# ==============================================================================
def small_line_chart(series, title, mult=1.0):
    fig = go.Figure(go.Scatter(x=series.index, y=series.values*mult, mode="lines", fill="tozeroy", line=dict(width=3, color='#2563EB')))
    fig.update_layout(height=180, margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", title=title, showlegend=False)
    fig.update_xaxes(visible=False); fig.update_yaxes(gridcolor="#E5E7EB")
    return fig

def malaysia_risk_map(df):
    fig = px.scatter_geo(df, lat="lat", lon="lon", color="Risk Status", size="Stress Score", hover_name="State / Territory",
                         color_discrete_map={"Stable": "#16A34A", "Watch": "#F59E0B", "Critical": "#DC2626"}, projection="natural earth")
    fig.update_geos(lataxis_range=[0, 8], lonaxis_range=[99, 120], showcountries=True, countrycolor="#CBD5E1")
    fig.update_layout(height=450, margin=dict(l=0, r=0, t=0, b=0))
    return fig

# ==============================================================================
# 7. LOAD DATA & GLOBAL VARS
# ==============================================================================
snap = get_market_snapshot()
oil_adj = round(snap["oil_now"] * st.session_state.oil_mult, 2)
fx_adj = round(snap["fx_now"] + (st.session_state.oil_mult - 1.0), 4)
cpi_proj = round(2.5 + (st.session_state.oil_mult - 1.0) * 15, 1)
debt_val = 1.525e12 + ((st.session_state.oil_mult - 1.0) * 85e9)
risk_lvl = get_risk_label(st.session_state.oil_mult)

# ==============================================================================
# 8. SIDEBAR
# ==============================================================================
with st.sidebar:
    st.markdown(f"### Researcher\n**{RESEARCHER_NAME}**")
    st.markdown(f"""<div class="dark-card"><div class="value">RM {debt_val/1e12:.3f}T</div><div class="sub">Debt Exposure</div></div>""", unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("Navigation", ["Executive Dashboard", "Operations Page", "Risk Page"])
    st.session_state.selected_page = page
    
    st.divider()
    scen = st.selectbox("Scenario Select", ["Normal Baseline", "Cyber Disruption", "Trade Route Stress", "Hormuz Blockade", "Pre-Emptive Strike"])
    if st.button("Apply"): set_scenario(scen)
    if st.button("Reset"): reset_scenario()

# ==============================================================================
# 9. MAIN CONTENT
# ==============================================================================
st.title("Malaysia Strategic Outlook Dashboard")
st.markdown(f"""<div class="info-banner">Scenario: <b>{st.session_state.scenario_name}</b> | Risk: {risk_chip(risk_lvl)}</div>""", unsafe_allow_html=True)

# Quick Access Scenario Chips
cols = st.columns(5)
names = ["Normal Baseline", "Cyber Disruption", "Trade Route Stress", "Hormuz Blockade", "Pre-Emptive Strike"]
for i, name in enumerate(names):
    if cols[i].button(name): set_scenario(name)

# --- PAGE: EXECUTIVE ---
if st.session_state.selected_page == "Executive Dashboard":
    m = st.columns(4)
    m[0].metric("Brent Oil", f"${oil_adj}", f"{(st.session_state.oil_mult-1)*100:.1f}%")
    m[1].metric("Gold", f"${snap['gold_now']:.2f}", f"{snap['gold_now']-snap['gold_prev']:.2f}")
    m[2].metric("USD/MYR", f"RM {fx_adj}", f"{snap['fx_now']-snap['fx_prev']:.3f}")
    m[3].metric("CPI (Proj)", f"{cpi_proj}%", "Inflation")

    st.markdown("### Market Trends")
    c = st.columns(3)
    c[0].plotly_chart(small_line_chart(snap["oil_series"], "Oil Trend", st.session_state.oil_mult), use_container_width=True)
    c[1].plotly_chart(small_line_chart(snap["gold_series"], "Gold Trend"), use_container_width=True)
    c[2].plotly_chart(small_line_chart(snap["fx_series"], "FX Trend"), use_container_width=True)

    ins = generate_policy_insight(st.session_state.scenario_name, risk_lvl, oil_adj, fx_adj, cpi_proj)
    st.markdown(f"""<div class="policy-box"><div class="policy-title">{ins['headline']}</div><div class="policy-text">{ins['summary']}<br><br><b>Response:</b> {ins['policy']}</div></div>""", unsafe_allow_html=True)

# --- PAGE: OPERATIONS ---
elif st.session_state.selected_page == "Operations Page":
    st.subheader("Economic Shock Simulator")
    s = st.columns(3)
    oil_s = s[0].slider("Oil Shock %", 0, 50, st.session_state.shock_oil_pct)
    usd_s = s[1].slider("USD Strength %", 0, 30, st.session_state.shock_usd_pct)
    supp_s = s[2].selectbox("Supply Chain Disruption", ["Low", "Medium", "High"])
    
    res = run_shock_simulation(snap["oil_now"], snap["fx_now"], oil_s, usd_s, supp_s)
    
    r = st.columns(4)
    r[0].metric("Sim. Oil", f"${res['oil']}")
    r[1].metric("Sim. FX", f"RM {res['fx']}")
    r[2].metric("Sim. CPI", f"{res['cpi']}%")
    r[3].metric("Sim. Debt", f"RM {res['debt']/1e12:.2f}T")

    st.markdown("### Command Logs")
    st.code("\n".join(reversed(st.session_state.logs[-10:])), language="bash")

# --- PAGE: RISK ---
elif st.session_state.selected_page == "Risk Page":
    df = build_state_risk_data(st.session_state.oil_mult)
    st.plotly_chart(malaysia_risk_map(df), use_container_width=True)
    st.dataframe(df.drop(columns=['lat', 'lon']), use_container_width=True)

# FOOTER
st.divider()
st.markdown(f"<div class='footer-note'>© 2026 Malaysia Strategic Outlook Dashboard | Researcher: {RESEARCHER_NAME}</div>", unsafe_allow_html=True)
