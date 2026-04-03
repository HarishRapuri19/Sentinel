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

---

## 📂 Project Structure

```directory
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
🛠️ Local Setup & Installation1. Clone the RepositoryBashgit clone [https://github.com/your-username/Project-Sentinel.git](https://github.com/your-username/Project-Sentinel.git)
cd Project-Sentinel
2. Environment ConfigurationCreate a .env file in the root directory. Never commit this file.Bash# Example .env content
GROQ_API_KEY=your_key_here
3. Install DependenciesBashpip install -r requirements.txt
4. Run the ApplicationBashstreamlit run src/app.py
🌐 Deployment to Streamlit CloudPush your code to GitHub (ensure .env is ignored via .gitignore).Connect your repo to Streamlit Community Cloud.Add your GROQ_API_KEY to the Secrets section in the Streamlit Cloud dashboard.Set the main file path to src/app.py.📈 
Implementation MetricsMetricComplexityFeasibilityConfidence ScoreTelemetry ParserMediumHigh95%ROI CalculatorLowHigh100%AI RefactoringMediumHigh92%Developed by: Harish RapuriRole: Senior Software Engineer | AI FinOps Specialist