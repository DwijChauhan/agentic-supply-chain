import streamlit as st
from agent_logic import SupplyChainAgent

# Page Config
st.set_page_config(page_title="SAP Code Unnati | Agentic Logistics", layout="wide")

st.title("🇮🇳 Autonomous Indian Logistics Rerouter")
st.markdown("---")

# Initialize Agent
if 'agent' not in st.session_state:
    with st.spinner("Initializing Agentic Logic..."):
        st.session_state.agent = SupplyChainAgent()

agent = st.session_state.agent

if not agent.df.empty:
    # Get unique list of all hubs for the dropdowns
    all_hubs = sorted(list(set(agent.df['source_name'].unique()) | set(agent.df['destination_name'].unique())))

    # Sidebar for Inputs
    st.sidebar.header("Route Settings")
    
    # NEW: Dropdowns to check distance between specific hubs
    origin = st.sidebar.selectbox("Select Origin:", all_hubs, index=0)
    destination = st.sidebar.selectbox("Select Destination:", all_hubs, index=min(1, len(all_hubs)-1))
    
    report = st.sidebar.text_area("Live Incident Report:", "Normal conditions")
    run_btn = st.sidebar.button("Run Simulation")

    if run_btn:
        with st.spinner("Agent is reasoning..."):
            # Pass selected cities to the agent
            res = agent.process_incident(report, start_node=origin, end_node=destination)
        
        col1, col2 = st.columns([1, 1])

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
            st.metric("Total Distance", f"{res['cost']} KM")
            st.write(f"**From:** {res['start']}")
            st.write(f"**To:** {res['end']}")

    # Raw Data Preview
    st.markdown("---")
    with st.expander("View Master Data"):
        st.dataframe(agent.df[['source_name', 'destination_name', 'osrm_distance']].head(10))
