import pandas as pd
import os
import streamlit as st
import copy
from optimizer import get_optimal_route

class SupplyChainAgent:
    def __init__(self):
        file_name = 'delhivery_gujarat.csv'
        if os.path.exists(file_name):
            try:
                raw_df = pd.read_csv(file_name).dropna(subset=['source_name', 'destination_name'])
                # Clean names: "City (Gujarat)" -> "City"
                raw_df['source_name'] = raw_df['source_name'].str.replace(' (Gujarat)', '', regex=False)
                raw_df['destination_name'] = raw_df['destination_name'].str.replace(' (Gujarat)', '', regex=False)
                self.df = raw_df
                self.network = self.build_network()
            except Exception as e:
                st.error(f"Data Loading Error: {e}")
                self.df, self.network = pd.DataFrame(), {}
        else:
            self.df, self.network = pd.DataFrame(), {}

    def build_network(self):
        graph = {}
        for _, row in self.df.iterrows():
            src = str(row['source_name']).strip()
            dest = str(row['destination_name']).strip()
            weight = float(row['osrm_distance']) if not pd.isna(row['osrm_distance']) else 10.0
            if src not in graph: 
                graph[src] = {}
            graph[src][dest] = weight
        return graph

    def process_incident(self, report, start_node, end_node):
        if not self.network:
            return {"status": "ERROR", "reasoning": "Data missing.", "path": [], "base_cost": 0, "opt_cost": 0, "risk_level": 0}

        # 1. Baseline: Standard distance
        base_cost, _ = get_optimal_route(self.network, start_node, end_node)
        
        # 2. Risk Score Calculation
        risk_score = 0
        keywords = {"flood": 5, "storm": 4, "block": 5, "rain": 2, "delay": 1, "accident": 3}
        for word, score in keywords.items():
            if word in report.lower(): 
                risk_score += score
        risk_score = min(risk_score, 10)

        # 3. Agentic Rerouting
        temp_network = copy.deepcopy(self.network)
        status = "NORMAL"
        if risk_score > 0:
            status = "REROUTED"
            words = [w for w in report.lower().split() if len(w) > 3]
            for src in temp_network:
                for dest in list(temp_network[src].keys()):
                    if any(w in dest.lower() or w in src.lower() for w in words):
                        temp_network[src][dest] += 2000

        opt_cost, opt_path = get_optimal_route(temp_network, start_node, end_node)

        return {
            "base_cost": round(base_cost, 2),
            "opt_cost": round(opt_cost, 2),
            "risk_level": risk_score,
            "path": opt_path,
            "status": status,
            "start": start_node,
            "end": end_node,
            "reasoning": f"Agent detected {risk_score}/10 risk factors." if risk_score > 0 else "Routes safe."
        }
