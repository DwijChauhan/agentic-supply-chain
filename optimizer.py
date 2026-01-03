import heapq

def get_optimal_route(graph, start, end):
    """
    Core DP Optimizer: Calculates shortest path and total distance.
    """
    if start not in graph:
        return 0, [start, "Origin not found in network"]

    # Initialize distances for ALL nodes mentioned in the graph
    distances = {node: float('inf') for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            if neighbor not in distances:
                distances[neighbor] = float('inf')
    
    distances[start] = 0
    pq = [(0, start, [start])] # (distance, current_node, path_history)

    while pq:
        curr_dist, curr_node, path = heapq.heappop(pq)

        if curr_node == end:
            return curr_dist, path

        if curr_dist > distances.get(curr_node, float('inf')):
            continue

        if curr_node in graph:
            for neighbor, weight in graph[current_node].items():
                new_dist = curr_dist + weight
                if new_dist < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))

    return 0, [start, "No viable connection found between these Gujarat hubs"]
