import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Strategic Intelligence Terminal",
    page_icon="🛰️",
    layout="wide"
)

OWNER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# =========================
# CORPORATE / MODERN CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F5F7FA;
    color: #1F2937;
}

/* Main container spacing */
.block-container {
    padding-top: 1.4rem;
    padding-bottom: 1.4rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}

/* Sidebar */
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
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #1F4E79 !important;
    border-color: #3B82F6 !important;
    color: #FFFFFF !important;
}

/* Headings */
h1, h2, h3 {
    color: #0F172A;
    letter-spacing: -0.02em;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 14px 18px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #D1D5DB;
    background: #FFFFFF;
    color: #1F2937;
    font-weight: 600;
    padding: 0.6rem 0.9rem;
    transition: all 0.2s ease;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}
.stButton > button:hover {
    border-color: #2563EB;
    color: #2563EB;
    background: #F8FBFF;
    transform: translateY(-1px);
}

/* Custom cards */
.card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 18px 18px 14px 18px;
    box-shadow: 0 2px 12px rgba(15, 23, 42, 0.04);
    margin-bottom: 1rem;
}
.card-title {
    font-size: 0.86rem;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.8rem;
}
.card-subtitle {
    color: #64748B;
    font-size: 0.92rem;
    margin-top: -0.25rem;
    margin-bottom: 1rem;
}

/* Section title */
.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #334155;
    margin-bottom: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* Status pills */
.pill {
    display: inline-block;
    padding: 0.28rem 0.65rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    line-height: 1;
}
.pill-stable {
    background: #ECFDF3;
    color: #166534;
    border: 1px solid #BBF7D0;
}
.pill-watch {
    background: #FFF7ED;
    color: #C2410C;
    border: 1px solid #FED7AA;
}
.pill-critical {
    background: #FEF2F2;
    color: #B91C1C;
    border: 1px solid #FECACA;
}

/* Info note */
.info-banner {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: #1D4ED8;
    padding: 0.9rem 1rem;
    border-radius: 12px;
    font-size: 0.92rem;
    margin-bottom: 1rem;
}

/* Footer */
.footer-note {
    color: #64748B;
    font-size: 0.85rem;
    text-align: center;
    padding-top: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATA ENGINE
# =========================
@st.cache_data(ttl=300)
def get_live_data():
    try:
        oil_hist = yf.Ticker("BZ=F").history(period="5d")
        gold_hist = yf.Ticker("GC=F").history(period="5d")
        fx_hist = yf.Ticker("MYR=X").history(period="5d")

        oil = float(oil_hist["Close"].dropna().iloc[-1])
        gold = float(gold_hist["Close"].dropna().iloc[-1])
        usd_myr = float(fx_hist["Close"].dropna().iloc[-1])

        oil_prev = float(oil_hist["Close"].dropna().iloc[-2]) if len(oil_hist["Close"].dropna()) > 1 else oil
        gold_prev = float(gold_hist["Close"].dropna().iloc[-2]) if len(gold_hist["Close"].dropna()) > 1 else gold
        fx_prev = float(fx_hist["Close"].dropna().iloc[-2]) if len(fx_hist["Close"].dropna()) > 1 else usd_myr

        return {
            "oil": round(oil, 2),
            "gold": round(gold, 2),
            "usd_myr": round(usd_myr, 4),
            "oil_delta": round(oil - oil_prev, 2),
            "gold_delta": round(gold - gold_prev, 2),
            "fx_delta": round(usd_myr - fx_prev, 4),
        }
    except Exception:
        return {
            "oil": 82.45,
            "gold": 2160.10,
            "usd_myr": 4.7200,
            "oil_delta": 0.15,
            "gold_delta": -3.20,
            "fx_delta": 0.0120,
        }

# =========================
# SESSION STATE
# =========================
if "logs" not in st.session_state:
    st.session_state.logs = []

if "oil_mult" not in st.session_state:
    st.session_state.oil_mult = 1.00

if "scenario_name" not in st.session_state:
    st.session_state.scenario_name = "Normal Baseline"

# =========================
# HELPERS
# =========================
def add_log(message: str):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"{timestamp} | {message}")

