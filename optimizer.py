import heapq

def get_optimal_route(graph, start, end):
    """
    Finds the shortest path using Dijkstra's Algorithm with KeyError protection.
    """
    if start not in graph:
        return 0, [start, "Origin not in dataset"]

    # Initialize distances for all nodes found in the graph (sources and neighbors)
    # This prevents the KeyError by ensuring every node has a 'float(inf)' starting distance.
    distances = {node: float('inf') for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            if neighbor not in distances:
                distances[neighbor] = float('inf')
    
    distances[start] = 0
    pq = [(0, start, [start])]

    while pq:
        current_distance, current_node, path = heapq.heappop(pq)

        if current_node == end:
            return current_distance, path

        # Use .get() to safely check the current recorded distance
        if current_distance > distances.get(current_node, float('inf')):
            continue

        # Check neighbors safely
        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_distance + weight
            
            # Update distance if a shorter path is found
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor, path + [neighbor]))

    return 0, [start, "No viable connection found"]
