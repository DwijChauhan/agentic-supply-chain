import streamlit as st
from agent_logic import SupplyChainAgent

# 1. Page Configuration for a professional look
st.set_page_config(
    page_title="SAP Code Unnati | Agentic Logistics",
    page_icon="🚚",
    layout="wide"
)

# Custom Styling
st.title("🇮🇳 Autonomous Indian Logistics Rerouter")
st.markdown("### SAP Code Unnati 2.0: Agentic AI & Dynamic Programming Optimization")
st.write("---")

# 2. Initialize the Agent once and store it in the session
if 'agent' not in st.session_state:
    with st.spinner("Initializing Agent and Loading Delhivery Data..."):
        st.session_state.agent = SupplyChainAgent()

agent = st.session_state.agent

# 3. Sidebar for User Input
st.sidebar.header("Agent Control Panel")
st.sidebar.info("The Agent uses Perception-Reasoning-Action loops to manage disruptions.")

report = st.sidebar.text_area(
    "Live Incident Report:", 
    placeholder="e.g., Heavy flooding reported near Anand_VUNagar_DC",
    help="Enter any keywords like 'rain', 'storm', or 'blocked' along with a city name."
)

run_btn = st.sidebar.button("Run Agentic Simulation", type="primary")

# 4. Main Dashboard Output
if run_btn:
    with st.spinner("Agent is reasoning and recalculating optimal paths..."):
        # Trigger the Agentic Logic
        res = agent.process_incident(report)
    
    if res["status"] == "ERROR":
        st.error(f"⚠️ {res['reasoning']}")
    else:
        # Create Two Columns for the 'Output Screen'
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🤖 Agentic Reasoning")
            if res["status"] == "REROUTED":
                st.warning(f"**Current Status:** {res['status']}")
            else:
                st.success(f"**Current Status:** {res['status']}")
            
            st.write(f"**Reasoning:** {res['reasoning']}")
            
            st.subheader("🛣️ Optimized Path")
            # Displays the path with arrows
            path_display = " ➔ ".join(res["path"])
            st.code(path_display, language="text")

        with col2:
            st.subheader("📊 Route Analytics")
            # Professional Metrics
            m1, m2 = st.columns(2)
            m1.metric("Total Distance", f"{res['cost']} KM")
            m2.metric("Network Nodes", len(agent.network))
            
            st.write(f"**Starting Point:** {res['start']}")
            st.write(f"**Destination:** {res['end']}")

# 5. Data Transparency (Plan A: Data Analytics)
st.write("---")
with st.expander("🔍 View Raw Delhivery Logistics Master Data"):
    if not agent.df.empty:
        st.write("Below is the sampled dataset used for the graph network:")
        st.dataframe(agent.df[['source_name', 'destination_name', 'osrm_distance', 'osrm_time']].head(15))
    else:
        st.warning("No data found. Ensure 'delhivery_small.csv' is in your GitHub repository.")

# Footer
st.caption("Developed for SAP Code Unnati 2.0 | Agentic AI Supply Chain Project")
