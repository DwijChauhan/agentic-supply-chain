import streamlit as st
from agent_logic import SupplyChainAgent

st.set_page_config(page_title="SAP Code Unnati | Agentic AI", layout="wide")
st.title("🇮🇳 Autonomous Indian Logistics Rerouter")

if 'agent' not in st.session_state:
    st.session_state.agent = SupplyChainAgent()
agent = st.session_state.agent

# Sidebar
all_hubs = sorted(list(set(agent.df['source_name'].unique())))
st.sidebar.header("Route Settings")
origin = st.sidebar.selectbox("Select Origin:", all_hubs)
destination = st.sidebar.selectbox("Select Destination:", all_hubs)
report = st.sidebar.text_area("Incident Report:", "Normal conditions")
run_btn = st.sidebar.button("Run Simulation")

if run_btn:
    res = agent.process_incident(report, origin, destination)
    
    # 1. Risk Meter
    st.subheader("🛡️ Agentic Risk Assessment")
    st.progress(res["risk_level"] / 10)
    st.write(f"**Confidence Score:** {10 - res['risk_level']}/10 | **Risk Factor:** {res['risk_level']}/10")

    # 2. ROI / Comparison Metrics
    st.write("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Standard Distance", f"{res['base_cost']} KM")
    c2.metric("Optimized Distance", f"{res['opt_cost']} KM")
    diff = round(res['opt_cost'] - res['base_cost'], 2)
    c3.metric("Safety Buffer", f"{diff} KM", delta_color="inverse")

    # 3. Path Output
    st.subheader("🛣️ Optimized Path")
    st.code(" ➔ ".join(res["path"]))