def set_scenario(multiplier: float, scenario_name: str):
    st.session_state.oil_mult = multiplier
    st.session_state.scenario_name = scenario_name
    add_log(f"Scenario changed: {scenario_name} | Oil multiplier set to {multiplier:.2f}x")

def reset_scenario():
    st.session_state.oil_mult = 1.00
    st.session_state.scenario_name = "Normal Baseline"
    add_log("Scenario reset to baseline conditions.")

def get_risk_label(multiplier: float):
    if multiplier >= 1.30:
        return "Critical"
    elif multiplier >= 1.10:
        return "Watch"
    return "Stable"

def get_risk_pill(multiplier: float):
    if multiplier >= 1.30:
        return '<span class="pill pill-critical">Critical</span>'
    elif multiplier >= 1.10:
        return '<span class="pill pill-watch">Watch</span>'
    return '<span class="pill pill-stable">Stable</span>'

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🛰️ Telemetry")
    st.caption("Strategic intelligence command layer")

    st.markdown(f"""
    <div class="card" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); box-shadow:none;">
        <div class="card-title" style="color:#D9E2EC;">Director</div>
        <div style="font-weight:700; font-size:1rem; color:#FFFFFF; line-height:1.4;">
            {OWNER_NAME}
        </div>
    </div>
    """, unsafe_allow_html=True)

    base_debt = 1.525e12
    current_debt = base_debt + ((st.session_state.oil_mult - 1) * 85e9)

    st.markdown("### National Debt Tracker")
    st.metric(
        "Federal Debt Exposure",
        f"RM {current_debt / 1e12:.3f}T",
        delta=f"Scenario: {st.session_state.scenario_name}",
        delta_color="normal"
    )

    st.markdown("### Emergency Protocols")
    if st.button("Activate Mobilization"):
        add_log("National mobilization protocol activated.")
    if st.button("Evacuation Order"):
        add_log("Evacuation order issued to strategic command centers.")
    if st.button("Reset Scenario"):
        reset_scenario()

# =========================
# MAIN HEADER
# =========================
now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

st.title("Strategic Intelligence Dashboard")
st.caption(f"Lead Analyst: {OWNER_NAME}  |  Session Time: {now_str}")

st.markdown(f"""
<div class="info-banner">
Current operating scenario: <strong>{st.session_state.scenario_name}</strong> &nbsp;&nbsp;|&nbsp;&nbsp;
System risk posture: {get_risk_pill(st.session_state.oil_mult)}
</div>
""", unsafe_allow_html=True)

# =========================
# TOP METRICS
# =========================
data = get_live_data()

cur_oil = round(data["oil"] * st.session_state.oil_mult, 2)
shock_pct = round((st.session_state.oil_mult - 1.0) * 100, 1)
projected_fx = round(data["usd_myr"] + (st.session_state.oil_mult - 1.0), 4)
projected_cpi = round(2.5 + (st.session_state.oil_mult - 1.0) * 15, 1)

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Brent Crude Oil",
    f"${cur_oil:,.2f}",
    f"{shock_pct:+.1f}% scenario impact"
)

m2.metric(
    "Gold (XAU/USD)",
    f"${data['gold']:,.2f}",
    f"{data['gold_delta']:+.2f} daily move",
    delta_color="normal"
)

m3.metric(
    "USD/MYR Exchange",
    f"RM {projected_fx:,.4f}",
    f"{data['fx_delta']:+.4f} market move",
    delta_color="normal"
)

m4.metric(
    "Inflation Pressure (CPI)",
    f"{projected_cpi:.1f}%",
    "Stress projection",
    delta_color="inverse"
)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# =========================
# ACTION PANELS
# =========================
left_panel, right_panel = st.columns(2)

