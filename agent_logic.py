import pandas as pd
import os
import streamlit as st
import copy
from optimizer import get_optimal_route

class SupplyChainAgent:
    def __init__(self):
        file_name = 'delhivery_small.csv'
        if os.path.exists(file_name):
            try:
                self.raw_data = pd.read_csv(file_name)
                self.df = self.raw_data.dropna(subset=['source_name', 'destination_name'])
                self.network = self.build_network()
            except Exception as e:
                st.error(f"Error: {e}")
                self.network = {}
        else:
            self.network = {}

    def build_network(self):
        graph = {}
        for _, row in self.df.iterrows():
            src, dest = str(row['source_name']).strip(), str(row['destination_name']).strip()
            weight = float(row['osrm_distance']) if not pd.isna(row['osrm_distance']) else 10.0
            if src not in graph: graph[src] = {}
            graph[src][dest] = weight
        return graph

    # FIXED: Accepts optional start/end nodes from the UI dropdowns
    def process_incident(self, report, start_node=None, end_node=None):
        if not self.network:
            return {"status": "ERROR", "reasoning": "Data missing.", "path": [], "cost": 0}

        temp_network = copy.deepcopy(self.network)
        status = "NORMAL"
        reasoning = "Operating within standard OSRM parameters."
        
        # Agentic Rerouting Logic
        report_lower = report.lower()
        keywords = ["storm", "rain", "block", "delay", "flood"]
        if any(word in report_lower for word in keywords):
            status = "REROUTED"
            reasoning = "Incident detected. Applying penalty weights to force reroute."
            words = [w for w in report_lower.split() if len(w) > 3]
            for src in temp_network:
                for dest in list(temp_network[src].keys()):
                    if any(w in dest.lower() or w in src.lower() for w in words):
                        temp_network[src][dest] += 5000

        # Logic to handle custom hub selection
        cities = list(self.network.keys())
        start = start_node if start_node else cities[0]
        
        if end_node:
            end = end_node
        else:
            # Fallback to first connected destination
            end = list(self.network[start].keys())[0] if self.network[start] else cities[-1]
        
        cost, path = get_optimal_route(temp_network, start, end)
        
        return {
            "status": status, "path": path, "cost": round(cost, 2), 
            "start": start, "end": end, "reasoning": reasoning
        }
