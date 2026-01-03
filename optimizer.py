import heapq

def get_optimal_route(graph, start, end):
    if start not in graph:
        return 0, [start, "Not found in dataset"]

    # Initialize all reachable nodes with infinity
    distances = {node: float('inf') for node in graph}
    for nodes in graph.values():
        for neighbor in nodes:
            if neighbor not in distances:
                distances[neighbor] = float('inf')
    
    distances[start] = 0
    pq = [(0, start, [start])]

    while pq:
        current_dist, current_node, path = heapq.heappop(pq)

        if current_node == end:
            return current_dist, path

        if current_dist > distances.get(current_node, float('inf')):
            continue

        for neighbor, weight in graph.get(current_node, {}).items():
            dist = current_dist + weight
            if dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = dist
                heapq.heappush(pq, (dist, neighbor, path + [neighbor]))

    return 0, [start, "No direct or indirect connection found"]
