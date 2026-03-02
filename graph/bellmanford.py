
def bellmanford(graph, start):
    distances = {v: float('inf') for v in graph}
    distances[start] = 0
    predecessors = {}
    negative_cycles = []
    for i in range(len(graph) - 1):
        for cur in graph:
            for neighbor, weight in graph[cur]:
                distance = distances[cur] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = cur

    for cur in graph:
        for neighbor, weight in graph[cur]:
            distance = distances[cur] + weight
            # Negative cycle
            if distance < distances[neighbor]:
                negative_cycles.append(neighbor)
                distances[neighbor] = distance
                predecessors[neighbor] = cur
    return distances, predecessors, negative_cycles


graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 5), ('D', 10)],
    'C': [('E', 3)],
    'D': [('F', 11)],
    'E': [('D', 4)],
    'F': []
}

graph2 = {
    'A' : [('B', 2)],
    'B' : [('C', 3)],
    'C' : [('A', -6), ('D', 2)],
    'D' : [('E', )]

}

distances, predecessors, negative_cycles = bellmanford(graph2, 'A')
print(graph)
print(distances)
print(predecessors)
print(negative_cycles)

