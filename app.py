import streamlit as st
from agent_logic import SupplyChainAgent

st.set_page_config(page_title="SAP Code Unnati | Agentic AI", layout="wide")
st.title("🚚 Autonomous Gujarat Logistics Rerouter")

# Initialize the Agent in session state
if 'agent' not in st.session_state:
    st.session_state.agent = SupplyChainAgent()
agent = st.session_state.agent

if not agent.df.empty:
    all_hubs = sorted(list(agent.df['source_name'].unique()))

    # Sidebar for simulation controls
    st.sidebar.header("Route Settings")
    origin = st.sidebar.selectbox("Origin Hub:", all_hubs)
    destination = st.sidebar.selectbox("Destination Hub:", all_hubs, index=min(5, len(all_hubs)-1))
    report = st.sidebar.text_area("Live Incident Report:", "Normal Conditions")
    run_btn = st.sidebar.button("Run Agentic Rerouter", type="primary")

    if run_btn:
        res = agent.process_incident(report, origin, destination)
        
        # AI Output
        st.subheader("🛡️ Agentic Reasoning")
        st.info(f"**AI Strategy:** {res['reasoning']}")
        st.progress(res["risk_level"] / 10)

        st.write("---")
        
        # Performance Metrics
        st.subheader("📊 Rerouting Metrics")
        c1, c2, c3 = st.columns(3)
        c1.metric("Standard Dist", f"{res['base_cost']} km")
        c2.metric("Agentic Path Cost", f"{res['opt_cost']} km")
        
        delay = round(res['opt_cost'] - res['base_cost'], 2)
        c3.metric("Delay Impact", f"+{delay} km" if delay > 0 else "0 km")

        # Path Display
        st.subheader("📍 Optimized Route Sequence")
        if res["path"] and len(res["path"]) > 1:
            st.success(" ➔ ".join(res["path"]))
        else:
            st.error("No safe route available. The agent advises halting delivery.")
