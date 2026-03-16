import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Malaysia Strategic Outlook Dashboard",
    page_icon="📊",
    layout="wide"
)

RESEARCHER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# =========================
# CUSTOM CSS
# =========================
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

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1F33 0%, #102A43 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * {
    color: #D9E2EC !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background: #16324F !important;
    color: #F8FAFC !important;
    border: 1px solid #2F4F6F !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #1F4E79 !important;
    border-color: #60A5FA !important;
    color: #FFFFFF !important;
}

/* General buttons */
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

h1, h2, h3 {
    color: #0F172A;
    letter-spacing: -0.02em;
}

/* Cards */
.card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    margin-bottom: 1rem;
}
.card-title {
    font-size: 0.86rem;
    font-weight: 800;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.65rem;
}
.card-subtitle {
    color: #64748B;
    font-size: 0.93rem;
    margin-bottom: 0.85rem;
}

/* Readable debt card */
.dark-card {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #DCE3EA !important;
    border-radius: 16px !important;
    padding: 18px !important;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05) !important;
}
.dark-card .label {
    color: #64748B !important;
    font-size: 0.90rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.45rem !important;
}
.dark-card .value {
    color: #0F172A !important;
    font-size: 2.15rem !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
}
.dark-card .sub {
    margin-top: 0.6rem !important;
    display: inline-block !important;
    background: #EFF6FF !important;
    color: #1D4ED8 !important;
    border: 1px solid #BFDBFE !important;
    border-radius: 999px !important;
    padding: 0.28rem 0.65rem !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 14px 18px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
}

/* Info banner */
.info-banner {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: #1D4ED8;
    padding: 0.95rem 1rem;
    border-radius: 12px;
    font-size: 0.93rem;
    margin-bottom: 1rem;
}

/* Status chips */
.chip {
    display: inline-block;
    padding: 0.30rem 0.70rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 800;
    line-height: 1;
    border: 1px solid transparent;
    margin-right: 0.3rem;
}
.chip-stable {
    background: #ECFDF3;
    color: #166534;
    border-color: #BBF7D0;
}
.chip-watch {
    background: #FFF7ED;
    color: #C2410C;
    border-color: #FED7AA;
}
.chip-critical {
    background: #FEF2F2;
    color: #B91C1C;
    border-color: #FECACA;
}
.chip-info {
    background: #EFF6FF;
    color: #1D4ED8;
    border-color: #BFDBFE;
}

/* Footer */
.footer-note {
    color: #64748B;
    font-size: 0.85rem;
    text-align: center;
    padding-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "logs" not in st.session_state:
    st.session_state.logs = []

if "scenario_name" not in st.session_state:
    st.session_state.scenario_name = "Normal Baseline"

if "oil_mult" not in st.session_state:
    st.session_state.oil_mult = 1.00

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Executive Dashboard"

# =========================
# HELPERS
# =========================
def add_log(message: str):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"{ts} | {message}")

def set_scenario(name: str):
    mapping = {
        "Normal Baseline": 1.00,
        "Cyber Disruption": 1.12,
        "Trade Route Stress": 1.22,
        "Hormuz Blockade": 1.45,
        "Pre-Emptive Strike": 1.25,
    }
    st.session_state.scenario_name = name
    st.session_state.oil_mult = mapping[name]
    add_log(f"Scenario updated to {name} ({mapping[name]:.2f}x oil multiplier).")

def reset_scenario():
    st.session_state.scenario_name = "Normal Baseline"
    st.session_state.oil_mult = 1.00
    add_log("Scenario reset to Normal Baseline.")

def get_risk_label(multiplier: float):
    if multiplier >= 1.30:
        return "Critical"
    elif multiplier >= 1.10:
        return "Watch"
    return "Stable"

def risk_chip(label: str):
    if label == "Critical":
        return '<span class="chip chip-critical">Critical</span>'
    if label == "Watch":
        return '<span class="chip chip-watch">Watch</span>'
    return '<span class="chip chip-stable">Stable</span>'

