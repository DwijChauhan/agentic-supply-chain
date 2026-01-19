import heapq

def get_optimal_route(graph, start, end, penalties=None):
    """Calculates the best path while accounting for real-time risk penalties."""
    if penalties is None: penalties = {}
    if start not in graph:
        return 0, [start, "Origin not in network"]

    # Initialize distances for all nodes in the network
    distances = {node: float('inf') for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            distances.setdefault(neighbor, float('inf'))
    
    distances[start] = 0
    pq = [(0, start, [start])]

    while pq:
        curr_dist, curr_node, path = heapq.heappop(pq)

        if curr_node == end:
            return curr_dist, path

        if curr_dist > distances.get(curr_node, float('inf')):
            continue

        for neighbor, weight in graph.get(curr_node, {}).items():
            # Apply agentic penalty if the destination or source is risky
            risk_penalty = penalties.get(neighbor, 0) + penalties.get(curr_node, 0)
            new_dist = curr_dist + weight + risk_penalty
            
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))

    return 0, [start, "No connection found"]
