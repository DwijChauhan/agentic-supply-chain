import heapq

def get_optimal_route(graph, start, end):
    """
    Finds the shortest path between start and end nodes using Dijkstra's Algorithm.
    This is a core Dynamic Programming approach for path optimization.
    """
    # If the start or end city isn't in our Delhivery dataset, return a fallback
    if start not in graph or end not in graph:
        return 0, [start, end]

    # distances stores the minimum distance to each node
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    
    # priority queue to store (distance, current_node, path)
    pq = [(0, start, [start])]

    while pq:
        current_distance, current_node, path = heapq.heappop(pq)

        # If we reached the destination, return the result
        if current_node == end:
            return current_distance, path

        # If the distance in the queue is greater than the known shortest, skip
        if current_distance > distances[current_node]:
            continue

        # Check neighbors
        if current_node in graph:
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                # If a shorter path to neighbor is found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor, path + [neighbor]))

    return float('infinity'), []
