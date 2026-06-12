import duckdb
import pandas as pd
import streamlit as st
import plotly.express as px

DB_PATH = "/mnt/c/Users/yasab/OneDrive/Desktop/Lean Data pipleine/ingestion/crypto_data.db"

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("🪙 Crypto Market Dashboard")
st.caption("Live data from CoinGecko — updated every 30 minutes")

@st.cache_data(ttl=1800)
def load_data():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.sql("SELECT * FROM marts_coin").df()
    conn.close()
    return df

@st.cache_data(ttl=1800)
def load_history():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.sql("SELECT coin_name, current_price, ingested_at FROM stg_coins").df()
    conn.close()
    return df

df = load_data()
history_df = load_history()

latest = df.sort_values("ingested_at").groupby("coin_name").last().reset_index()

st.subheader("Latest Prices")
cols = st.columns(5)
for i, row in latest.head(5).iterrows():
    with cols[i % 5]:
        st.metric(
            label=row["coin_name"],
            value=f"${row['current_price']:,.2f}"
        )

cols2 = st.columns(5)
for i, row in latest.iloc[5:10].iterrows():
    with cols2[i % 5]:
        st.metric(
            label=row["coin_name"],
            value=f"${row['current_price']:,.2f}"
        )

st.divider()

st.subheader("Price Over Time")
coin_options = history_df["coin_name"].unique().tolist()
selected_coin = st.selectbox("Select a coin", sorted(coin_options))
coin_df = history_df[history_df["coin_name"] == selected_coin].sort_values("ingested_at")
fig1 = px.line(
    coin_df,
    x="ingested_at",
    y="current_price",
    title=f"{selected_coin} Price Over Time",
    labels={"ingested_at": "Time", "current_price": "Price (USD)"}
)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Market Cap Ranking")
    fig2 = px.bar(
        latest.sort_values("market_cap", ascending=False),
        x="coin_name",
        y="market_cap",
        color="coin_name",
        title="Market Cap by Coin",
        labels={"market_cap": "Market Cap (USD)", "coin_name": "Coin"}
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Trading Volume Ranking")
    fig3 = px.bar(
        latest.sort_values("total_volume", ascending=False),
        x="coin_name",
        y="total_volume",
        color="coin_name",
        title="Trading Volume by Coin",
        labels={"total_volume": "Volume (USD)", "coin_name": "Coin"}
    )
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("Price Category Distribution")
    cat_counts = latest["price_category"].value_counts().reset_index()
    cat_counts.columns = ["price_category", "count"]
    fig4 = px.pie(
        cat_counts,
        names="price_category",
        values="count",
        title="Coins by Price Category",
        color_discrete_map={"High": "#2ecc71", "Medium": "#f39c12", "Low": "#e74c3c"}
    )
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    st.subheader("Top 10 Coins Table")
    st.dataframe(
        latest[["coin_name", "symbol", "current_price", "market_cap_rank", "volume_rank", "price_category"]]
        .sort_values("market_cap_rank")
        .reset_index(drop=True),
        use_container_width=True
    )

st.caption(f"Last data ingestion: {df['ingested_at'].max()}")