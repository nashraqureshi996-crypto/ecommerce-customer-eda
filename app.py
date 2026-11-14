import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Customer EDA", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("ecommerce_customers.csv")

df = load_data()

st.title("E-Commerce Customer Behavior & EDA Dashboard")
st.write("Analyze online store customer engagement across the mobile app, website, and membership duration to understand yearly spending.")

# Sidebar Filters
st.sidebar.header("Filter Customers")
mem_range = st.sidebar.slider(
    "Length of Membership (Years)",
    float(df["Length of Membership"].min()),
    float(df["Length of Membership"].max()),
    (float(df["Length of Membership"].min()), float(df["Length of Membership"].max()))
)
spend_range = st.sidebar.slider(
    "Yearly Amount Spent ($)",
    float(df["Yearly Amount Spent"].min()),
    float(df["Yearly Amount Spent"].max()),
    (float(df["Yearly Amount Spent"].min()), float(df["Yearly Amount Spent"].max()))
)

filtered_df = df[
    (df["Length of Membership"].between(mem_range[0], mem_range[1])) &
    (df["Yearly Amount Spent"].between(spend_range[0], spend_range[1]))
]

# 4 Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", len(filtered_df))
col2.metric("Average Yearly Spend", f"${filtered_df['Yearly Amount Spent'].mean():.2f}" if len(filtered_df) else "$0.00")
col3.metric("Average Membership", f"{filtered_df['Length of Membership'].mean():.2f} yrs" if len(filtered_df) else "0.00 yrs")
col4.metric("Highest Spend", f"${filtered_df['Yearly Amount Spent'].max():.2f}" if len(filtered_df) else "$0.00")

st.divider()

# 5 Graphs
c1, c2 = st.columns(2)
with c1:
    fig1 = px.histogram(filtered_df, x="Yearly Amount Spent", nbins=25, title="1. Distribution of Yearly Amount Spent (Univariate)")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.box(filtered_df, y="Length of Membership", title="2. Spread of Length of Membership (Univariate)")
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    fig3 = px.scatter(filtered_df, x="Time on App", y="Yearly Amount Spent", title="3. Time on App vs Yearly Amount Spent (Bivariate)")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = px.scatter(filtered_df, x="Time on Website", y="Yearly Amount Spent", title="4. Time on Website vs Yearly Amount Spent (Bivariate)")
    st.plotly_chart(fig4, use_container_width=True)

num_cols = ['Avg. Session Length', 'Time on App', 'Time on Website', 'Length of Membership', 'Yearly Amount Spent']
corr = filtered_df[num_cols].corr()
fig5 = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", title="5. Correlation Heatmap of Numeric Features")
st.plotly_chart(fig5, use_container_width=True)

# Checkbox for Raw Data
if st.checkbox("Show Raw Data Table"):
    st.dataframe(filtered_df)

# Main Findings
st.subheader("Main Findings & Business Recommendation")
st.markdown("""
- **Membership Loyalty Drives Revenue:** `Length of Membership` has the strongest positive correlation (~0.81) with `Yearly Amount Spent`.
- **Mobile App Outperforms Website:** `Time on App` correlates strongly (~0.50) with spending, while `Time on Website` has virtually zero correlation.
- **Recommendation:** Invest in mobile app user experience and customer retention programs to maximize annual spending.
""")
