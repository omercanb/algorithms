def dfs(G):
    def dfs_visit(u):
        visited[u] = True
        for v in G[u]:
            if visited[v]:
                continue
            dfs_visit(v)
        nonlocal t
        t += 1
        finishing[u] = t
    visited = {u: False for u in G}
    finishing = {}
    t = 0
    for u in G:
        if visited[u]:
            continue
        dfs_visit(u)
    return finishing

def strongly_connected_components(G):
    finishing_times = dfs(G)
    G_T = transpose(G)
    # Order vertices by finishing times
    order = {}
    for u in finishing_times:
        order[finishing_times[u]] = u
    order = list(reversed(order.values()))
    components = dfs_scc(G_T, order)
    return components

def dfs_scc(G, order):
    visited = {u: False for u in G}
    components = []
    component_num = {u: None for u in G}
    component_graph = {}
    def dfs_visit(u):
        visited[u] = True
        components[-1].add(u)

        u_num = len(components)
        component_num[u] = u_num

        if u_num not in component_graph:
            component_graph[u_num] = set()

        for v in G[u]:
            if visited[v]:
                if component_num[u] != component_num[v]:
                    print(component_num[v])
                    component_graph[u_num].add(component_num[v])
                continue
            dfs_visit(v)

    for u in order:
        if visited[u]:
            continue
        # Add a set to put this scc's vertices in
        components.append(set([u]))
        dfs_visit(u)

    components = {i + 1: component for (i, component) in enumerate(components)}
    return components, component_graph, component_num

def transpose(G):
    G_T = {u: [] for u in G}
    for u in G:
        for v in G[u]:
            G_T[v].append(u)
    return G_T

graph = {
    'q': ['s', 't', 'w'],
    's': ['v'],
    'v': ['w'],
    'w': ['s'],
    't': ['x', 'y'],
    'x': ['z'],
    'z': ['x'],
    'y': ['q'],
    'r': ['u', 'y'],
    'u': ['y'],
}

dfs(graph)
print(transpose(graph))
print(strongly_connected_components(graph))
