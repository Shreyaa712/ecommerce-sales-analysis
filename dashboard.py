
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# 1. PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="E-commerce Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. DESIGN SYSTEM
# =====================================================
NAVY = "#10172A"
NAVY_LIGHT = "#192440"
PURPLE = "#8575FF"
TEAL = "#36D6C3"
TEXT = "#202945"
MUTED = "#7D879E"
BG = "#F4F6FC"
WHITE = "#FFFFFF"
BORDER = "#E8EBF4"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #F4F6FC;
    color: #202945;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10172A 0%, #192440 100%);
}

[data-testid="stSidebar"] * {
    color: #F2F4FF;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #25304C;
    border-color: #3A4665;
}

[data-testid="stSidebar"] input {
    color: #FFFFFF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2.5rem;
    max-width: 1600px;
}

h1, h2, h3 {
    color: #202945;
    letter-spacing: -0.7px;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E8EBF4;
    border-radius: 16px;
    padding: 20px 20px 17px 20px;
    box-shadow: 0 5px 20px rgba(28, 39, 75, 0.045);
}

[data-testid="stMetricLabel"] {
    color: #7D879E;
    font-size: 13px;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #202945;
    font-size: 27px;
    font-weight: 800;
}

div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E8EBF4;
    border-radius: 16px;
    padding: 8px;
    box-shadow: 0 5px 20px rgba(28, 39, 75, 0.035);
}

.insight-card {
    background: #FFFFFF;
    border: 1px solid #E8EBF4;
    border-radius: 14px;
    padding: 17px 19px;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(28, 39, 75, 0.035);
}

.insight-label {
    color: #7D879E;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 7px;
}

.insight-value {
    color: #202945;
    font-size: 18px;
    font-weight: 800;
}

.insight-description {
    color: #7D879E;
    font-size: 13px;
    margin-top: 5px;
}

