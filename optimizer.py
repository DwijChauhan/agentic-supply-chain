import heapq
def get_optimal_route(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start, [])]
    while priority_queue:
        dist, current, path = heapq.heappop(priority_queue)
        if current == end: return dist, path + [current]
        for neighbor, weight in graph[current].items():
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(priority_queue, (new_dist, neighbor, path + [current]))
    return float('inf'), []