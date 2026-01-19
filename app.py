import streamlit as st
from agent_logic import SupplyChainAgent

st.set_page_config(page_title="SAP Code Unnati | Agentic AI", layout="wide")
st.title("🚚 Autonomous Gujarat Logistics Rerouter")

# Initialize the Agent
if 'agent' not in st.session_state:
    st.session_state.agent = SupplyChainAgent()
agent = st.session_state.agent

if not agent.df.empty:
    all_hubs = sorted(list(agent.df['source_name'].unique()))

    # SIDEBAR: Control Panel
    st.sidebar.header("Route Settings")
    origin = st.sidebar.selectbox("Origin Hub:", all_hubs)
    destination = st.sidebar.selectbox("Destination Hub:", all_hubs, index=min(5, len(all_hubs)-1))
    report = st.sidebar.text_area("Live Incident Report:", "Normal Conditions")
    run_btn = st.sidebar.button("Run Agentic Rerouter", type="primary")

    if run_btn:
        # Agent Logic Triggered
        res = agent.process_incident(report, origin, destination)
        
        # DISPLAY: Agent Intelligence
        st.subheader("🛡️ Agentic Reasoning")
        st.info(f"**AI Strategy:** {res['reasoning']}")
        st.progress(res["risk_level"] / 10)

        st.write("---")
        
        # DISPLAY: Metrics
        st.subheader("📊 Rerouting Metrics")
        c1, c2, c3 = st.columns(3)
        c1.metric("Original Distance", f"{res['base_cost']} km")
        c2.metric("New Path Cost", f"{res['opt_cost']} km")
        
        cost_diff = round(res['opt_cost'] - res['base_cost'], 2)
        c3.metric("Cost of Delay", f"+{cost_diff} km" if cost_diff > 0 else "0 km")

        # DISPLAY: The Sequence
        st.subheader("📍 Agent's New Path")
        if res["path"] and "No connection" not in res["path"][-1]:
            st.success(" ➔ ".join(res["path"]))
        else:
            st.error("The agent determined no safe route is currently available.")
