import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(page_title="Advertising & Sales Dashboard", page_icon="📊", layout="wide")

st.title("📊 Advertising & Sales Analytics Dashboard")
st.caption("Interactive analysis of advertising spend across media channels and sales performance by city.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Advertising_F.csv")
    return df

try:
    df = load_data()

    # Sidebar Filters
    st.sidebar.header("Filter Data")
    cities = st.sidebar.multiselect("Select Cities:", options=df["City"].unique(), default=df["City"].unique())
    filtered_df = df[df["City"].isin(cities)]

    # Top KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"${filtered_df['sales'].sum():,.1f}k")
    col2.metric("TV Spend", f"${filtered_df['TV'].sum():,.1f}k")
    col3.metric("Radio Spend", f"${filtered_df['radio'].sum():,.1f}k")
    col4.metric("Newspaper Spend", f"${filtered_df['newspaper'].sum():,.1f}k")

    st.markdown("---")

    # Layout Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Channel Correlations", "🗺️ City Map Overview", "📋 Raw Data"])

    with tab1:
        st.subheader("Sales vs. Advertising Spend")
        channel = st.selectbox("Select Advertising Channel:", ["TV", "radio", "newspaper"])
        fig_scatter = px.scatter(
            filtered_df, 
            x=channel, 
            y="sales", 
            color="City",
            size="sales", 
            trendline="ols",
            title=f"Sales vs {channel.capitalize()} Budget"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab2:
        st.subheader("Geographic Sales Distribution")
        fig_map = px.scatter_mapbox(
            filtered_df,
            lat="latitude",
            lon="longitude",
            size="sales",
            color="sales",
            hover_name="City",
            hover_data=["TV", "radio", "newspaper", "sales"],
            color_continuous_scale=px.colors.cyclical.IceFire,
            zoom=3,
            mapbox_style="carto-positron",
            title="Sales Performance Across Cities"
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with tab3:
        st.subheader("Dataset Table")
        st.dataframe(filtered_df, use_container_width=True)

except FileNotFoundError:
    st.error("Data file `Advertising_F.csv` not found. Please place `Advertising_F.csv` in the same directory as this file.")
