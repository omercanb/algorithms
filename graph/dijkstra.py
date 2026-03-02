import heapq
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class ShortestPathItem:
    vertex: Any = field(compare=False)
    distance: Any

# O(E lgV)
def dijkstra(graph, start):
    distances = {v: float('inf') for v in graph}
    distances[start] = 0
    heap = [ShortestPathItem(start, 0)]
    predecessors = {}
    while heap:
        cur = heapq.heappop(heap)
        if cur.distance > distances[cur.vertex]:
            continue
        for neighbor, weight in graph[cur.vertex]:
            updated_distance = cur.distance + weight
            if updated_distance < distances[neighbor]:
                heapq.heappush(heap, ShortestPathItem(neighbor, updated_distance))
                distances[neighbor] = updated_distance
                predecessors[neighbor] = cur.vertex
    return distances, predecessors

graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 5), ('D', 10)],
    'C': [('E', 3)],
    'D': [('F', 11)],
    'E': [('D', 4)],
    'F': []
}

distances, predecessors = dijkstra(graph, 'A')
print(graph)
print(distances)
print(predecessors)
