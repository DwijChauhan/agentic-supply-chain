import pandas as pd
import os
import streamlit as st
import copy
from optimizer import get_optimal_route

class SupplyChainAgent:
    def __init__(self):
        # Using your new Gujarat-specific dataset
        file_name = 'delhivery_gujarat.csv'
        if os.path.exists(file_name):
            try:
                raw_df = pd.read_csv(file_name).dropna(subset=['source_name', 'destination_name'])
                # Data Cleaning: Remove "(Gujarat)" for a cleaner UI
                raw_df['source_name'] = raw_df['source_name'].str.replace(' (Gujarat)', '', regex=False)
                raw_df['destination_name'] = raw_df['destination_name'].str.replace(' (Gujarat)', '', regex=False)
                self.df = raw_df
                self.network = self.build_network()
            except:
                self.df, self.network = pd.DataFrame(), {}
        else:
            self.df, self.network = pd.DataFrame(), {}

    def build_network(self):
        graph = {}
        for _, row in self.df.iterrows():
            src, dest = str(row['source_name']), str(row['destination_name'])
            weight = float(row['osrm_distance'])
            if src not in graph: graph[src] = {}
            graph[src][dest] = weight
        return graph

    def process_incident(self, report, start_node, end_node):
        # 1. BASELINE: Calculate standard distance before any disruption
        base_cost, _ = get_optimal_route(self.network, start_node, end_node)
        
        # 2. PERCEPTION: Calculate Risk Score
        risk_score = 0
        keywords = {"flood": 5, "storm": 4, "block": 5, "rain": 2, "delay": 1, "accident": 3}
        for word, score in keywords.items():
            if word in report.lower(): risk_score += score
        risk_score = min(risk_score, 10)

        # 3. REASONING: Apply penalties if risk is detected
        temp_network = copy.deepcopy(self.network)
        status = "NORMAL"
        if risk_score > 0:
            status = "REROUTED"
            report_words = [w for w in report.lower().split() if len(w) > 3]
            for src in temp_network:
                for dest in list(temp_network[src].keys()):
                    if any(w in dest.lower() or w in src.lower() for w in report_words):
                        temp_network[src][dest] += 2000 # Penalty weight

        # 4. ACTION: Get the new safe route
        opt_cost, opt_path = get_optimal_route(temp_network, start_node, end_node)

        return {
            "base_cost": round(base_cost, 2),
            "opt_cost": round(opt_cost, 2) if opt_cost < 1000 else round(base_cost, 2),
            "risk_level": risk_score,
            "path": opt_path,
            "status": status,
            "start": start_node,
            "end": end_node,
            "reasoning": f"Agent detected {risk_score}/10 risk factors. Rerouting initiated." if risk_score > 0 else "Routes verified safe."
        }
