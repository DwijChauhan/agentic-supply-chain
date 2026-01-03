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
        # ... (previous keyword reasoning code) ...

        # Safety Check: If the selected start_node is not in our network, 
        # the optimizer will fail. We must ensure it exists.
        if start_node not in self.network:
             return {"status": "ERROR", "reasoning": f"Node {start_node} not in network."}

        # Trigger the hardened optimizer
        cost, path = get_optimal_route(temp_network, start_node, end_node)
        
        return {
            "base_cost": round(base_cost, 2),
            "opt_cost": round(cost, 2),
            "risk_level": risk_score,
            "path": path,
            "status": status,
            "start": start_node,
            "end": end_node,
            "reasoning": reasoning
        }
