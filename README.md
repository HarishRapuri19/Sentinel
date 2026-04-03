# 🛡️ Project Sentinel: AI FinOps Architect

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Project Sentinel** is an enterprise-grade AI agent designed to optimize **Databricks** and **Apache Spark** compute costs. By analyzing Spark UI telemetry (JSON) and source code (.py), Sentinel identifies bottlenecks like disk spills and data skew, providing automated, refactored code to reduce DBU consumption.

---

## 🏗️ System Architecture

Project Sentinel utilizes a decoupled architecture to ensure high-performance AI reasoning without compromising data security.

1.  **Ingestion Layer:** Accepts PySpark scripts and SQL execution metrics.
2.  **Reasoning Engine:** Powered by **Groq (Llama-3)** and **LangChain** to parse physical plans.
3.  **Optimization Layer:** Applies Broadcast hints, Skew hints, and Salted keys.
4.  **FinOps Dashboard:** A Streamlit-based UI that calculates Annual ROI and Node Scaling.

---

## 🚀 Key Features

* **📊 FinOps ROI Scorecard:** Real-time calculation of runtime reduction and yearly cost savings.
* **⚡ Spark Optimization:** Automated conversion of `SortMergeJoin` to `BroadcastHashJoin`.
* **🛡️ Logic Guardrails:** Strict enforcement to ensure optimization never alters business logic.
* **📉 Cluster Right-Sizing:** Direct recommendations for downsizing clusters based on memory pressure.
* **🔄 Synced Code Review:** Side-by-side comparison of baseline vs. optimized code.

# 🛡️ Project Sentinel: AI FinOps Architect

**Project Sentinel** is an enterprise-grade AI agent designed to optimize **Databricks** and **Apache Spark** compute costs. By analyzing Spark UI telemetry (JSON) and source code (.py), Sentinel identifies bottlenecks like disk spills and data skew, providing automated, refactored code to reduce DBU consumption.

---

## 📂 Project Structure

```text
Project-Sentinel/
├── src/
│   ├── app.py              # Main Streamlit Dashboard
│   ├── finops_agent.py     # AI Agent & Prompt Engineering
│   └── mock_data.py        # Test telemetry & code samples
├── .streamlit/
│   └── config.toml         # Theme and Server settings
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── .gitignore              # Security: Prevents .env from being committed

````

---

## 🏗️ Architecture Overview

The **Sentinel Engine** operates as a decoupled AI agent. It separates the telemetry ingestion from the optimization logic to ensure 100% code integrity.

* **Ingestion:** Parsers for `.py` (Source) and `.json` (Spark Metrics).
* **Reasoning:** LangChain + Groq (Llama-3) to identify physical plan bottlenecks.
* **Optimization:** Rule-based and Generative refactoring for Spark DAGs.
* **FinOps UI:** Databricks-themed dashboard for ROI visualization.

---

## 💻 Local Setup Guide

Follow these steps to run Project Sentinel on your local workstation.

### 1. Environment Preparation
Ensure you have **Python 3.10+** installed. We recommend using a virtual environment to avoid dependency conflicts.

```bash
# Clone the repository
git clone [https://github.com/your-username/Project-Sentinel.git](https://github.com/your-username/Project-Sentinel.git)
cd Project-Sentinel

# Create and activate virtual environment
python -m venv sentinel_env
source sentinel_env/bin/activate  # On Windows use: .\sentinel_env\Scripts\activate
