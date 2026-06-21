#  Crypto Data Engineering Pipeline

An end-to-end data engineering pipeline that ingests live cryptocurrency market data from CoinGecko API and the Fear & Greed Index, processes it through a medallion architecture using dbt, and stores analytics-ready datasets in DuckDB for downstream analysis and visualization.

>  This pipeline passively captured the June 6th 2026 Bitcoin crash (-11.87% in a single hour) — an event that triggered $1.1B in global liquidations. Fear & Greed sentiment hit 10/100 (Extreme Fear) confirming the market panic.

---

##  Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Data ingestion & orchestration scripts |
| Apache Airflow | Pipeline scheduling (crypto: 30min, sentiment: 24hr) |
| DuckDB | Lightweight analytical warehouse |
| dbt | Data modeling & transformations |
| CoinGecko API | Live cryptocurrency market data |
| alternative.me API | Daily Fear & Greed sentiment index |
| Streamlit + Plotly | Interactive dashboard & visualizations |
| Jupyter Notebook | Exploratory data analysis |
| Linux/WSL | Deployment & monitoring |

---

##  Architecture
CoinGecko API ─────┐

├──▶ Python Ingestion ──▶ DuckDB (Raw)

alternative.me ────┘         ↓

dbt Staging

(stg_coins + stg_fear_greed)

↓

dbt Marts

(marts_coin + fact_daily_market)

↓

Jupyter Analysis + Streamlit Dashboard

**Medallion Architecture:**
- 🥉 Bronze — raw API responses stored in DuckDB
- 🥈 Silver — dbt staging layer (cleaned, deduplicated, typed)
- 🥇 Gold — dbt marts layer (business-ready analytical tables)

---

## 📊 Key Analysis Findings

From 1 month of hourly data across 55 coins (May–June 2026):

- 📉 Bitcoin dropped **-11.87% in a single hour** on June 6th 2026
- 💸 The crash triggered **$1.1B in liquidations** globally
- 😱 Fear & Greed Index hit **10/100 (Extreme Fear)** during the crash — confirmed via multi-source JOIN in `fact_daily_market`
- 🏆 Rain was the best performer at **+69.4% return** over the same period
- 🔗 Bitcoin/Ethereum correlation of **0.98** — confirming limited diversification benefits in crypto portfolios
- 👑 Bitcoin maintained **~60% market dominance** throughout the entire period
- 📊 LAB coin recorded the highest hourly volatility at **~9% standard deviation** per hour

📓 **[View Full Analysis Notebook](https://nbviewer.org/github/Zamzam-tech/crypto-pipeline/blob/main/crypto_analysis/crypto_market_analysis.ipynb)**

---

## Pipeline Components

**🔹 Ingestion Layer**
Two separate ingestion scripts for different data sources and schedules:
- `crypto_ingestion.py` — fetches CoinGecko market data every 30 minutes
- `fear_greed_ingestion.py` — fetches Fear & Greed sentiment index once daily

**🔹 Storage Layer (DuckDB)**
Lightweight analytical data warehouse storing two raw tables: `crypto_data` and `fear_greed`.

**🔹 Transformation Layer (dbt)**
- Staging models — `stg_coins` and `stg_fear_greed` (cleaning, standardization, type casting)
- Mart models — `marts_coin` (top coins leaderboard) and `fact_daily_market` (daily price + sentiment JOIN)

**🔹 Orchestration Layer (Airflow)**
Two separate DAGs with different schedules:
- `crypto_pipeline` — runs every 30 minutes
- `fear_greed_pipeline` — runs every 24 hours

**🔹 Analysis Layer (Jupyter + Plotly)**
Full EDA notebook covering price trends, volatility, correlation matrices, volume analysis, return rankings, and Fear & Greed correlation across 55 coins.

**🔹 Dashboard (Streamlit)**
Interactive dashboard with real-time metrics, price over time, market cap rankings, and Fear & Greed vs Bitcoin price visualization.

---

##  Project Structure
ingestion/

├── crypto_ingestion.py         # CoinGecko ingestion

└── fear_greed_ingestion.py     # Fear & Greed ingestion

dags/

├── crypto_dag.py               # 30-min Airflow DAG

└── fear_greed_dag.py           # 24-hr Airflow DAG

dbt/crypto_pipeline/

├── models/

│   ├── staging/                # stg_coins + stg_fear_greed

│   └── marts/                  # marts_coin + fact_daily_market

└── dbt_project.yml

analysis/

└── crypto_market_analysis.ipynb

dashboard.py

requirements.txt

---

##  How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run ingestion
python ingestion/crypto_ingestion.py
python ingestion/fear_greed_ingestion.py

# 3. Run dbt transformations
cd dbt/crypto_pipeline
dbt run

# 4. Launch Streamlit dashboard
streamlit run dashboard.py

# 5. Start Airflow
airflow standalone
```

---

##  Roadmap

- [ ] Migrate storage layer to cloud warehouse (BigQuery or PostgreSQL)
- [x] Add second data source (Fear & Greed Index) ✅
- [ ] Add pipeline observability and alerting
- [ ] Deploy Streamlit dashboard publicly on Streamlit Cloud
- [ ] Expand dataset to include historical OHLCV data

---

*Part of my data engineering portfolio — focused on building production-style pipelines with real world data and deriving meaningful insights from them.*
