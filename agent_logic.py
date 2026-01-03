import pandas as pd
import os
import streamlit as st
from optimizer import get_optimal_route

class SupplyChainAgent:
    def __init__(self):
        # RELATIVE PATH for GitHub/Streamlit Cloud
        file_name = 'delhivery_small.csv'
        
        if os.path.exists(file_name):
            try:
                # Loading the sampled Delhivery data
                self.raw_data = pd.read_csv(file_name)
                self.df = self.raw_data.dropna(subset=['source_name', 'destination_name'])
                self.network = self.build_network()
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
                self.df = pd.DataFrame()
                self.network = {}
        else:
            st.error(f"Critical Error: '{file_name}' not found on GitHub!")
            self.df = pd.DataFrame()
            self.network = {}

    def build_network(self):
        graph = {}
        for _, row in self.df.iterrows():
            src = str(row['source_name']).strip()
            dest = str(row['destination_name']).strip()
            try:
                # Using OSRM Distance as the mathematical weight
                weight = float(row['osrm_distance'])
            except:
                weight = 10.0
                
            if src not in graph: 
                graph[src] = {}
            graph[src][dest] = weight
        return graph

    # FIXED: This function is now properly indented inside the class
    def process_incident(self, report):
        if not self.network:
            return {
                "status": "ERROR", 
                "path": ["No Data"], 
                "cost": 0, 
                "start": "N/A", 
                "end": "N/A", 
                "reasoning": "CSV not loaded."
            }

        # Use a deep copy to avoid modifying the original network permanently
        import copy
        temp_network = copy.deepcopy(self.network)
        status = "NORMAL"
        reasoning = "All Indian hubs operating normally."
        
        # Keyword reasoning logic
        report_lower = report.lower()
        if any(word in report_lower for word in ["storm", "rain", "block", "delay", "flood"]):
            status = "REROUTED"
            reasoning = "Incident detected. Agent applying penalty weights to affected hubs."
            
            # Agentic Logic: Scan all routes and penalize those matching words in the report
            report_words = [w for w in report_lower.split() if len(w) > 3]
            for src in temp_network:
                for dest in list(temp_network[src].keys()):
                    if any(word in dest.lower() or word in src.lower() for word in report_words):
                        temp_network[src][dest] += 5000  # Apply heavy penalty to force reroute

        # SAFE CITY SELECTION
        cities = list(self.network.keys())
        if len(cities) < 2:
            return {
                "status": "ERROR", 
                "path": ["Missing Cities"], 
                "cost": 0, 
                "start": "N/A", 
                "end": "N/A", 
                "reasoning": "Dataset too small to form a network."
            }
            
        # Start at the first city in the CSV
        start = cities[0]
        
        # Look for a destination that is actually a known source (hubs that have outgoing routes)
        # This prevents the KeyError: 'City Name' in optimizer.py
        possible_ends = [c for c in self.network[start].keys() if c in self.network]
        
        if possible_ends:
            end = possible_ends[0]
        else:
            # Fallback to the last available source node
            end = cities[-1]
        
        # Trigger the Dijkstra Optimizer
        cost, path = get_optimal_route(temp_network, start, end)
        
        return {
            "status": status, 
            "path": path, 
            "cost": round(cost, 2), 
            "start": start, 
            "end": end, 
            "reasoning": reasoning
        }