.section-label {
    color: #7D879E;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

div[data-testid="stCaptionContainer"] {
    color: #7D879E;
}

hr {
    border-color: #E8EBF4;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    data = pd.read_csv(
        "data/processed/online_retail_cleaned.csv"
    )

    data["InvoiceDate"] = pd.to_datetime(
        data["InvoiceDate"], errors="coerce"
    )
    data["TotalSales"] = pd.to_numeric(
        data["TotalSales"], errors="coerce"
    )
    data["Quantity"] = pd.to_numeric(
        data["Quantity"], errors="coerce"
    )

    data = data.dropna(
        subset=["InvoiceDate", "TotalSales"]
    )

    return data


try:
    original_df = load_data()
except Exception as error:
    st.error(f"Unable to load the cleaned dataset: {error}")
    st.info(
        "Check that data/processed/online_retail_cleaned.csv "
        "exists relative to the project root."
    )
    st.stop()

if original_df.empty:
    st.error("The dataset contains no usable records.")
    st.stop()


# =====================================================
# 4. SIDEBAR AND FILTERS
# =====================================================
st.sidebar.markdown(
    "<div style='font-size:34px;font-weight:800;'>◆</div>",
    unsafe_allow_html=True
)
st.sidebar.markdown("## E-commerce")
st.sidebar.markdown("### SALES INTELLIGENCE")
st.sidebar.caption("Explore your business performance")

st.sidebar.divider()
st.sidebar.markdown("#### FILTERS")

countries = sorted(
    original_df["Country"].dropna().unique().tolist()
)

selected_country = st.sidebar.selectbox(
    "🌍 Country",
    ["All Countries"] + countries
)

min_date = original_df["InvoiceDate"].min().date()
max_date = original_df["InvoiceDate"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

st.sidebar.divider()
st.sidebar.markdown("#### ABOUT THIS REPORT")
st.sidebar.caption(
    "Retail transaction analysis covering sales, "
    "products, countries and customers."
)

# Apply filters to a copy, not to the source dataset.
df = original_df.copy()

if selected_country != "All Countries":
    df = df[df["Country"] == selected_country]

if isinstance(selected_dates, (tuple, list)):
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
    elif len(selected_dates) == 1:
        start_date = end_date = selected_dates[0]
    else:
        start_date, end_date = min_date, max_date
else:
    start_date = end_date = selected_dates

df = df[
    (df["InvoiceDate"].dt.date >= start_date)
    & (df["InvoiceDate"].dt.date <= end_date)
]

if df.empty:
    st.title("Sales Intelligence")
    st.warning(
        "No records match these filters. "
        "Please choose another country or date range."
    )
    st.stop()


# =====================================================
# 5. PREPARE BUSINESS METRICS
# =====================================================
total_sales = df["TotalSales"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()

average_order_value = (
    total_sales / total_orders if total_orders else 0
)

# Explicitly identify potential cancellations/returns.
invoice_text = df["InvoiceNo"].astype(str)
cancel_mask = invoice_text.str.upper().str.startswith("C")
cancelled_invoice_count = df.loc[cancel_mask, "InvoiceNo"].nunique()

negative_sales_rows = int((df["TotalSales"] < 0).sum())

# Aggregate for charts.
monthly = (
    df.assign(Month=df["InvoiceDate"].dt.to_period("M").astype(str))
    .groupby("Month", as_index=False)["TotalSales"]
    .sum()
)

country_sales = (
    df.groupby("Country", as_index=False)["TotalSales"]
    .sum()
    .nlargest(10, "TotalSales")
    .sort_values("TotalSales")
)

product_sales = (
    df.dropna(subset=["Description"])
    .groupby("Description", as_index=False)["TotalSales"]
    .sum()
    .nlargest(10, "TotalSales")
    .sort_values("TotalSales")
)

customer_sales = (
    df.dropna(subset=["CustomerID"])
    .groupby("CustomerID", as_index=False)["TotalSales"]
    .sum()
    .nlargest(10, "TotalSales")
    .sort_values("TotalSales")
)

# Use a consistent chart theme.
def polish_chart(fig, height=330):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=18, r=18, t=65, b=22),
        font=dict(
            family="DM Sans, sans-serif",
            color=TEXT,
            size=11
        ),
        title=dict(
            font=dict(size=15, color=TEXT),
            x=0.03,
            xanchor="left"
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#EDF0F7",
        zeroline=False,
        linecolor=BORDER
    )
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        linecolor=BORDER
    )

    return fig


# =====================================================
# 6. MAIN HEADER
# =====================================================
st.markdown(
    "<div class='section-label'>BUSINESS PERFORMANCE / RETAIL ANALYTICS</div>",
    unsafe_allow_html=True
)

header_left, header_right = st.columns([3, 1])

with header_left:
    st.title("Sales Overview")
    st.caption(
        f"{start_date.strftime('%d %b %Y')} — "
        f"{end_date.strftime('%d %b %Y')}  ·  "
        f"{selected_country}"
    )

with header_right:
    st.markdown(
        f"""
        <div style="text-align:right;padding-top:25px;">
          <span style="background:#E4F8F4;color:#087F70;
          padding:9px 13px;border-radius:20px;font-size:12px;
          font-weight:700;">● DATA LOADED</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("### Performance at a glance")

k1, k2, k3, k4 = st.columns(4)

k1.metric("TOTAL SALES", f"{total_sales:,.2f}")
k2.metric("UNIQUE INVOICES", f"{total_orders:,}")
k3.metric("UNIQUE CUSTOMERS", f"{total_customers:,}")
k4.metric("AVG. SALES / INVOICE", f"{average_order_value:,.2f}")

st.caption(
    "These metrics sum the recorded TotalSales values. "
    "Returns and cancellations may affect their interpretation."
)

st.write("")


# =====================================================
# 7. SALES TREND AND COUNTRY RANKING
# =====================================================
left, right = st.columns([1.15, 1])

with left:
    fig_monthly = px.area(
        monthly,
        x="Month",
        y="TotalSales",
        title="Monthly sales trend",
        markers=True
    )

    fig_monthly.update_traces(
        line=dict(color=PURPLE, width=3),
        marker=dict(color=PURPLE, size=6),
        fillcolor="rgba(133,117,255,0.12)",
        hovertemplate="%{x}<br>Sales: %{y:,.2f}<extra></extra>"
    )

    fig_monthly = polish_chart(fig_monthly, 360)
    fig_monthly.update_layout(
        hovermode="x unified",
        xaxis_title="",
        yaxis_title="Recorded sales"
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with right:
    fig_country = px.bar(
        country_sales,
        x="TotalSales",
        y="Country",
        orientation="h",
        title="Top 10 countries",
        text="TotalSales",
        color_discrete_sequence=[PURPLE]
    )

    fig_country.update_traces(
        texttemplate="%{x:,.0f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}<br>Sales: %{x:,.2f}<extra></extra>"
    )

    fig_country = polish_chart(fig_country, 360)
    fig_country.update_layout(
        xaxis_title="Recorded sales",
        yaxis_title="",
        showlegend=False,
        margin=dict(l=20, r=80, t=40, b=20),
        yaxis=dict(automargin=True)
    )


    st.plotly_chart(
        fig_country,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# =====================================================
# 8. PRODUCT AND CUSTOMER RANKINGS
# =====================================================
left, right = st.columns(2)

with left:
    fig_product = px.bar(
        product_sales,
        x="TotalSales",
        y="Description",
        orientation="h",
        title="Top 10 products by sales",
        color_discrete_sequence=[TEAL]
    )

    fig_product.update_traces(
        hovertemplate="%{y}<br>Sales: %{x:,.2f}<extra></extra>"
    )

    fig_product = polish_chart(fig_product, 390)
    fig_product.update_layout(
        xaxis_title="Recorded sales",
        yaxis_title=""
    )

    st.plotly_chart(
        fig_product,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with right:
    customer_sales["CustomerID"] = customer_sales["CustomerID"].astype(int).astype(str) 

    fig_customer = px.bar(
        customer_sales,
        x="TotalSales",
        y="CustomerID",
        orientation="h",
        title="Top 10 customers by sales",
        color_discrete_sequence=[PURPLE]
    )

    fig_customer.update_traces(
        hovertemplate="Customer %{y}<br>Sales: %{x:,.2f}<extra></extra>"
    )

    fig_customer = polish_chart(fig_customer, 390)
    fig_customer.update_layout(
        xaxis_title="Recorded sales",
        yaxis_title="Customer ID"
    )

    st.plotly_chart(
        fig_customer,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# =====================================================
# 9. BUSINESS INSIGHTS
# =====================================================
st.markdown("## Business insights")
st.caption(
    "Automatically calculated from the current country and date selection."
)

i1, i2, i3 = st.columns(3)

# Highest-selling country
if not country_sales.empty:
    top_country = country_sales.iloc[-1]
    with i1:
        st.markdown(
            f"""
            <div class="insight-card">
              <div class="insight-label">LEADING COUNTRY</div>
              <div class="insight-value">{top_country['Country']}</div>
              <div class="insight-description">
                Recorded sales: {top_country['TotalSales']:,.2f}
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Highest-selling product
if not product_sales.empty:
    top_product = product_sales.iloc[-1]
    product_name = str(top_product["Description"])
    if len(product_name) > 36:
        product_name = product_name[:33] + "..."

    with i2:
        st.markdown(
            f"""
            <div class="insight-card">
              <div class="insight-label">TOP PRODUCT BY SALES</div>
              <div class="insight-value">{product_name}</div>
              <div class="insight-description">
                Recorded sales: {top_product['TotalSales']:,.2f}
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Highest-sales month
if not monthly.empty:
    top_month = monthly.loc[monthly["TotalSales"].idxmax()]

    with i3:
        st.markdown(
            f"""
            <div class="insight-card">
              <div class="insight-label">STRONGEST MONTH</div>
              <div class="insight-value">{top_month['Month']}</div>
              <div class="insight-description">
                Recorded sales: {top_month['TotalSales']:,.2f}
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# 10. DATA QUALITY CONTEXT AND FOOTER
# =====================================================
with st.expander("Transaction notes and metric definitions"):
    st.write(
        f"- Rows included after filtering: {len(df):,}."
    )
    st.write(
        f"- Rows with negative TotalSales: {negative_sales_rows:,}."
    )
    st.write(
        f"- Distinct invoice numbers beginning with C: "
        f"{cancelled_invoice_count:,}."
    )
    st.write(
        "- Total Sales is the sum of TotalSales in the cleaned dataset."
    )
    st.write(
        "- Unique Invoices counts distinct InvoiceNo values, including "
        "cancellation invoice numbers if they are present."
    )
    st.write(
        "- Average Sales per Invoice = Total Sales / Unique Invoices. "
        "It is not necessarily average completed-order value."
    )
    st.write(
        "- Customer and product rankings use net recorded sales, "
        "so negative sales can affect their order."
    )

st.divider()

footer_left, footer_right = st.columns(2)

with footer_left:
    st.caption(
        "E-COMMERCE INTELLIGENCE  ·  Python / Pandas / Plotly / Streamlit"
    )

with footer_right:
    st.caption(
        f"{len(df):,} filtered rows · {len(original_df):,} total cleaned rows"
    )
