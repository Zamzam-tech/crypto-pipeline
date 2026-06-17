import duckdb
import plotly.graph_objects as go

conn = duckdb.connect('ingestion/crypto_data.db')

df = conn.execute("""
    SELECT date, avg_price, fear_greed_score, sentiment
    FROM fact_daily_market
    WHERE coin_name = 'Bitcoin'
    ORDER BY date ASC
""").df()

conn.close()

# Dual axis chart
fig = go.Figure()

# Bitcoin price — left axis
fig.add_trace(go.Scatter(
    x=df['date'],
    y=df['avg_price'],
    name='Bitcoin Price (USD)',
    line=dict(color='orange', width=2),
    yaxis='y1'
))

# Fear & Greed — right axis
fig.add_trace(go.Scatter(
    x=df['date'],
    y=df['fear_greed_score'],
    name='Fear & Greed Score',
    line=dict(color='red', width=2, dash='dot'),
    yaxis='y2'
))

fig.update_layout(
    title='Bitcoin Price vs Fear & Greed Index (May-June 2026)',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Price (USD)', side='left'),
    yaxis2=dict(title='Fear & Greed Score', side='right', overlaying='y', range=[0, 100]),
    legend=dict(x=0.01, y=0.99),
    hovermode='x unified'
)

fig.show()