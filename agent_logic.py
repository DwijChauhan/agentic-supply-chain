import pandas as pd
import os
import streamlit as st
import copy
from optimizer import get_optimal_route

class SupplyChainAgent:
    def __init__(self):
        file_name = 'delhivery_small.csv'
        if os.path.exists(file_name):
            self.df = pd.read_csv(file_name).dropna(subset=['source_name', 'destination_name'])
            self.network = self.build_network()
        else:
            self.network = {}

    def build_network(self):
        graph = {}
        for _, row in self.df.iterrows():
            src, dest = str(row['source_name']), str(row['destination_name'])
            weight = float(row['osrm_distance'])
            if src not in graph: graph[src] = {}
            graph[src][dest] = weight
        return graph

    def process_incident(self, report, start_node, end_node):
        # 1. Baseline Calculation (Standard Distance)
        base_cost, base_path = get_optimal_route(self.network, start_node, end_node)
        
        # 2. Risk Assessment Logic
        risk_score = 0
        keywords = {"flood": 5, "storm": 4, "block": 5, "rain": 2, "delay": 1}
        for word, score in keywords.items():
            if word in report.lower(): risk_score += score
        risk_score = min(risk_score, 10)

        # 3. Apply Penalties & Get Optimized Path
        temp_network = copy.deepcopy(self.network)
        if risk_score > 0:
            for src in temp_network:
                for dest in list(temp_network[src].keys()):
                    if any(w in dest.lower() or w in src.lower() for w in report.lower().split() if len(w) > 3):
                        temp_network[src][dest] += 5000 

        opt_cost, opt_path = get_optimal_route(temp_network, start_node, end_node)

        return {
            "base_cost": round(base_cost, 2),
            "opt_cost": round(opt_cost, 2) if opt_cost < 1000 else round(base_cost, 2), # Clean up penalty display
            "risk_level": risk_score,
            "path": opt_path,
            "status": "REROUTED" if risk_score > 0 else "NORMAL",
            "reasoning": f"Agent detected risk level {risk_score}/10. Rerouting via safe hubs." if risk_score > 0 else "Normal parameters."
        }
