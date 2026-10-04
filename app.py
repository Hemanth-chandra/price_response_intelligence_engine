
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Price Response Intelligence Engine",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE = Path(__file__).parent
DATA = BASE / "data"

st.markdown("""
<style>
.main .block-container {padding-top:1.3rem; max-width:1500px;}
[data-testid="stSidebar"] {background:#0b1930;}
[data-testid="stSidebar"] * {color:white !important;}
.hero {
    padding:2.1rem 2.4rem; border-radius:20px; margin-bottom:1.2rem;
    background:linear-gradient(135deg,#0b1930 0%,#123b68 100%);
    color:white;
}
.hero h1 {font-size:2.55rem;margin:0;}
.hero p {font-size:1.08rem;margin:.5rem 0 0;}
div[data-testid="stMetric"] {
    background:#ffffff; border:1px solid #e5e7eb;
    padding:12px; border-radius:14px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def read_csv(name):
    return pd.read_csv(DATA / name)

summary = read_csv("project_summary.csv")
events = read_csv("event_types.csv")
reduction = read_csv("reduction_distribution.csv")
daily = read_csv("daily_activity.csv")
categories = read_csv("category_results.csv")
episodes = read_csv("reduction_episodes.csv")
sensitivity = read_csv("baseline_sensitivity.csv")

st.sidebar.title("🧊 Price Response")
st.sidebar.caption("Intelligence Engine")
page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Price Analysis",
        "Causal Analysis",
        "Category Insights",
        "Simulation & What-if",
        "A/B Test Planner",
        "Data & Methodology"
    ]
)

st.markdown("""
<div class="hero">
<h1>Price Response <span style="color:#55a8ff">Intelligence Engine</span></h1>
<p>Causal analysis of observed price reductions on e-commerce purchases</p>
<p>From customer behaviour data → estimated impact → business decision</p>
</div>
""", unsafe_allow_html=True)

if page == "Overview":
    st.subheader("Overview")
    st.caption("Current feasibility sample: 20 million e-commerce events, October 1–15, 2019.")

    cols = st.columns(6)
    metrics = [
        ("Events", "20.0M"),
        ("Products", "139,877"),
        ("Users", "1.76M"),
        ("Days", "15"),
        ("≥10% Reductions", "4.00%"),
        ("10% Episodes", "477"),
    ]
    for col, (label, value) in zip(cols, metrics):
        col.metric(label, value)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(
            events, values="events", names="event_type",
            hole=.55, title="Event Type Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(
            reduction, x="reduction_bucket", y="percentage",
            title="Observed Price Reduction Distribution",
            text="percentage"
        )
        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig.update_layout(xaxis_title="", yaxis_title="Product-days (%)")
        st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=daily["d"], y=daily["views"], name="Views"
    ))
    fig.add_trace(go.Scatter(
        x=daily["d"], y=daily["purchases"],
        name="Purchases", yaxis="y2", mode="lines+markers"
    ))
    fig.update_layout(
        title="Purchase Activity Over Time",
        yaxis=dict(title="Views"),
        yaxis2=dict(title="Purchases", overlaying="y", side="right")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.success(
        "Feasibility status: PROMISING / CONTINUE — sufficient observed price "
        "variation and reduction episodes to proceed to causal analysis."
    )

elif page == "Price Analysis":
    st.subheader("Price Analysis")

    threshold = st.select_slider(
        "Observed price reduction threshold",
        options=[0.05, 0.10, 0.15, 0.20],
        value=0.10,
        format_func=lambda x: f"{x:.0%}"
    )

    row = summary.iloc[0]
    rates = {
        0.05: row["reduction_5pct_pct"],
        0.10: row["reduction_10pct_pct"],
        0.15: row["reduction_15pct_pct"],
        0.20: row["reduction_20pct_pct"],
    }

    c1, c2, c3 = st.columns(3)
    c1.metric("Reduction rate", f"{rates[threshold]:.2f}%")
    c2.metric(
        "Reduction episodes",
        f"{int(row[f'episodes_{int(threshold*100)}pct']):,}"
    )
    c3.metric("Same-day ≥5% mixing", "1.31%")

    fig = px.bar(
        reduction,
        x="reduction_bucket",
        y="percentage",
        text="percentage",
        title="Price Reduction Buckets"
    )
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Baseline sensitivity")
    st.dataframe(sensitivity, use_container_width=True, hide_index=True)

    st.info(
        "The project uses 'observed price reduction' rather than assuming "
        "the change was caused by a promotion or discount."
    )

elif page == "Causal Analysis":
    st.subheader("Causal Analysis")

    st.warning(
        "Causal estimation is the next analytical stage. The current deployed "
        "version intentionally does not invent a causal effect from the feasibility sample."
    )

    st.markdown("""
### Planned identification strategy

1. **Naive comparison** — treated vs untreated purchase rate.
2. **Product fixed effects** — control for stable product differences.
3. **Time fixed effects** — control for common daily shocks.
4. **Event study** — inspect outcomes before and after treatment.
5. **Pre-trend test** — check whether treated products were already moving differently.
6. **Placebo test** — assign fake treatment dates and check for false effects.
7. **Robustness** — repeat at 5%, 10%, 15%, and 20% thresholds.
8. **Category-level effects** — aggregate where product-level evidence is insufficient.
9. **Confidence intervals** — report uncertainty rather than a single point estimate.
""")

    c1, c2, c3 = st.columns(3)
    c1.metric("10% reduction episodes", "477")
    c2.metric("Strict usable products", "0")
    c3.metric("Current evidence", "Feasibility passed")

    st.markdown("### What we will NOT claim")
    st.write(
        "Observed price reductions do not automatically prove that price caused "
        "the purchase change. The final business recommendation should be validated "
        "with a controlled A/B experiment."
    )

elif page == "Category Insights":
    st.subheader("Category Insights")

    top = categories.sort_values("reduction_10pct_days", ascending=False).head(20)

    fig = px.bar(
        top.sort_values("reduction_10pct_days"),
        x="reduction_10pct_days",
        y="category",
        orientation="h",
        title="Categories with Most ≥10% Reduction Days"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        categories,
        use_container_width=True,
        hide_index=True
    )

elif page == "Simulation & What-if":
    st.subheader("Margin Scenario Simulator")

    st.info(
        "The source dataset does not provide product cost or margin. "
        "Therefore margin is an explicit scenario assumption, not an observed value."
    )

    c1, c2 = st.columns(2)
    with c1:
        margin = st.slider("Assumed gross margin", 0.10, 0.60, 0.30, 0.05)
        reduction_pct = st.slider("Observed price reduction", 0.05, 0.30, 0.10, 0.05)
    with c2:
        baseline_price = st.number_input("Baseline price ($)", 10.0, 5000.0, 100.0, 5.0)
        baseline_units = st.number_input("Baseline units", 1, 100000, 100, 1)

    lift = st.slider(
        "Assumed purchase lift",
        -0.50, 1.00, 0.15, 0.05
    )

    new_price = baseline_price * (1 - reduction_pct)
    new_units = baseline_units * (1 + lift)

    baseline_profit = baseline_price * baseline_units * margin
    scenario_profit = new_price * new_units * margin
    change = scenario_profit - baseline_profit

    a, b, c = st.columns(3)
    a.metric("Baseline profit", f"${baseline_profit:,.2f}")
    b.metric("Scenario profit", f"${scenario_profit:,.2f}")
    c.metric("Profit change", f"${change:+,.2f}")

elif page == "A/B Test Planner":
    st.subheader("A/B Test Planner")

    reduction_pct = st.slider(
        "Proposed treatment reduction",
        0.05, 0.30, 0.10, 0.05
    )

    st.markdown(f"""
### Experiment design

**Control:** current pricing strategy

**Treatment:** approximately **{reduction_pct:.0%} observed price reduction**

### Primary metric
**Contribution profit per visitor**

### Secondary metrics
- Purchase conversion
- Purchases per visitor
- Revenue per visitor

### Guardrails
- Margin
- Inventory availability
- Returns / cancellations
- Customer behaviour after treatment

### Decision rule

Do not roll out the strategy simply because purchases increase.

The treatment should improve the primary business metric while remaining
within the predefined guardrails.
""")

elif page == "Data & Methodology":
    st.subheader("Data & Methodology")

    st.markdown("""
## Dataset

REES46 multi-category e-commerce behavior data.

### Unit of analysis

**Product-day**

The raw event stream is aggregated into daily product-level observations.

### Price baseline

A trailing price baseline is used to identify an observed price reduction.

### Treatment thresholds

- 5%
- 10%
- 15%
- 20%

### Current feasibility result

- 20,000,000 events
- 139,877 products
- 15 calendar days
- 477 ≥10% reduction episodes
- 4.00% ≥10% reduction product-days

### Important limitation

The data records observed prices and customer behaviour but does not establish
why a price changed. Therefore this project does not equate every price reduction
with a promotional discount.

The causal estimate will be presented as an **observational causal estimate**
with assumptions, uncertainty and robustness checks.

Final business validation is through an A/B test.
""")

    st.markdown("### Data-quality checks")
    st.write(
        "Missing values, price quality, duplicates, product-day coverage, "
        "price variation, same-day price mixing, reduction distribution, "
        "episode counts and 7-day vs 14-day baseline sensitivity."
    )
