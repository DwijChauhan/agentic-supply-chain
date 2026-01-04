import streamlit as st
from agent_logic import SupplyChainAgent

st.set_page_config(page_title="SAP Code Unnati | Agentic AI", layout="wide")
st.title("🚚 Autonomous Gujarat Logistics Rerouter")

if 'agent' not in st.session_state:
    st.session_state.agent = SupplyChainAgent()
agent = st.session_state.agent

if not agent.df.empty:
    all_hubs = sorted(list(agent.df['source_name'].unique()))

    st.sidebar.header("Route Settings")
    origin = st.sidebar.selectbox("Select Origin Hub:", all_hubs)
    destination = st.sidebar.selectbox("Select Destination Hub:", all_hubs, index=min(5, len(all_hubs)-1))
    report = st.sidebar.text_area("Live Incident Report:", "Normal")
    run_btn = st.sidebar.button("Run Simulation", type="primary")

    if run_btn:
        res = agent.process_incident(report, origin, destination)
        
        st.subheader("🛡️ Agentic Risk Assessment")
        st.progress(res["risk_level"] / 10)
        st.info(f"**AI Reasoning:** {res['reasoning']}")

        st.write("---")
        st.subheader("📊 ROI Analysis")
        c1, c2, c3 = st.columns(3)
        c1.metric("Standard Dist", f"{res['base_cost']} KM")
        c2.metric("Optimized Dist", f"{res['opt_cost']} KM")
        diff = round(res['opt_cost'] - res['base_cost'], 2)
        c3.metric("Safety Overhead", f"{diff} KM", delta_color="inverse")

        st.subheader("🛣️ Final Path")
        st.code(" ➔ ".join(res["path"]))
else:
    st.error("Missing delhivery_gujarat.csv")
