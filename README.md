# 🚀 Crypto Data Engineering Pipeline

An end-to-end data engineering pipeline that ingests live cryptocurrency market data from the CoinGecko API, processes it through a medallion architecture using dbt, and stores analytics-ready datasets in DuckDB for downstream analysis and visualization.

> 💡 This pipeline passively captured the June 6th 2026 Bitcoin crash (-11.87% in a single hour) — an event that triggered $1.1B in global liquidations.

---

## 🧱 Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Data ingestion & orchestration scripts |
| Apache Airflow | Hourly pipeline scheduling |
| DuckDB | Lightweight analytical warehouse |
| dbt | Data modeling & transformations |
| Streamlit + Plotly | Interactive dashboard & visualizations |
| Jupyter Notebook | Exploratory data analysis |
| Linux/WSL | Deployment & monitoring |

---

## 🏗️ Architecture
**Medallion Architecture:**
- 🥉 Bronze — raw API responses stored in DuckDB
- 🥈 Silver — dbt staging layer (cleaned, deduplicated, typed)
- 🥇 Gold — dbt marts layer (business-ready analytical tables)

---

## 📊 Key Analysis Findings

From 1 month of hourly data across 55 coins (May–June 2026):

- 📉 Bitcoin dropped **-11.87% in a single hour** on June 6th 2026
- 💸 The crash triggered **$1.1B in liquidations** globally
- 🏆 Rain was the best performer at **+69.4% return** over the same period
- 🔗 Bitcoin/Ethereum correlation of **0.98** — confirming limited diversification benefits in crypto portfolios
- 👑 Bitcoin maintained **~60% market dominance** throughout the entire period
- 📊 LAB coin recorded the highest hourly volatility at **~9% standard deviation** per hour

---

## ⚙️ Pipeline Components

**🔹 Ingestion Layer**
Fetches real-time cryptocurrency market data from CoinGecko API every hour. Handles API responses, error handling, and loads raw data directly into DuckDB.

**🔹 Storage Layer (DuckDB)**
Acts as a lightweight analytical data warehouse. Stores raw ingested datasets and serves as the source for dbt transformations and downstream querying.

**🔹 Transformation Layer (dbt)**
- Staging models — data cleaning, standardization, deduplication, null handling, and type casting
- Mart models — business-ready analytical tables structured for reporting and analysis

**🔹 Orchestration Layer (Airflow)**
Four chained DAGs handle scheduled hourly ingestion, transformation triggering, and pipeline monitoring.

**🔹 Analysis Layer (Jupyter + Plotly)**
Full exploratory data analysis notebook covering price trends, volatility analysis, correlation matrices, volume analysis, and return rankings across all 55 tracked coins.

**🔹 Dashboard (Streamlit)**
Interactive dashboard with Plotly visualizations for real-time exploration of the pipeline output.

---

## 📁 Project Structure
ingestion/
└── main.py                         # API ingestion scripts
dags/
└── crypto_dag.py                   # Airflow DAGs
dbt/crypto_pipeline/
├── models/
│   ├── staging/                    # Cleaning & standardization layer
│   └── marts/                      # Analytics-ready tables
└── dbt_project.yml
analysis/
└── crypto_market_analysis.ipynb   # Full EDA notebook
dashboard.py                           # Streamlit dashboard
requirements.txt

---

## ▶️ How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run data ingestion
python ingestion/main.py

# 3. Run dbt transformations
cd dbt/crypto_pipeline
dbt run

# 4. Launch Streamlit dashboard
streamlit run dashboard.py
```

---

##  Roadmap

- [ ] Migrate storage layer to cloud warehouse (BigQuery or PostgreSQL)
- [ ] Add pipeline observability and alerting
- [ ] Expand dataset to include historical OHLCV data
- [ ] Deploy Streamlit dashboard publicly on Streamlit Cloud

---

*Part of my data engineering portfolio — focused on building production-style pipelines with real world data and deriving meaningful insights from them.*
