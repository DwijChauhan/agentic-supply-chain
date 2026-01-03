import heapq

def get_optimal_route(graph, start, end):
    """
    Core Optimization Engine: Dijkstra's Algorithm.
    This provides the mathematical 'Action' for the Agentic AI.
    """
    # Safety Check: If nodes don't exist in our CSV data
    if start not in graph or end not in graph:
        return 0, [start, "No viable path found in dataset"]

    # Initialize distances and priority queue
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    pq = [(0, start, [start])]

    while pq:
        (current_distance, current_node, path) = heapq.heappop(pq)

        # Optimization: If we found the target node
        if current_node == end:
            return current_distance, path

        # If we found a longer path than already recorded, skip
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors (connected hubs)
        if current_node in graph:
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                # If this new path is shorter, record it and add to queue
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor, path + [neighbor]))

    return 0, [start, "Destination unreachable in current network"]
