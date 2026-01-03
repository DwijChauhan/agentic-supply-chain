import heapq

def get_optimal_route(graph, start, end):
    """
    Finds the shortest path between start and end nodes using Dijkstra's Algorithm.
    Returns (distance, path_list).
    """
    # 1. Edge Case: Start city is not in our source database
    if start not in graph:
        return 0, [start, "Source Not Found in Dataset"]

    # 2. Initialization:
    # Set distance to infinity for every node in the graph (source or destination)
    # This prevents the 'KeyError' during relaxation
    distances = {node: float('inf') for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            if neighbor not in distances:
                distances[neighbor] = float('inf')
    
    distances[start] = 0
    priority_queue = [(0, start, [start])] # (current_distance, current_node, path_history)

    while priority_queue:
        # Extract the node with the smallest tentative distance
        current_distance, current_node, path = heapq.heappop(priority_queue)

        # 3. Found the destination!
        if current_node == end:
            return current_distance, path

        # If we already found a shorter path to this node, skip it
        if current_distance > distances.get(current_node, float('inf')):
            continue

        # 4. Explore Neighbors:
        # Check all connections from the current hub
        if current_node in graph:
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight
                
                # Relaxation: If a shorter path is found, update and push to queue
                if distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor, path + [neighbor]))

    # 5. Return fallback if no path exists between the selected hubs
    return 0, [start, "No viable path found between these hubs"]
