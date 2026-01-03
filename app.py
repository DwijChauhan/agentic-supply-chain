import streamlit as st
from agent_logic import SupplyChainAgent

st.set_page_config(page_title="SAP Code Unnati | Agentic AI", layout="wide")
st.title("🚚 Autonomous Gujarat Logistics Rerouter")
st.caption("Agentic AI & Dynamic Programming Optimization | Delhivery Dataset")

if 'agent' not in st.session_state:
    st.session_state.agent = SupplyChainAgent()
agent = st.session_state.agent

# Check if data loaded correctly
if not agent.df.empty:
    all_hubs = sorted(list(agent.df['source_name'].unique()))

    # SIDEBAR: User Inputs
    st.sidebar.header("Route Settings")
    origin = st.sidebar.selectbox("Select Origin Hub:", all_hubs)
    destination = st.sidebar.selectbox("Select Destination Hub:", all_hubs, index=min(5, len(all_hubs)-1))
    
    report = st.sidebar.text_area("Live Incident Report:", "Heavy rains reported in Anand")
    run_btn = st.sidebar.button("Execute Agentic Simulation", type="primary")

    if run_btn:
        res = agent.process_incident(report, origin, destination)
        
        # 1. RISK ASSESSMENT PROGRESS BAR
        st.subheader("🛡️ Agentic Risk Assessment")
        risk_color = "red" if res["risk_level"] > 5 else "orange" if res["risk_level"] > 0 else "green"
        st.markdown(f"**Risk Level: {res['risk_level']}/10**")
        st.progress(res["risk_level"] / 10)
        st.info(f"**AI Reasoning:** {res['reasoning']}")

        # 2. ROI / COMPARISON METRICS
        st.write("---")
        st.subheader("📊 Supply Chain ROI Analysis")
        c1, c2, c3 = st.columns(3)
        c1.metric("Standard Distance", f"{res['base_cost']} KM")
        c2.metric("Optimized Distance", f"{res['opt_cost']} KM")
        
        # Calculate Delta
        safety_buffer = round(res['opt_cost'] - res['base_cost'], 2)
        c3.metric("Safety Overhead", f"{safety_buffer} KM", delta_color="inverse")

        # 3. FINAL PATH OUTPUT
        st.subheader("🛣️ Final Optimized Path")
        st.success(f"**Status:** {res['status']}")
        st.code(" ➔ ".join(res["path"]))

else:
    st.error("Dataset not found. Please ensure 'delhivery_gujarat.csv' is in the root directory.")
