# src/app.py
import sys
import os
import json
import streamlit as st

# --- PATH FIX ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.finops_agent import FinOpsOptimizer

# 1. Page Configuration
st.set_page_config(page_title="Databricks | Sentinel FinOps", layout="wide")

# 2. Forced High-Contrast CSS (Prevents Fading)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* Navigation Bar */
    .nav-bar {
        background-color: #1B262E; padding: 1.2rem 2.5rem;
        margin-bottom: 2rem; display: flex; 
        justify-content: space-between; align-items: center;
        border-radius: 4px;
    }
    
    /* Metric Cards - Solid Borders & Dark Labels */
    div[data-testid="stMetric"] {
        background-color: #F8F9FA !important; 
        border: 2px solid #E2E8F0 !important;
        border-radius: 8px !important; 
    }
    div[data-testid="stMetricValue"] { color: #FF3621 !important; font-size: 2.2rem !important; font-weight: 800 !important; }
    div[data-testid="stMetricLabel"] { color: #1B262E !important; font-weight: 700 !important; font-size: 1.1rem !important; }
    
    /* Action Buttons - Databricks Blue */
    .stButton>button {
        background-color: #00A1E0 !important; color: white !important;
        border: none !important; border-radius: 30px !important;
        font-weight: 700 !important; padding: 0.8rem 3rem !important;
        text-transform: uppercase;
    }
    
    /* Code Blocks - Dark with Syntax Pop */
    .stCodeBlock, pre { background-color: #111827 !important; border-radius: 8px !important; border: 1px solid #2D3748 !important; }
    code { color: #F7FAFC !important; }

    /* Sidebar Polish */
    section[data-testid="stSidebar"] { background-color: #1B262E !important; }
    section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# 3. STATE MANAGEMENT
if "opt_code" not in st.session_state: st.session_state.opt_code = ""
if "active_metrics" not in st.session_state: st.session_state.active_metrics = None
if "active_code" not in st.session_state: st.session_state.active_code = ""
if "yearly_runs" not in st.session_state: st.session_state.yearly_runs = 365

@st.cache_resource
def load_agent():
    return FinOpsOptimizer()

agent = load_agent()

# --- HEADER ---
st.markdown("""
    <div class='nav-bar'>
        <div style='font-size: 22px; font-weight: 900; color: #FFFFFF;'>
            <span style='color: #FF3621;'></span> DATABRICKS <span style='color: #00A1E0;'>SENTINEL</span>
        </div>
        <div style='color: #A0AEC0; font-size: 13px; font-weight: 600;'>AI-POWERED FINOPS ENGINE</div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### **DATA INGESTION**")
    s_file = st.file_uploader("Upload Script (.py)", type=["py"])
    m_file = st.file_uploader("Upload Metrics (.json)", type=["json"])
    
    if s_file: st.session_state.active_code = s_file.getvalue().decode("utf-8")
    if m_file: st.session_state.active_metrics = json.load(m_file)
        
    st.divider()
    logic_lock = st.toggle("Lock Business Logic", value=True)
    st.session_state.yearly_runs = st.number_input("Yearly Job Runs", value=st.session_state.yearly_runs)
    
    if st.button("🔄 RESET PLATFORM", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- METRIC EXTRACTION ---
def extract_metrics(data):
    if not data: return None
    rt = data.get("execution_time_seconds") or data.get("runtime_metrics", {}).get("skew_metrics", {}).get("max_task_duration_sec", 0)
    sp = data.get("metrics", {}).get("spill_to_disk_bytes") or data.get("runtime_metrics", {}).get("resource_usage", {}).get("disk_spill_bytes", 0)
    nd = data.get("cluster_info", {}).get("node_count") or data.get("project_metadata", {}).get("node_count", 8)
    return {"runtime": int(rt), "spill": float(sp), "nodes": int(nd)}

# --- MAIN UI ---
if not st.session_state.active_code:
    st.markdown("<h2 style='color: #1B262E;'>FinOps Analysis Hub</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #4A5568;'>👋 System Ready. Please upload your PySpark script and metrics in the sidebar to begin.</p>", unsafe_allow_html=True)
else:
    # ROI SCORECARD
    if st.session_state.opt_code and st.session_state.active_metrics:
        m = extract_metrics(st.session_state.active_metrics)
        est_t = int(m['runtime'] * 0.45)
        cur_n, req_n = m['nodes'], max(2, m['nodes'] // 2)
        sav_run = (cur_n - req_n) * 0.40 * (m['runtime'] / 3600)
        ann_sav = sav_run * st.session_state.yearly_runs
        
        st.markdown("<h2 style='color: #1B262E;'>💰 FinOps Value Realization</h2>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Runtime Reduction", f"{m['runtime']}s → {est_t}s", f"-{m['runtime']-est_t}s")
        c2.metric("Cluster Scaling", f"{cur_n} → {req_n} Nodes", "-50% Size")
        c3.metric("Savings / Run", f"${sav_run:.2f}", "Cost Reduction")
        c4.metric("Annual ROI Projection", f"${ann_sav:,.2f}", f"for {st.session_state.yearly_runs} runs")
        st.divider()

    # ACTION WORKSPACE (Titles fixed with HTML)
    st.markdown("<h3 style='color: #1B262E; margin-bottom: 10px;'>Optimization Workspace</h3>", unsafe_allow_html=True)
    if st.button("🚀 EXECUTE FINOPS OPTIMIZATION", use_container_width=True):
        if not st.session_state.active_metrics:
            st.error("⚠️ Metrics JSON missing.")
        else:
            with st.spinner("Analyzing DAG..."):
                mod = "\nRESTRICTION: Do NOT change logic." if logic_lock else ""
                st.session_state.opt_code = agent.optimize_pipeline(st.session_state.active_code + mod, st.session_state.active_metrics)
                st.rerun()

    # DUAL PANE
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("<h4 style='color: #1B262E;'>📝 Baseline Source</h4>", unsafe_allow_html=True)
        st.code(st.session_state.active_code, language="python")

    with col_r:
        st.markdown("<h4 style='color: #1B262E;'>✨ Sentinel Optimized</h4>", unsafe_allow_html=True)
        if st.session_state.opt_code:
            st.code(st.session_state.opt_code, language="python")
            # DOWNLOAD FIXED: data= keyword and key= provided
            st.download_button(
                label="💾 EXPORT OPTIMIZED CODE",
                data=st.session_state.opt_code,
                file_name="sentinel_optimized.py",
                mime="text/plain",
                use_container_width=True,
                key="download_sentinel"
            )
        else:
            st.write("---")
            st.caption("Results will appear here after execution.")