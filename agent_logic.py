import pandas as pd
import os
import streamlit as st
from optimizer import get_optimal_route

class SupplyChainAgent:
    def __init__(self):
        # Use relative path for Streamlit Cloud compatibility
        file_name = 'delhivery_small.csv'
        
        if os.path.exists(file_name):
            self.raw_data = pd.read_csv(file_name)
            # Clean data and take a sample for the graph
            self.df = self.raw_data.dropna(subset=['source_name', 'destination_name'])
            self.network = self.build_network()
        else:
            self.df = pd.DataFrame()
            self.network = {}

    def build_network(self):
        graph = {}
        # Building the graph from Delhivery road distances
        for _, row in self.df.iterrows():
            src, dest = str(row['source_name']), str(row['destination_name'])
            weight = float(row['osrm_distance'])
            if src not in graph: graph[src] = {}
            graph[src][dest] = weight
        return graph

    def process_incident(self, report):
        """Agentic Reasoning: Interprets the report and adjusts the DP Optimizer"""
        temp_network = self.network.copy()
        status = "NORMAL"
        reasoning = "All routes operating at optimal OSRM distances."
        
        # Logic: If disruption mentioned, penalize those specific nodes
        disruption_keywords = ["storm", "blocked", "strike", "flood", "delay"]
        if any(word in report.lower() for word in disruption_keywords):
            status = "REROUTED"
            reasoning = f"Disruption detected via Agent Reasoning. Increasing weight for affected Indian hubs."
            for src in temp_network:
                for dest in temp_network[src]:
                    # Example: If report mentions 'Anand', avoid that route
                    if "Anand" in dest or "Mumbai" in dest:
                        temp_network[src][dest] += 1000  # Dynamic Penalty
        
        # Select two points existing in the dataset
        cities = list(self.network.keys())
        start, end = cities[0], cities[min(15, len(cities)-1)]
        
        cost, path = get_optimal_route(temp_network, start, end)
        
        return {
            "status": status, 
            "path": path, 
            "cost": round(cost, 2), 
            "start": start, 
            "end": end,
            "reasoning": reasoning
        }
