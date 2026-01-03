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
                
            if src not in graph: graph[src] = {}
            graph[src][dest] = weight
        return graph

    def process_incident(self, report):
        if not self.network:
            return {"status": "ERROR", "reasoning": "Database not loaded."}

        temp_network = self.network.copy()
        status = "NORMAL"
        reasoning = "All Indian logistics hubs operating within standard OSRM parameters."
        
        # Agentic Reasoning Keywords
        keywords = ["storm", "blocked", "strike", "flood", "delay", "rain", "accident"]
        
        if any(word in report.lower() for word in keywords):
            status = "REROUTED"
            reasoning = "AI Reasoning: Incident detected. Applying penalty weights to affected nodes."
            
            # Penalize routes that match the incident location
            for src in temp_network:
                for dest in list(temp_network[src].keys()):
                    if any(word.lower() in dest.lower() for word in report.split()):
                        temp_network[src][dest] += 2000 # Force the optimizer to find a new path
        
        # Select start/end nodes from the dataset
        all_cities = list(self.network.keys())
        start_node = all_cities[0]
        end_node = list(self.network[start_node].keys())[0] if self.network[start_node] else all_cities[-1]
        
        # Trigger Dijkstra Optimizer
        cost, path = get_optimal_route(temp_network, start_node, end_node)
        
        return {
            "status": status, 
            "path": path, 
            "cost": round(cost, 2), 
            "start": start_node, 
            "end": end_node,
            "reasoning": reasoning
        }
