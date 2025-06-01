import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
import plotly.express as px
import json

# ========== INTRO PAGE ================
if "page_state" not in st.session_state:
    st.session_state.page_state = "intro"

if st.session_state.page_state == "intro":
    st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'SF Pro Display', 'Segoe UI', Helvetica, Arial, sans-serif;
        color: #e5e5e7;
        background: #19191c;
    }
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700 !important;
        color: #fff !important;
        letter-spacing: -0.02em;
    }
    </style>
    <div style="height:86vh;display:flex;flex-direction:column;justify-content:center;align-items:center;">
        <h1 style='font-size:3.3rem; font-weight:900; margin-bottom:0.6rem; background:linear-gradient(85deg,#f7f6fc,#5b4be7 75%,#50d3fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-1.8px;'>🌏 Pacific Trade Analytics Dashboard</h1>
        <div style='font-size:1.22rem; color:#d6d6ef; margin-bottom:36px; max-width:670px; text-align:center;'>
            This dashboard provides a comprehensive, interactive view of Pacific Island merchandise trade, featuring detailed annual data on imports and exports by country, partner, and commodity group. With advanced filtering and visual analytics, users can explore trends, identify opportunities and risks, and support informed policy and investment decisions across the region.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Premium Centered Button (real Streamlit button)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <style>
        .stButton>button {
            font-size:1.35rem !important;
            font-weight:700 !important;
            padding: 22px 0px !important;
            background: linear-gradient(90deg, #29294c 20%, #6c61f6 100%) !important;
            border-radius: 20px !important;
            color: #fff !important;
            border:none !important;
            box-shadow:0 6px 36px #4645ca20 !important;
            margin-bottom:30px !important;
            margin-top: 5px;
            width: 100%;
            max-width: 450px;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #a996fd 0%, #5143d9 100%) !important;
            color: #fff !important;
            box-shadow: 0 8px 32px #8879fc70 !important;
            transform: scale(1.04) translateY(-2px);
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("Start Dashboard →"):
            st.session_state.page_state = "main"
            st.rerun()
    st.stop()

# ============ PREMIUM CSS STYLING (ADD THIS BEFORE YOUR DASHBOARD) ==============
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'SF Pro Display', 'Segoe UI', Helvetica, Arial, sans-serif;
    color: #e5e5e7;
    background: #19191c;
}
h1, h2, h3, h4, h5, h6 {
    font-weight: 700 !important;
    color: #fff !important;
    letter-spacing: -0.02em;
}
.stApp {
    background: radial-gradient(ellipse 120% 100% at 50% 10%, #22222a 60%, #18181c 100%);
}
section[data-testid="stSidebar"] {
    background: linear-gradient(125deg, #252535 80%, #21212b 100%);
    border-radius: 20px 0 0 20px;
    padding: 32px 16px 32px 16px;
    box-shadow: 6px 0 24px 0 #0d0d1420;
    min-width: 320px;
}
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 {
    color: #fff !important;
}
div[data-testid="stSidebarUserContent"] {
    padding-top: 32px !important;
}
.stSelectbox, .stSelectbox label, .stSelectbox div {
    font-size: 1.12rem !important;
}
.stSelectbox [data-baseweb="select"] > div {
    border-radius: 16px !important;
}
.st-bf, .st-bk {
    background: #242432 !important;
    border-radius: 16px !important;
    border: none !important;
}
.st-emotion-cache-13k62yr, .main, .stApp main {
    padding-top: 40px !important;
}
.st-bf, .st-bk, .st-b8, .st-eg {
    box-shadow: 0 4px 48px 0 #17171b40, 0 1.5px 8px 0 #25253a20;
}
.stButton button, .stDownloadButton button {
    background: linear-gradient(90deg, #29294c 20%, #6c61f6 100%);
    color: #fff !important;
    font-weight: 700;
    font-size: 1.04rem;
    border-radius: 15px;
    padding: 0.6rem 2.2rem;
    border: none;
    box-shadow: 0 4px 16px #4e4ecb20;
    margin-bottom: 10px;
    transition: 0.25s;
}
.stButton button:hover, .stDownloadButton button:hover {
    background: linear-gradient(90deg, #a996fd 0%, #5143d9 100%);
    color: #fff;
    transform: scale(1.03) translateY(-2px);
    box-shadow: 0 8px 32px #8879fc70;
}
.stExpander {
    border-radius: 22px;
    background: rgba(31,31,43,0.97) !important;
    border: 1.5px solid #29294920;
    box-shadow: 0 2px 22px 0 #3c3c563a;
    margin-top: 20px;
}
.stExpanderHeader {
    font-weight: 700;
    color: #aaa !important;
    font-size: 1.13rem;
}
.stDataFrame {
    background: #232337;
    border-radius: 20px;
    color: #fafafc;
    box-shadow: 0 2px 10px #24244420;
}
div[data-testid="stVerticalBlock"] > div > div > div:has(.stPlotlyChart), div[data-testid="stPlotlyChart"] {
    background: #232336e0;
    border-radius: 28px;
    margin: 16px 0 16px 0;
    box-shadow: 0 4px 32px #32325232;
    padding: 14px 30px 18px 30px;
    transition: box-shadow 0.18s;
}
div[data-testid="stPlotlyChart"]:hover {
    box-shadow: 0 8px 44px #8b86fd51;
}
.stMarkdown > div {
    color: #ccc;
    font-size: 1.08rem;
}
h2, .stMarkdown h2, .stMarkdown > h2 {
    background: linear-gradient(90deg, #d7d7ef 10%, #7669e6 55%, #bb5efd 100%);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent !important;
    -webkit-text-fill-color: transparent;
}
.stApp small, .stMarkdown small {
    color: #b2b2c0 !important;
    font-size: 0.93em;
}
.stPlotlyChart text, .stPlotlyChart .legend, .stPlotlyChart .tick text {
    font-family: 'SF Pro Display', 'Segoe UI', Helvetica, Arial, sans-serif !important;
    color: #eee !important;
}
g.legend text {
    fill: #e6e6ef !important;
}
div[data-testid="stVerticalBlock"] > div > div > div:has(.stPlotlyChart) {
    backdrop-filter: blur(2.5px);
    background: linear-gradient(115deg, #1a1834e0 70%, #302d45d0 100%);
}
.stDataFrame tr:hover td {
    background: #312b58 !important;
    color: #fff !important;
    transition: 0.19s;
}
::-webkit-scrollbar {
    width: 10px; background: #2c2c39;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(90deg, #313155 50%, #6e69ec 100%);
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# ============= APPLE-LIKE TITLE ============
st.markdown("""
<h1 style='font-size:2.8rem; font-weight:900; margin-bottom:0.5rem; background:linear-gradient(85deg,#f7f6fc,#5b4be7 75%,#50d3fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-1.8px;'>🌏 Pacific Trade Geo-Globe</h1>
""", unsafe_allow_html=True)

# ============= AI INSIGHT FUNCTION: KOMA BUKAN DASH =============
def get_ai_insight(filtered, label, by, value, filter_country, filter_flow, filter_commodity, top_n=3):
    country_txt = (filter_country if filter_country != "All" else "all Pacific Island countries")
    flow_txt = (filter_flow if filter_flow else "all trade flows")
    commodity_txt = (filter_commodity if filter_commodity and filter_commodity != "All" else "all commodities")
    if filtered.empty:
        return "<span style='color:#bbb'><i>No data available to analyze for this selection. Consider expanding your filter for broader insights, or check for data quality issues.</i></span>"
    if label == "map":
        if filter_flow == "Import":
            return (
                f"This interactive map reveals the leading sources of imports for {country_txt} within {commodity_txt}, offering critical intelligence for both policymakers and supply chain managers. By identifying which countries supply the highest import values, the map can uncover over-dependence on specific partners, which presents a strategic vulnerability if geopolitical shifts or natural disruptions occur. Stakeholders are encouraged to monitor these concentrations and explore new supplier relationships or diversify sourcing strategies. Governments may use this data to design incentives for local production of critical imports or negotiate new trade agreements that reduce risk exposure."
            )
        elif filter_flow == "Total Export" or filter_flow == "Domestic Export":
            return (
                f"The map illustrates primary export destinations for {country_txt} across {commodity_txt}. Business leaders and trade officials can use these visualizations to identify growth markets, spot regions with untapped potential, and understand where revenue is concentrated. When exports cluster in a few countries, there is a risk of demand shocks if market access is lost. Proactive stakeholders may consider developing promotional campaigns or adapting products for emerging markets. This evidence can inform diplomatic missions, support negotiation priorities, and drive efforts to increase competitiveness in new markets."
            )
        elif filter_flow == "Trade Balance":
            return (
                f"This map shows the trade surplus and deficit patterns of {country_txt} with each partner. Persistent deficits may reveal underlying weaknesses in competitiveness, reliance on foreign goods, or barriers to local industry development. Conversely, consistent surpluses may signal strong sectors that could attract further investment or technological innovation. Policymakers can use these insights to target industrial policy, review trade agreements, or design sector-specific support to balance trade outcomes. Economic development agencies and foreign investors should monitor these patterns to identify strategic partnerships or interventions."
            )
        else:
            return (
                f"This map delivers a high-level overview of trade engagement for {country_txt}, empowering users to spot partner concentrations, overlooked regions, or unexpected gaps. It provides actionable intelligence for risk analysis, partner selection, and strategic prioritization."
            )
    elif label == "bar-partner":
        top = (
            filtered.groupby(by)[value]
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
        )
        if filter_flow == "Import":
            if not top.empty:
                main_sources = ", ".join([f"{idx} ({val:,.2f} USD)" for idx, val in top.items()])
                return (
                    f"The most significant import partners for {country_txt} in {commodity_txt} are {main_sources}. Businesses and government planners should recognize the risk of supply disruptions if these partners experience political unrest, logistical issues, or regulatory changes. Companies can use this information to evaluate supplier diversity and identify opportunities for alternative sourcing. Policy recommendations include bilateral trade negotiations, supply chain incentives, or targeted investment in domestic industries to replace high-risk imports."
                )
        elif filter_flow == "Total Export" or filter_flow == "Domestic Export":
            if not top.empty:
                main_dest = ", ".join([f"{idx} ({val:,.2f} USD)" for idx, val in top.items()])
                return (
                    f"The top export destinations for {country_txt} in {commodity_txt} are {main_dest}. For export-oriented companies, this data highlights where marketing and sales teams should focus their attention. Trade ministries can prioritize trade missions, support market entry, and build institutional partnerships in these regions. If new export opportunities are sought, this visualization will help select pilot countries and adapt products to local preferences, expanding the export footprint beyond established partners."
                )
        elif filter_flow == "Trade Balance":
            if not top.empty:
                main_balance = ", ".join([f"{idx} ({val:,.2f} USD)" for idx, val in top.items()])
                return (
                    f"The largest trade surpluses and deficits for {country_txt} are observed with {main_balance}. For countries with persistent deficits, policy interventions such as tariff adjustments or export promotion programs may be warranted. Surplus partners may offer investment or technology transfer opportunities, suggesting potential for deeper bilateral cooperation. Firms should monitor these balances to optimize market and sourcing decisions."
                )
        else:
            if not top.empty:
                return (
                    f"This chart ranks trading partners for {country_txt}, helping stakeholders identify dominant players and spot prospects for trade expansion. Market analysts can investigate partners with modest volumes as potential targets for future engagement."
                )
        return "No major partners identified for this filter. Consider adjusting your selection or reviewing data quality."
    elif label == "bar-commodity":
        top = (
            filtered.groupby(by)[value]
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
        )
        if filter_flow == "Import":
            if not top.empty:
                key_goods = ", ".join([f"{idx} ({val:,.2f} USD)" for idx, val in top.items()])
                return (
                    f"The most imported commodities for {country_txt} are {key_goods}. Supply chain and risk managers should evaluate the strategic importance of these commodities, especially if they are essential for food security, health, or critical industries. For highly imported goods, national agencies might consider supporting local production or securing long-term contracts with reliable partners to ensure continuous supply."
                )
        elif filter_flow == "Total Export" or filter_flow == "Domestic Export":
            if not top.empty:
                main_exports = ", ".join([f"{idx} ({val:,.2f} USD)" for idx, val in top.items()])
                return (
                    f"The top export commodities for {country_txt} are {main_exports}. Industry and investment authorities can use this information to attract foreign direct investment, promote sectoral innovation, and develop export promotion strategies. For companies, these products present the greatest opportunity for value-added production or branding, while governments should focus on maintaining market access for these goods."
                )
        else:
            if not top.empty:
                return (
                    f"This visualization spotlights leading traded commodities for {country_txt}, supporting analysis of economic strengths, weaknesses, and diversification potential."
                )
        return "No dominant commodities found. This may reveal fragmentation or gaps in the trade structure."
    elif label == "line-trend":
        trend = (
            filtered.groupby(by)[value]
            .sum()
            .reset_index()
        )
        if not trend.empty and trend.shape[0] >= 2:
            y1 = trend[value].iloc[0]
            y2 = trend[value].iloc[-1]
            t1 = trend[by].iloc[0]
            t2 = trend[by].iloc[-1]
            direction = "increased" if y2 > y1 else "decreased" if y2 < y1 else "remained stable"
            pct = abs(y2-y1)/y1*100 if y1 else 0
            if filter_flow == "Import":
                return (
                    f"Between {t1} and {t2}, total imports for {country_txt} in {commodity_txt} have {direction}, changing from {y1:,.2f} USD to {y2:,.2f} USD, representing a {pct:.1f}% shift. If the import trend is rising, it may signal economic expansion, currency movements, or changes in domestic demand. Stakeholders should examine whether this increase is sustainable or due to temporary factors, and businesses might plan for inventory adjustment or renegotiation of supplier terms."
                )
            elif filter_flow == "Total Export" or filter_flow == "Domestic Export":
                return (
                    f"Export trends for {country_txt} in {commodity_txt} have {direction} from {y1:,.2f} USD in {t1} to {y2:,.2f} USD in {t2}, marking a {pct:.1f}% shift. A rising trend could indicate strong international demand or successful trade promotion, whereas declines may warrant new product development or the opening of alternative markets."
                )
            elif filter_flow == "Trade Balance":
                return (
                    f"Trade balance trends for {country_txt} moved from {y1:,.2f} USD in {t1} to {y2:,.2f} USD in {t2}, signifying a {pct:.1f}% change. Persistent deficits may trigger macroeconomic risks and policy review, while growing surpluses can attract international investment or demand for higher-value exports."
                )
            else:
                return (
                    f"The overall trend for {country_txt} in {commodity_txt} has {direction} across the selected period. Stakeholders can use these signals to optimize timing for trade negotiations, business expansion, or policy reform."
                )
        else:
            return "Not enough data for a trend. Consider expanding your date range for a richer analysis."
    elif label == "pie":
        share = (
            filtered.groupby(by)[value]
            .sum()
            .sort_values(ascending=False)
        )
        if not share.empty:
            total = share.sum()
            items = share.head(top_n)
            contributors = [f"{idx} ({(val/total*100):.1f}%)" for idx, val in items.items()]
            contributors_str = ", ".join(contributors)  # --- INI FORMAT KOMA SAJA TANPA DASH
            if filter_flow == "Import":
                return (
                    f"This pie chart identifies which countries supply the largest shares of imports for {country_txt}. Main contributors: {contributors_str}. This analysis is crucial for identifying concentration risk in supply chains and designing policies to broaden trade relationships. Decision-makers can act to reduce import dependence, develop backup suppliers, or foster domestic capabilities for critical goods."
                )
            elif filter_flow == "Total Export" or filter_flow == "Domestic Export":
                return (
                    f"This chart shows the main export markets for {country_txt}, indicating where sales and marketing efforts yield the most value. Top destinations: {contributors_str}. Companies should focus on strengthening these relationships, while government agencies might pursue mutual recognition agreements, reduce trade barriers, or sponsor export promotions in leading markets."
                )
            elif filter_flow == "Trade Balance":
                return (
                    f"The trade balance share chart highlights the most consequential bilateral relationships for {country_txt}, where surpluses or deficits are most pronounced. Leading pairs: {contributors_str}. These patterns should inform future negotiations, investment targeting, and the review of existing trade agreements."
                )
            else:
                return (
                    f"This chart provides a clear snapshot of the structure of trade for {country_txt} in {commodity_txt}, offering practical insights into diversification and resilience."
                )
        return "No significant partner shares detected. Review data or consider a broader filter."
    return "No automated insight for this chart and filter. Please adjust your filter or check the raw data for details."

# ==================== LABELS =========================
TRADE_FLOW_LABELS = {
    "M": "Import",
    "X": "Total Export",
    "X1": "Domestic Export",
    "X2": "Re-export",
    "TB": "Trade Balance"
}
COMMODITY_LABELS = {
    "I": "Live animals; animal products",
    "II": "Vegetable products",
    "III": "Animal/vegetable fats & oils; waxes",
    "IV": "Prepared foodstuffs; beverages; tobacco",
    "V": "Mineral products",
    "VI": "Chemical products",
    "VII": "Plastics, rubber",
    "VIII": "Hides, skins, leather, furskins, etc.",
    "IX": "Wood & articles of wood; cork; basketware",
    "X": "Pulp, paper, paperboard, and articles",
    "XI": "Textiles and textile articles",
    "XII": "Footwear, headgear, umbrellas, etc.",
    "XIII": "Stone, ceramics, glass",
    "XIV": "Precious stones, metals, jewelry",
    "XV": "Base metals and articles of base metal",
    "XVI": "Machinery, electrical equipment",
    "XVII": "Transport equipment (vehicles, aircraft, ships)",
    "XVIII": "Instruments (medical, musical, etc.)",
    "XIX": "Arms and ammunition",
    "XX": "Miscellaneous manufactured articles",
    "XXI": "Works of art, antiques",
    "XXII": "Others",
    "_T": "All Commodities"
}

# ================== LOAD DATA =======================
@st.cache_data(show_spinner=True)
def load_data():
    url = "https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_IMTS,4.0/all/?format=csvfilewithlabels"
    df = pd.read_csv(url, low_memory=False)
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
    df = df[df["OBS_VALUE"].notna() & (df["OBS_VALUE"] > 0)]
    return df

@st.cache_data
def load_coords():
    coords = pd.read_csv("country-coordinates-world.csv")
    coords["COUNTRY_CLEAN"] = coords["Country"].astype(str).str.strip().str.lower()
    return coords

@st.cache_data
def load_geojson():
    with open("world.geojson", "r", encoding="utf-8") as f:
        return json.load(f)

# =============== COLOR LOG MAPPING ================
def get_color(val, max_val):
    if val <= 0 or max_val <= 0:
        return [80, 80, 80]  # dark gray for "zero" trade
    norm = np.log10(val + 1) / np.log10(max_val + 1)
    cmap = plt.get_cmap("plasma")
    rgba = cmap(norm)
    return [int(255 * x) for x in rgba[:3]]

st.markdown("""
Explore Pacific trade dynamics with interactive filters, colored globe, insightful charts, and downloadable raw data.<br>
<b>Tips:</b> Hover over a country or column for details. Adjust filters to focus on specific trade flows or commodities.
""", unsafe_allow_html=True)

df = load_data()
coords = load_coords()
geojson = load_geojson()

COUNTERPART = "Counterpart area"
REF_AREA = "Pacific Island Countries and territories"
COMMODITY = "COMMODITY"
TRADE_FLOW = "TRADE_FLOW"
VALUE = "OBS_VALUE"
TIME_PERIOD = "TIME_PERIOD"

# Clean/prep
df["TRADE_FLOW_LABEL"] = df[TRADE_FLOW].map(TRADE_FLOW_LABELS).fillna(df[TRADE_FLOW])
df["COMMODITY_LABEL"] = df[COMMODITY].map(COMMODITY_LABELS).fillna(df[COMMODITY])
df["PARTNER_CLEAN"] = df[COUNTERPART].astype(str).str.strip().str.lower()
coords = coords.rename(columns={"Country": "PARTNER"})
merged = pd.merge(df, coords, left_on="PARTNER_CLEAN", right_on="COUNTRY_CLEAN", how="left")
merged["Trade_M_USD"] = merged[VALUE] / 1e6

# ============ SIDEBAR FILTERS ===============
with st.sidebar:
    st.markdown("## :mag: Filter")
    reporting_countries = ["All"] + sorted(merged[REF_AREA].dropna().unique().tolist())
    selected_country = st.selectbox("Select Reporting Country", reporting_countries)
    flows = sorted(merged["TRADE_FLOW_LABEL"].dropna().unique().tolist())
    commodities = sorted(merged["COMMODITY_LABEL"].dropna().unique().tolist())
    selected_flow = st.selectbox("Select Trade Flow", flows)
    selected_commodity = st.selectbox("Select Commodity", ["All"] + commodities)

# ============ FILTER DATA ===============
filtered = merged.copy()
if selected_country != "All":
    filtered = filtered[filtered[REF_AREA] == selected_country]
filtered = filtered[filtered["TRADE_FLOW_LABEL"] == selected_flow]
if selected_commodity != "All":
    filtered = filtered[filtered["COMMODITY_LABEL"] == selected_commodity]

# ============ GEOJSON COLOR INJECTION ===============
country_trade = (
    filtered.groupby("COUNTRY_CLEAN")["Trade_M_USD"]
    .sum()
    .reset_index()
    .rename(columns={"Trade_M_USD": "value"})
)
max_trade = country_trade["value"].max() if not country_trade.empty else 1
for feature in geojson["features"]:
    name = feature["properties"].get("ADMIN", "").strip().lower()
    match = country_trade[country_trade["COUNTRY_CLEAN"] == name]
    value = match["value"].values[0] if not match.empty else 0
    feature["properties"]["trade_value"] = f"{value:,.2f}"
    feature["properties"]["trade_value_num"] = value
    feature["properties"]["fill_color"] = get_color(value, max_trade)
    feature["properties"]["tooltip"] = f"{feature['properties'].get('ADMIN','')}: {value:,.2f} M USD" if value > 0 else f"{feature['properties'].get('ADMIN','')}: No data"

# ============ COLUMN LAYER (3D Bar) ==============
filtered_map = filtered.copy()
filtered_map = filtered_map[filtered_map["latitude"].notna() & filtered_map["longitude"].notna()]
filtered_map["latitude"] = filtered_map["latitude"].astype(float)
filtered_map["longitude"] = filtered_map["longitude"].astype(float)
filtered_map["Trade_M_USD"] = filtered_map["Trade_M_USD"].astype(float)

max_val = filtered_map["Trade_M_USD"].max() if not filtered_map.empty else 1
filtered_map["color_value"] = filtered_map["Trade_M_USD"].apply(lambda x: x / max_val if max_val > 0 else 0)

# ====== DYNAMIC AI INSIGHT: MAP ======
st.markdown("<b>Insight:</b> " + get_ai_insight(filtered, "map", None, None, selected_country, selected_flow, selected_commodity), unsafe_allow_html=True)

trade_layer = pdk.Layer(
    "ColumnLayer",
    data=filtered_map,
    get_position=["longitude", "latitude"],
    get_elevation="Trade_M_USD",
    elevation_scale=200000,
    radius=60000,
    get_fill_color="[color_value * 255, 100, 255 * (1 - color_value)]",
    pickable=True,
    auto_highlight=True,
)
geojson_layer = pdk.Layer(
    "GeoJsonLayer",
    data=geojson,
    stroked=True,
    filled=True,
    get_fill_color="properties.fill_color",
    get_line_color=[255, 255, 255],
    line_width_min_pixels=0.8,
    pickable=True,
    auto_highlight=True,
)
view = pdk.ViewState(latitude=30, longitude=10, zoom=1.5, pitch=40)
deck = pdk.Deck(
    layers=[geojson_layer, trade_layer],
    initial_view_state=view,
    map_style="mapbox://styles/mapbox/dark-v10",
    tooltip={
        "html": "<b>{ADMIN}</b><br/>Trade: {trade_value} M USD",
        "style": {"color": "white"}
    }
)
st.pydeck_chart(deck)

st.markdown("""
<div style='margin-top: -20px'>
    <h5>🌈 Legend: Estimated Trade (Million USD, Log Color)</h5>
    <div style='display: flex; gap: 10px; align-items: center'>
        <div style='width: 20px; height: 20px; background-color: #0d0887;'></div> <span>Low</span>
        <div style='width: 100px; height: 20px; background: linear-gradient(to right, #0d0887, #f0f921);'></div>
        <span>High</span>
    </div>
    <div style='margin-top:8px;color:gray;font-size:small'>Countries with no trade data colored gray.</div>
</div>
""", unsafe_allow_html=True)

# ================= CHART 1: Top 10 Trading Partners (bar) ==============
st.subheader("📊 Top 10 Trading Partners (by Value)")
filtered_top_partners = filtered[~filtered[COUNTERPART].str.lower().str.contains("all")]
st.markdown("<b>Insight:</b> " + get_ai_insight(filtered_top_partners, "bar-partner", COUNTERPART, VALUE, selected_country, selected_flow, selected_commodity), unsafe_allow_html=True)
top_partners = (
    filtered_top_partners.groupby(COUNTERPART)[VALUE]
    .sum()
    .reset_index()
    .sort_values(by=VALUE, ascending=False)
    .head(10)
)
bar = px.bar(top_partners, x=VALUE, y=COUNTERPART, orientation="h",
             title="Top 10 Partners", labels={VALUE: "Trade Value (USD)", COUNTERPART: "Partner"},
             color=VALUE, color_continuous_scale="plasma")
bar.update_layout(showlegend=False)
if not top_partners.empty:
    max_bar_val = top_partners[VALUE].max()
    bar.update_xaxes(range=[0, max_bar_val * 1.2])
bar.update_traces(hovertemplate=f"<b>%{{y}}</b><br>Trade Value: %{{x:,.2f}} USD")
st.plotly_chart(bar, use_container_width=True)

# =============== CHART 2: Komoditas Terbesar (Pareto) ===============
st.subheader("🏷️ Top Commodities Traded")
filtered_commodities = filtered[~filtered["COMMODITY_LABEL"].str.lower().str.contains("all")]
st.markdown("<b>Insight:</b> " + get_ai_insight(filtered_commodities, "bar-commodity", "COMMODITY_LABEL", VALUE, selected_country, selected_flow, selected_commodity), unsafe_allow_html=True)
top_commodities = (
    filtered_commodities.groupby("COMMODITY_LABEL")[VALUE]
    .sum()
    .reset_index()
    .sort_values(by=VALUE, ascending=False)
    .head(10)
)
commodity_chart = px.bar(top_commodities, x=VALUE, y="COMMODITY_LABEL", orientation="h",
                        labels={VALUE: "Trade Value (USD)", "COMMODITY_LABEL": "Commodity"},
                        color=VALUE, color_continuous_scale="viridis")
commodity_chart.update_layout(title="Top Commodities Traded", showlegend=False)
if not top_commodities.empty:
    max_commod_val = top_commodities[VALUE].max()
    commodity_chart.update_xaxes(range=[0, max_commod_val * 1.2])
commodity_chart.update_traces(hovertemplate=f"<b>%{{y}}</b><br>Trade Value: %{{x:,.2f}} USD")
st.plotly_chart(commodity_chart, use_container_width=True)

# =============== CHART 3: Trade Trend Over Time =====================
st.subheader("⏳ Total Trade Value Over Time")
st.markdown("<b>Insight:</b> " + get_ai_insight(filtered, "line-trend", TIME_PERIOD, VALUE, selected_country, selected_flow, selected_commodity), unsafe_allow_html=True)
if not filtered.empty:
    trend = (
        filtered.groupby(TIME_PERIOD)[VALUE]
        .sum()
        .reset_index()
    )
    trend[TIME_PERIOD] = (
        trend[TIME_PERIOD]
        .astype(str)
        .str.extract(r'(\d{4})')
    )
    trend = trend.dropna(subset=[TIME_PERIOD])
    trend[TIME_PERIOD] = trend[TIME_PERIOD].astype(int)
    trend = trend.sort_values(by=TIME_PERIOD)
    trend_chart = px.line(trend, x=TIME_PERIOD, y=VALUE, markers=True,
                          labels={TIME_PERIOD: "Year", VALUE: "Total Trade Value (USD)"})
    trend_chart.update_layout(title="Total Trade Value Over Time", showlegend=False)
    st.plotly_chart(trend_chart, use_container_width=True)
else:
    st.info("No trade data for selected filter to plot time trend.")

# =============== CHART 4: Pie Share By Partner =======================
st.subheader("🥧 Trade Share By Partner (Top 8)")
filtered_pie_partners = filtered[~filtered[COUNTERPART].str.lower().str.contains("all")]
st.markdown("<b>Insight:</b> " + get_ai_insight(filtered_pie_partners, "pie", COUNTERPART, VALUE, selected_country, selected_flow, selected_commodity), unsafe_allow_html=True)
if not filtered_pie_partners.empty:
    share = (
        filtered_pie_partners.groupby(COUNTERPART)[VALUE]
        .sum()
        .reset_index()
        .sort_values(by=VALUE, ascending=False)
        .head(8)
    )
    others_value = filtered_pie_partners[~filtered_pie_partners[COUNTERPART].isin(share[COUNTERPART])][VALUE].sum()
    share = pd.concat([share, pd.DataFrame([{COUNTERPART: "Others", VALUE: others_value}])], ignore_index=True)
    pie_chart = px.pie(share, values=VALUE, names=COUNTERPART, title="Trade Share by Partner")
    st.plotly_chart(pie_chart, use_container_width=True)
else:
    st.info("No trade data for selected filter to plot partner share.")

# ============= RAW DATA ==============
with st.expander("📄 Show Raw Data"):
    col_names = [REF_AREA, COUNTERPART, "COMMODITY_LABEL", VALUE, TIME_PERIOD, "Trade_M_USD"]
    show_cols = [c for c in col_names if c in filtered.columns]
    st.dataframe(filtered[show_cols].reset_index(drop=True).head(100))

# ============= DOWNLOAD ==============
csv = filtered.to_csv(index=False)
st.download_button("⬇️ Download Filtered Data as CSV", csv, "filtered_trade_data.csv", "text/csv")