with left_panel:
    st.markdown("""
    <div class="card">
        <div class="card-title">Intelligence Channels</div>
        <div class="card-subtitle">Secure monitoring, signal access, and command network review</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if c1.button("Decrypt Iran Assets"):
        add_log("SIGINT review initiated: Iranian strategic communication channels flagged.")
    if c2.button("Decrypt US/EU Navy"):
        add_log("Naval intelligence feed reviewed: maritime force posture updated.")
    if c3.button("Decrypt MY Intel"):
        add_log("Domestic intelligence node accessed: reserve readiness status checked.")

    st.markdown("</div>", unsafe_allow_html=True)

with right_panel:
    st.markdown("""
    <div class="card">
        <div class="card-title">Strategic Triggers</div>
        <div class="card-subtitle">Scenario simulation tools for economic and regional stress testing</div>
    """, unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)
    if t1.button("Cyber Override"):
        set_scenario(1.12, "Cyber Override")
    if t2.button("Hormuz Blockade"):
        set_scenario(1.45, "Hormuz Blockade")
    if t3.button("Strike Scenario"):
        set_scenario(1.25, "Pre-Emptive Strike")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# ANALYSIS + LOGS
# =========================
st.markdown("## Regional Resource Risk Mapping")

table_col, log_col = st.columns([1.8, 1.1])

with table_col:
    risk_label = get_risk_label(st.session_state.oil_mult)

    state_data = pd.DataFrame({
        "State / Territory": [
            "W.P. Kuala Lumpur",
            "W.P. Putrajaya",
            "Penang",
            "Sarawak",
            "Selangor",
            "Johor",
            "Kedah"
        ],
        "Strategic Domain": [
            "Finance Hub",
            "Governance HQ",
            "Semiconductors",
            "Oil & Gas",
            "Logistics",
            "Manufacturing",
            "Food Security"
        ],
        "Risk Status": [risk_label] * 7,
        "Priority": [
            "Tier 1",
            "Tier 1",
            "Tier 2",
            "Tier 1",
            "Tier 2",
            "Tier 2",
            "Tier 3"
        ]
    })

    def highlight_risk(val):
        if val == "Critical":
            return "background-color: #FEF2F2; color: #B91C1C; font-weight: 700;"
        elif val == "Watch":
            return "background-color: #FFF7ED; color: #C2410C; font-weight: 700;"
        return "background-color: #ECFDF3; color: #166534; font-weight: 700;"

    st.dataframe(
        state_data.style.applymap(highlight_risk, subset=["Risk Status"]),
        use_container_width=True,
        hide_index=True
    )

with log_col:
    st.markdown("""
    <div class="card">
        <div class="card-title">Command Logs</div>
        <div class="card-subtitle">Latest operational and simulation events</div>
    """, unsafe_allow_html=True)

    if st.session_state.logs:
        recent_logs = list(reversed(st.session_state.logs[-10:]))
        st.code("\n".join(recent_logs), language="bash")
    else:
        st.caption("Awaiting system activity...")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# ADVISORY
# =========================
if st.session_state.oil_mult >= 1.30:
    st.error(
        f"Strategic advisory: Director {OWNER_NAME.split()[0]}, high-stress scenario detected. "
        "Energy shock risk is materially elevated and requires immediate fiscal coordination."
    )
elif st.session_state.oil_mult >= 1.10:
    st.warning(
        f"Strategic advisory: Director {OWNER_NAME.split()[0]}, medium-risk scenario in progress. "
        "Currency and inflation pressures should be monitored closely."
    )
else:
    st.success(
        "Strategic advisory: baseline conditions remain stable. Monitoring continues across financial and regional indicators."
    )

# =========================
# FOOTER
# =========================
st.divider()
st.markdown(
    f"<div class='footer-note'>© 2026 Strategic Command Center | Lead Analyst: {OWNER_NAME} | Source: Real-time Financial API</div>",
    unsafe_allow_html=True
)