# =========================
# DATA ENGINE
# =========================
@st.cache_data(ttl=300)
def get_market_snapshot():
    try:
        oil_hist = yf.Ticker("BZ=F").history(period="1mo")
        gold_hist = yf.Ticker("GC=F").history(period="1mo")
        fx_hist = yf.Ticker("MYR=X").history(period="1mo")

        oil_series = oil_hist["Close"].dropna()
        gold_series = gold_hist["Close"].dropna()
        fx_series = fx_hist["Close"].dropna()

        return {
            "oil_now": float(oil_series.iloc[-1]),
            "oil_prev": float(oil_series.iloc[-2]) if len(oil_series) > 1 else float(oil_series.iloc[-1]),
            "gold_now": float(gold_series.iloc[-1]),
            "gold_prev": float(gold_series.iloc[-2]) if len(gold_series) > 1 else float(gold_series.iloc[-1]),
            "fx_now": float(fx_series.iloc[-1]),
            "fx_prev": float(fx_series.iloc[-2]) if len(fx_series) > 1 else float(fx_series.iloc[-1]),
            "oil_series": oil_series,
            "gold_series": gold_series,
            "fx_series": fx_series,
        }
    except Exception:
        idx = pd.date_range(end=pd.Timestamp.today(), periods=20)
        oil_series = pd.Series(
            [81.2, 81.7, 82.0, 82.5, 82.1, 83.0, 83.5, 84.1, 83.8, 84.4,
             84.9, 85.2, 84.8, 85.0, 85.5, 86.0, 86.2, 86.5, 86.8, 87.0],
            index=idx
        )
        gold_series = pd.Series(
            [4980, 4988, 4995, 5002, 4998, 5005, 5010, 5015, 5020, 5018,
             5022, 5028, 5031, 5027, 5030, 5036, 5040, 5038, 5042, 5045],
            index=idx
        )
        fx_series = pd.Series(
            [4.20, 4.21, 4.20, 4.22, 4.23, 4.22, 4.21, 4.22, 4.23, 4.24,
             4.23, 4.22, 4.21, 4.22, 4.23, 4.24, 4.23, 4.22, 4.21, 4.20],
            index=idx
        )
        return {
            "oil_now": float(oil_series.iloc[-1]),
            "oil_prev": float(oil_series.iloc[-2]),
            "gold_now": float(gold_series.iloc[-1]),
            "gold_prev": float(gold_series.iloc[-2]),
            "fx_now": float(fx_series.iloc[-1]),
            "fx_prev": float(fx_series.iloc[-2]),
            "oil_series": oil_series,
            "gold_series": gold_series,
            "fx_series": fx_series,
        }

def build_state_risk_data(multiplier: float):
    label = get_risk_label(multiplier)

    data = [
        ("Johor", "Manufacturing & Logistics", "Tier 2"),
        ("Kedah", "Food Security & Agriculture", "Tier 3"),
        ("Kelantan", "Border Economy & Agriculture", "Tier 3"),
        ("Melaka", "Port Services & Tourism", "Tier 3"),
        ("Negeri Sembilan", "Logistics & Industry", "Tier 3"),
        ("Pahang", "Resources & Transport", "Tier 2"),
        ("Perak", "Industry & Food Systems", "Tier 2"),
        ("Perlis", "Agriculture & Border Supply", "Tier 3"),
        ("Pulau Pinang", "Semiconductors & Manufacturing", "Tier 1"),
        ("Sabah", "Ports, Energy & Food Supply", "Tier 2"),
        ("Sarawak", "Oil, Gas & Energy", "Tier 1"),
        ("Selangor", "Logistics, Finance & Industry", "Tier 1"),
        ("Terengganu", "Energy & Maritime", "Tier 2"),
        ("W.P. Kuala Lumpur", "Finance Hub", "Tier 1"),
        ("W.P. Labuan", "Offshore Finance & Energy Services", "Tier 2"),
        ("W.P. Putrajaya", "Federal Governance HQ", "Tier 1"),
    ]

    df = pd.DataFrame(data, columns=["State / Territory", "Strategic Domain", "Priority"])
    df["Risk Status"] = label
    df["Stress Score"] = df["Priority"].map({"Tier 1": 85, "Tier 2": 70, "Tier 3": 55}) * round(multiplier, 2)
    df["Stress Score"] = df["Stress Score"].round(1)
    return df

