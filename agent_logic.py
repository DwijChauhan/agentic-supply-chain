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
            return {"status": "ERROR", "path": ["No Data"], "cost": 0, "start": "N/A", "end": "N/A", "reasoning": "CSV not loaded."}

        temp_network = self.network.copy()
        status = "NORMAL"
        reasoning = "All Indian hubs operating normally."
        
        # Keyword reasoning
        if any(word in report.lower() for word in ["storm", "rain", "block", "delay"]):
            status = "REROUTED"
            reasoning = "Incident detected. Agent applying penalty weights."
            for src in temp_network:
                for dest in list(temp_network[src].keys()):
                    if any(word.lower() in dest.lower() for word in report.split() if len(word) > 3):
                        temp_network[src][dest] += 5000

        # SAFE CITY SELECTION
        cities = list(self.network.keys())
        if len(cities) < 2:
            return {"status": "ERROR", "path": ["Missing Cities"], "cost": 0, "start": "N/A", "end": "N/A", "reasoning": "Dataset too small."}
            
        start = cities[0]
        # Pick an end city that is actually connected to the start city
        possible_ends = list(self.network[start].keys())
        end = possible_ends[0] if possible_ends else cities[-1]
        
        cost, path = get_optimal_route(temp_network, start, end)
        return {"status": status, "path": path, "cost": round(cost, 2), "start": start, "end": end, "reasoning": reasoning}
