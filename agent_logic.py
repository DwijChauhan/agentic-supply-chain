import pandas as pd
import os
import streamlit as st
from optimizer import get_optimal_route

class SupplyChainAgent:
    def __init__(self):
        file_name = 'delhivery_gujarat.csv'
        if os.path.exists(file_name):
            try:
                raw_df = pd.read_csv(file_name).dropna(subset=['source_name', 'destination_name'])
                # Clean city names by removing the (Gujarat) suffix for better keyword matching
                raw_df['source_name'] = raw_df['source_name'].str.replace(' (Gujarat)', '', regex=False)
                raw_df['destination_name'] = raw_df['destination_name'].str.replace(' (Gujarat)', '', regex=False)
                self.df = raw_df
                self.network = self.build_network()
            except Exception as e:
                st.error(f"Data Loading Error: {e}")
                self.df, self.network = pd.DataFrame(), {}
        else:
            st.error(f"Critical: File '{file_name}' not found!")
            self.df, self.network = pd.DataFrame(), {}

    def build_network(self):
        graph = {}
        for _, row in self.df.iterrows():
            src, dest = str(row['source_name']).strip(), str(row['destination_name']).strip()
            weight = float(row['osrm_distance']) if not pd.isna(row['osrm_distance']) else 10.0
            if src not in graph: graph[src] = {}
            graph[src][dest] = weight
        return graph

    def process_incident(self, report, start_node, end_node):
        # 1. Baseline: Standard shortest path
        base_cost, _ = get_optimal_route(self.network, start_node, end_node)
        
        # 2. Agent Reasoning: Detect risk keywords
        risk_score = 0
        keywords = {"flood": 5, "storm": 4, "block": 5, "rain": 2, "delay": 1, "accident": 3}
        for word, score in keywords.items():
            if word in report.lower(): 
                risk_score += score
        risk_score = min(risk_score, 10)

        # 3. Decision Logic: Apply penalties to mentioned areas
        penalties = {}
        reasoning = "Conditions normal. Route optimized for distance."
        
        if risk_score > 0:
            # Extract meaningful words to identify hubs to avoid
            impact_words = [w for w in report.lower().split() if len(w) > 3]
            for node in self.network.keys():
                if any(k in node.lower() for k in impact_words):
                    penalties[node] = 5000  # High penalty forces the path elsewhere
            reasoning = f"Risk Level {risk_score}/10: Rerouting to avoid hubs mentioned in: '{report}'."

        opt_cost, opt_path = get_optimal_route(self.network, start_node, end_node, penalties=penalties)

        return {
            "base_cost": round(base_cost, 2),
            "opt_cost": round(opt_cost, 2),
            "path": opt_path,
            "risk_level": risk_score,
            "reasoning": reasoning
        }
