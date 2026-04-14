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
    # The components parent
    # The returned graph will be a graph of the parents
    parent = {}
    components = {}
    component_graph = {}
    def dfs_visit(u):
        visited[u] = True

        # Put this node into its component
        parent[u] = cur_parent
        components[cur_parent].append(u)

        # Check the connections from this node to other components AND continue dfs
        for v in G[u]:
            if visited[v]:
                if parent[u] != parent[v]:
                    # This a previous SCC
                    component_graph[cur_parent].add(parent[v])
                continue
            dfs_visit(v)

    for u in order:
        if visited[u]:
            continue
        cur_parent = u
        components[u] = []
        component_graph[u] = set()
        dfs_visit(u)
    component_graph = transpose(component_graph)
    return components, component_graph

def scc_minimal_edge_set(G):
    components, component_graph = strongly_connected_components(G)
    # Solution
    # For each component: Add edges that form the basic cycle that goes through all vertices
    # Between each component: Add the edge in the component graph
    minimal_edge_set = {u: [] for u in G}
    for parent, component in components.items():
        # Forming the simple cycle that goes through all components
        if len(component) > 1:
            for i in range(len(component)):
                j = (i + 1) % len(component)
                minimal_edge_set[component[i]].append(component[j])
        # Adding the edges that go between components
        for neighbor_parent in component_graph[parent]:
            minimal_edge_set[parent].append(neighbor_parent)
    return minimal_edge_set



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
print(graph)
minimal_edge_set = scc_minimal_edge_set(graph)
print(strongly_connected_components(graph))
print(strongly_connected_components(minimal_edge_set))
