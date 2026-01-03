import heapq

def get_optimal_route(graph, start, end):
    if start not in graph or end not in graph:
        return 0, [start, "Path not found"]

    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    pq = [(0, start, [start])]

    while pq:
        (current_distance, current_node, path) = heapq.heappop(pq)

        if current_node == end:
            return current_distance, path

        if current_distance > distances[current_node]:
            continue

        if current_node in graph:
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor, path + [neighbor]))

    return 0, [start, "No viable connection"]
