import streamlit as st
from agent_logic import SupplyChainAgent

# Page Config
st.set_page_config(page_title="SAP Code Unnati | Agentic AI", layout="wide")

st.title("🇮🇳 Autonomous Indian Logistics Rerouter")
st.markdown("---")

# Initialize Agent
if 'agent' not in st.session_state:
    with st.spinner("Initializing Agentic Logic..."):
        st.session_state.agent = SupplyChainAgent()

agent = st.session_state.agent

# Check if data loaded
if agent.df.empty:
    st.error("Missing 'delhivery_small.csv' on GitHub! Please upload the file to start.")
else:
    # Sidebar for Inputs
    st.sidebar.header("Control Panel")
    report = st.sidebar.text_area("Live Incident Report:", "Heavy rains near Anand_VUNagar_DC")
    run_btn = st.sidebar.button("Run Agentic Simulation")

    # Main Dashboard Area
    col1, col2 = st.columns([1, 1])

    if run_btn:
        with st.spinner("Agent is reasoning..."):
            res = agent.process_incident(report)
        
        with col1:
            st.subheader("🤖 Agentic Reasoning")
            if res["status"] == "REROUTED":
                st.warning(f"**Status:** {res['status']}")
            else:
                st.success(f"**Status:** {res['status']}")
            st.write(f"*Reasoning:* {res['reasoning']}")
            
            st.subheader("🛣️ Optimized Path")
            st.code(" ➔ ".join(res["path"]))

        with col2:
            st.subheader("📊 Route Metrics")
            st.metric("Total Distance (KM)", f"{res['cost']} km")
            st.metric("Origin", res["start"])
            st.metric("Destination", res["end"])

    # Show raw data section (Plan A)
    st.markdown("---")
    with st.expander("View Real-Time Master Data (Delhivery Sample)"):
        st.dataframe(agent.df[['source_name', 'destination_name', 'osrm_distance', 'osrm_time']].head(20))

st.caption("Developed for SAP Code Unnati 2.0 | Agentic AI & DP Optimization")
