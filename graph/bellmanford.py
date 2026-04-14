
def bellmanford(G, s):
    d = {u: float('inf') for u in G}
    d[s] = 0
    pred = {u: None for u in G}
    V = len(G)
    for _ in range(V - 1):
        # Iterate over all edges
        for u in G:
            for v, w in G[u]:
                if d[v] > d[u] + w:
                    d[v] = d[u] + w
                    pred[v] = u
    neg_cycle = False
    for u in G:
        for v, w in G[u]:
            if d[v] > d[u] + w:
                # Set all vertices on the path from s to v to -inf distance
                cur = v
                while cur != s:
                    # Has been visited before
                    if d[cur] == float('-inf'):
                        break
                    d[cur] = float('-inf')
                    cur = pred[cur]
                neg_cycle = True
    if neg_cycle:
        return False, d, pred

    return True, d, pred

graph = {
    's': [('t', 6), ('y', 7)],
    't': [('x', 5), ('y', 8), ('z', -4)],
    'x': [('t', -2)],
    'y': [('x', -3), ('z', 9)],
    'z': [('x', 4), ('s', 2)],
}

valid, distances, predecessors = bellmanford(graph, 's')
print(distances)
print(predecessors)
print(valid)

