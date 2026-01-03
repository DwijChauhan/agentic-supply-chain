import heapq

def get_optimal_route(graph, start, end):
    if start not in graph:
        return 0, [start, "Source not in data"]

    # Initialize distances for all nodes in the graph AND their neighbors
    distances = {}
    for node in graph:
        distances[node] = float('infinity')
        for neighbor in graph[node]:
            distances[neighbor] = float('infinity')
            
    distances[start] = 0
    pq = [(0, start, [start])]

    while pq:
        current_distance, current_node, path = heapq.heappop(pq)

        if current_node == end:
            return current_distance, path

        if current_distance > distances.get(current_node, float('inf')):
            continue

        if current_node in graph:
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight
                
                # SAFE CHECK: Ensure neighbor exists in distances
                if neighbor not in distances:
                    distances[neighbor] = float('infinity')
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor, path + [neighbor]))

    return 0, [start, "No path found"]
