import heapq

def get_optimal_route(graph, start, end):
    # If the start city isn't in our source list, we can't begin
    if start not in graph:
        return 0, [start, "Source Not Found"]

    # Initialize distances for EVERY node mentioned in the graph (source or dest)
    distances = {node: float('inf') for node in graph}
    for nodes in graph.values():
        for neighbor in nodes:
            if neighbor not in distances:
                distances[neighbor] = float('inf')
    
    distances[start] = 0
    pq = [(0, start, [start])]

    while pq:
        current_distance, current_node, path = heapq.heappop(pq)

        if current_node == end:
            return current_distance, path

        if current_distance > distances.get(current_node, float('inf')):
            continue

        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_distance + weight
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor, path + [neighbor]))

    return 0, [start, "No Connected Path Found"]
