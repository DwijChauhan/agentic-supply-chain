import streamlit as st
from agent_logic import SupplyChainAgent

st.set_page_config(page_title="SAP Code Unnati | Agentic AI", layout="wide")

st.title("🇮🇳 Autonomous Indian Logistics Rerouter")
st.markdown("### Agentic AI & Dynamic Programming Optimization")

if 'agent' not in st.session_state:
    with st.spinner("Loading Delhivery Logistics Data..."):
        st.session_state.agent = SupplyChainAgent()

agent = st.session_state.agent

# Sidebar Control
st.sidebar.header("Logistics Control Center")
report = st.sidebar.text_area("Incident Report:", "Heavy rain near Anand_VUNagar_DC")
run_btn = st.sidebar.button("Execute Agentic Reasoning")

if run_btn:
    with st.spinner("Agent is analyzing and recalculating..."):
        res = agent.process_incident(report)
    
    if res.get("status") == "ERROR":
        st.error(f"⚠️ {res['reasoning']}")
    else:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("🤖 AI Reasoning Engine")
            if res["status"] == "REROUTED":
                st.warning("🚨 REROUTE TRIGGERED")
            else:
                st.success("✅ OPTIMAL PATH SECURE")
            st.info(f"**Reasoning:** {res['reasoning']}")
            st.subheader("🛣️ Final Computed Path")
            st.code(" ➔ ".join(res["path"]))

        with col2:
            st.subheader("📊 Route Analytics")
            st.metric("Total Distance", f"{res['cost']} KM")
            st.metric("Source Hub", res["start"])
            st.metric("Destination Hub", res["end"])

st.markdown("---")
with st.expander("View Active Logistics Segments (Delhivery Data)"):
    if not agent.df.empty:
        st.dataframe(agent.df[['source_name', 'destination_name', 'osrm_distance', 'osrm_time']].head(10))