# =========================
# PLOTLY HELPERS
# =========================
def small_line_chart(series, title, multiplier=1.0):
    adjusted = pd.Series(series.values * multiplier, index=series.index)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=adjusted.index,
        y=adjusted.values,
        mode="lines",
        line=dict(width=3),
        fill="tozeroy",
        name=title
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=10, r=10, t=35, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        title=title,
        xaxis_title="",
        yaxis_title="",
        showlegend=False
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E5E7EB")
    return fig

def comparison_chart(base_oil, scenarios):
    names = list(scenarios.keys())
    values = [round(base_oil * mult, 2) for mult in scenarios.values()]
    fig = px.bar(
        x=names,
        y=values,
        labels={"x": "Scenario", "y": "Projected Brent Crude Oil (USD)"},
        text=values
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=25, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    fig.update_yaxes(gridcolor="#E5E7EB")
    return fig

# =========================
# LOAD DATA
# =========================
snapshot = get_market_snapshot()

oil_now = snapshot["oil_now"]
gold_now = snapshot["gold_now"]
fx_now = snapshot["fx_now"]

oil_delta = oil_now - snapshot["oil_prev"]
gold_delta = gold_now - snapshot["gold_prev"]
fx_delta = fx_now - snapshot["fx_prev"]

oil_adjusted = round(oil_now * st.session_state.oil_mult, 2)
fx_adjusted = round(fx_now + (st.session_state.oil_mult - 1.0), 4)
cpi_projected = round(2.5 + (st.session_state.oil_mult - 1.0) * 15, 1)

scenarios = {
    "Normal Baseline": 1.00,
    "Cyber Disruption": 1.12,
    "Trade Route Stress": 1.22,
    "Hormuz Blockade": 1.45,
    "Pre-Emptive Strike": 1.25
}

current_risk = get_risk_label(st.session_state.oil_mult)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 📡 Telemetry")
    st.caption("Public strategic monitoring interface")

    st.markdown(f"""
    <div class="card" style="background: rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08); box-shadow:none;">
        <div class="card-title" style="color:#D9E2EC;">Researcher</div>
        <div style="font-weight:800; font-size:1rem; color:#FFFFFF; line-height:1.45;">
            {RESEARCHER_NAME}
        </div>
    </div>
    """, unsafe_allow_html=True)

    base_debt = 1.525e12
    current_debt = base_debt + ((st.session_state.oil_mult - 1.0) * 85e9)

    st.markdown("### National Debt Tracker")
    st.markdown(f"""
    <div class="dark-card">
        <div class="label">Federal Debt Exposure</div>
        <div class="value">RM {current_debt / 1e12:.3f}T</div>
        <div class="sub">Scenario: {st.session_state.scenario_name}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navigation")
    page = st.radio(
        "Go to page",
        ["Executive Dashboard", "Operations Page", "Risk Page"],
        index=["Executive Dashboard", "Operations Page", "Risk Page"].index(st.session_state.selected_page),
        label_visibility="collapsed"
    )
    st.session_state.selected_page = page

    st.markdown("### Quick Scenario Control")
    scenario_pick = st.selectbox(
        "Select scenario",
        list(scenarios.keys()),
        index=list(scenarios.keys()).index(st.session_state.scenario_name)
    )

    if st.button("Apply Scenario"):
        set_scenario(scenario_pick)

    if st.button("Reset Scenario"):
        reset_scenario()

    st.markdown("### Emergency Protocols")
    if st.button("Activate Mobilization"):
        add_log("National mobilization protocol activated.")
    if st.button("Issue Advisory Notice"):
        add_log("Public advisory notice released.")
    if st.button("Update Monitoring Logs"):
        add_log("Monitoring logs refreshed for public dashboard.")

# =========================
# MAIN HEADER
# =========================
now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

st.title("Malaysia Strategic Outlook Dashboard")
st.caption(f"Researcher: {RESEARCHER_NAME} | Session Time: {now_str}")

st.markdown(
    f"""
    <div class="info-banner">
        Current operating scenario: <strong>{st.session_state.scenario_name}</strong>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        Risk posture: {risk_chip(current_risk)}
        &nbsp;&nbsp;|&nbsp;&nbsp;
        Audience mode: <span class="chip chip-info">Public-Friendly View</span>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# INTERACTIVE STATUS CHIPS
# =========================
chip_col1, chip_col2, chip_col3, chip_col4, chip_col5 = st.columns(5)
if chip_col1.button("Normal Baseline"):
    set_scenario("Normal Baseline")
if chip_col2.button("Cyber Disruption"):
    set_scenario("Cyber Disruption")
if chip_col3.button("Trade Route Stress"):
    set_scenario("Trade Route Stress")
if chip_col4.button("Hormuz Blockade"):
    set_scenario("Hormuz Blockade")
if chip_col5.button("Pre-Emptive Strike"):
    set_scenario("Pre-Emptive Strike")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# =========================
# EXECUTIVE DASHBOARD
# =========================
if st.session_state.selected_page == "Executive Dashboard":
    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Brent Crude Oil", f"${oil_adjusted:,.2f}", f"{(st.session_state.oil_mult - 1.0) * 100:+.1f}% scenario effect")
    m2.metric("Gold (XAU/USD)", f"${gold_now:,.2f}", f"{gold_delta:+.2f} daily move", delta_color="normal")
    m3.metric("USD/MYR Exchange", f"RM {fx_adjusted:,.4f}", f"{fx_delta:+.4f} market move", delta_color="normal")
    m4.metric("Inflation Pressure (CPI)", f"{cpi_projected:.1f}%", "Projected stress", delta_color="inverse")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    chart1, chart2, chart3 = st.columns(3)
    with chart1:
        st.plotly_chart(
            small_line_chart(snapshot["oil_series"], "Brent Crude Trend", st.session_state.oil_mult),
            use_container_width=True
        )
    with chart2:
        st.plotly_chart(
            small_line_chart(snapshot["gold_series"], "Gold Trend", 1.0),
            use_container_width=True
        )
    with chart3:
        st.plotly_chart(
            small_line_chart(snapshot["fx_series"], "USD/MYR Trend", 1.0),
            use_container_width=True
        )

    st.markdown("## Scenario Comparison Panel")
    st.plotly_chart(
        comparison_chart(oil_now, scenarios),
        use_container_width=True
    )

    compare_df = pd.DataFrame({
        "Scenario": list(scenarios.keys()),
        "Oil Multiplier": list(scenarios.values()),
        "Projected Brent (USD)": [round(oil_now * v, 2) for v in scenarios.values()],
        "Projected USD/MYR": [round(fx_now + (v - 1.0), 4) for v in scenarios.values()],
        "Projected CPI (%)": [round(2.5 + (v - 1.0) * 15, 1) for v in scenarios.values()],
        "Risk Posture": [get_risk_label(v) for v in scenarios.values()]
    })
    st.dataframe(compare_df, use_container_width=True, hide_index=True)

# =========================
# OPERATIONS PAGE
# =========================
elif st.session_state.selected_page == "Operations Page":
    st.subheader("Operations and Monitoring Controls")

    left_panel, right_panel = st.columns(2)

    with left_panel:
        st.markdown("""
        <div class="card">
            <div class="card-title">Monitoring Channels</div>
            <div class="card-subtitle">Public-oriented monitoring and strategic observation tools</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        if c1.button("Regional Signals"):
            add_log("Regional signals review completed.")
        if c2.button("Trade Corridor Watch"):
            add_log("Trade corridor monitoring updated.")
        if c3.button("Domestic Readiness"):
            add_log("Domestic readiness snapshot refreshed.")

    with right_panel:
        st.markdown("""
        <div class="card">
            <div class="card-title">Scenario Controls</div>
            <div class="card-subtitle">Simulate strategic stress conditions for public briefings</div>
        </div>
        """, unsafe_allow_html=True)

        t1, t2, t3 = st.columns(3)
        if t1.button("Cyber Stress"):
            set_scenario("Cyber Disruption")
        if t2.button("Route Pressure"):
            set_scenario("Trade Route Stress")
        if t3.button("High Shock"):
            set_scenario("Hormuz Blockade")

    st.markdown("## Command Logs")
    if st.session_state.logs:
        st.code("\n".join(reversed(st.session_state.logs[-15:])), language="bash")
    else:
        st.caption("Awaiting system activity...")

# =========================
# RISK PAGE
# =========================
elif st.session_state.selected_page == "Risk Page":
    st.subheader("Malaysia Regional Risk Mapping")

    risk_df = build_state_risk_data(st.session_state.oil_mult)

    filter_col1, filter_col2 = st.columns([1.1, 1.1])
    with filter_col1:
        selected_priority = st.multiselect(
            "Filter by priority",
            options=sorted(risk_df["Priority"].unique().tolist()),
            default=sorted(risk_df["Priority"].unique().tolist())
        )
    with filter_col2:
        selected_risk = st.multiselect(
            "Filter by risk status",
            options=sorted(risk_df["Risk Status"].unique().tolist()),
            default=sorted(risk_df["Risk Status"].unique().tolist())
        )

    filtered_df = risk_df[
        risk_df["Priority"].isin(selected_priority) &
        risk_df["Risk Status"].isin(selected_risk)
    ].copy()

    def style_risk(val):
        if val == "Critical":
            return "background-color: #FEF2F2; color: #B91C1C; font-weight: 700;"
        elif val == "Watch":
            return "background-color: #FFF7ED; color: #C2410C; font-weight: 700;"
        return "background-color: #ECFDF3; color: #166534; font-weight: 700;"

    st.dataframe(
        filtered_df.style.applymap(style_risk, subset=["Risk Status"]),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("## State Stress Score Overview")
    stress_fig = px.bar(
        filtered_df.sort_values("Stress Score", ascending=False),
        x="State / Territory",
        y="Stress Score",
        color="Priority",
        text="Stress Score"
    )
    stress_fig.update_traces(textposition="outside")
    stress_fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=20, b=30),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    stress_fig.update_yaxes(gridcolor="#E5E7EB")
    st.plotly_chart(stress_fig, use_container_width=True)

# =========================
# ADVISORY
# =========================
st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

if st.session_state.oil_mult >= 1.30:
    st.error(
        "Public advisory: high-stress scenario detected. Energy shock risk is elevated and may affect fiscal pressure, inflation, and regional supply resilience."
    )
elif st.session_state.oil_mult >= 1.10:
    st.warning(
        "Public advisory: moderate scenario pressure detected. Currency and inflation trends should be monitored closely."
    )
else:
    st.success(
        "Public advisory: baseline conditions remain stable. Monitoring continues across key national indicators."
    )

# =========================
# FOOTER
# =========================
st.divider()
st.markdown(
    f"<div class='footer-note'>© 2026 Malaysia Strategic Outlook Dashboard | Researcher: {RESEARCHER_NAME} | Source: Real-time Financial API</div>",
    unsafe_allow_html=True
)
