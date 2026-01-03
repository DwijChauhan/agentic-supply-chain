import pandas as pd
import os
import streamlit as st
from optimizer import get_optimal_route

class SupplyChainAgent:
    def __init__(self):
        # 1. FIX: Use only the filename for GitHub/Streamlit Cloud compatibility
        file_name = 'delhivery_small.csv'
        
        if os.path.exists(file_name):
            try:
                self.raw_data = pd.read_csv(file_name)
                # 2. FIX: Handle potential NaN values in city names
                self.df = self.raw_data.dropna(subset=['source_name', 'destination_name'])
                self.network = self.build_network()
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
                self.df = pd.DataFrame()
                self.network = {}
        else:
            # This helps you debug if the file isn't found on GitHub
            st.error(f"Critical Error: '{file_name}' not found in the root directory!")
            self.df = pd.DataFrame()
            self.network = {}

    def build_network(self):
        graph = {}
        # 3. FIX: Ensure data types are correct for the optimizer
        for _, row in self.df.iterrows():
            src = str(row['source_name']).strip()
            dest = str(row['destination_name']).strip()
            # Use 'osrm_distance' as the mathematical weight
            try:
                weight = float(row['osrm_distance'])
            except:
                weight = 10.0 # Fallback weight
                
            if src not in graph: graph[src] = {}
            graph[src][dest] = weight
        return graph

    def process_incident(self, report):
        """Agentic Reasoning: Interprets reports and triggers DP Optimizer"""
        # Safety Check: If data didn't load, return early
        if not self.network:
            return {"status": "ERROR", "path": ["No Data"], "cost": 0, "start": "N/A", "end": "N/A", "reasoning": "Database not loaded."}

        temp_network = self.network.copy()
        status = "NORMAL"
        reasoning = "All Indian logistics hubs operating within standard OSRM parameters."
        
        # 4. FIX: Expanded keywords for better 'Agentic' feel
        disruption_keywords = ["storm", "blocked", "strike", "flood", "delay", "rain", "accident"]
        
        if any(word in report.lower() for word in disruption_keywords):
            status = "REROUTED"
            reasoning = "AI Reasoning: Incident detected in report. Applying penalty weights to affected nodes."
            
            # Search through the network to apply penalties
            for src in temp_network:
                for dest in list(temp_network[src].keys()):
                    # If the report mentions a location found in our data
                    # e.g., If user types "Rain in Anand" and destination is "Anand_VUNagar_DC"
                    if any(word.lower() in dest.lower() for word in report.split()):
                        temp_network[src][dest] += 2000 # Significant penalty to force reroute
        
        # 5. FIX: Dynamic selection of Start and End nodes from available data
        all_cities = list(self.network.keys())
        start_node = all_cities[0]
        
        # Try to find a connected destination, otherwise pick another city
        if self.network[start_node]:
            end_node = list(self.network[start_node].keys())[0]
        else:
            end_node = all_cities[-1]
        
        # Trigger the Optimizer (Dijkstra)
        cost, path = get_optimal_route(temp_network, start_node, end_node)
        
        return {
            "status": status, 
            "path": path, 
            "cost": round(cost, 2), 
            "start": start_node, 
            "end": end_node,
            "reasoning": reasoning
        }
