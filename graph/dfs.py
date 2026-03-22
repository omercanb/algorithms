from dataclasses import dataclass

white = 'white'
black = 'black'
gray = 'gray'

# Edge Types
tree = 'tree'
back = 'back'
forward = 'forward'
cross = 'cross'


def dfs_iter(graph):
    color = {v: white for v in graph}
    predecessors = {}
    discovery = {}
    finish = {}
    stack = []
    t = 1
    for u in graph:
        if color[u] != white:
            continue
        # Stack keeps the vertex and it's unchecked neighbors
        stack.append([u, 0])
        discovery[u] = t
        while stack:
            t += 1
            u, cur_neighbor = stack[-1]
            neighbors = graph[u]
            print(u, neighbors, cur_neighbor)
            # If neighbors is nonempty we 'recurse' on it
            # If it's empty it means this vertex should be blackened
            if cur_neighbor == len(neighbors):
                stack.pop()
                color[u] = black
                t += 1
                finish[u] = t
                continue

            i = cur_neighbor
            while (i < len(neighbors)):
                v = neighbors[i]
                # Increment cur neighbor
                i += 1
                stack[-1][1] = i
                if color[v] != white:
                    continue
                stack.append([v, 0])
                color[v] = gray
                t += 1
                discovery[v] = t
                predecessors[v] = u
                break

    print(f'{color=}')
    print(f'{predecessors=}')
    print(f'{discovery=}')
    print(f'{finish=}')
    print(f'{stack=}')

def get_edge_type(u, v, color, discovery, predecessors, edge_types, directed):
    edge = None
    # Assign type of edge
    if directed:
        # We need edge types to be symmetric for directed graphs
        if (v, u) in edge_types:
            edge = edge_types[(v, u)]
        elif color[v] == gray and predecessors[u] != v:
            edge = back
        else:
            edge = tree
    else:
        if color[v] == gray:
            edge = back
        elif color[v] == black:
            if discovery[u] < discovery[v]:
                edge = forward
            else:
                edge = cross
        else:
            edge = tree
    return edge


def dfs_full(graph, directed):
    color = {v: white for v in graph}
    predecessors = {v: None for v in graph}
    discovery = {}
    finish = {}
    edge_type = {}
    t = 1
    def dfs_visit(u):
        nonlocal t
        t += 1
        discovery[u] = t
        color[u] = gray
        for v in graph[u]:
            edge_type[(u, v)] = get_edge_type(u, v, color, discovery, predecessors, edge_type, directed)
            if color[v] != white:
                continue
            predecessors[v] = u
            dfs_visit(v)
        t += 1
        finish[u] = t
        color[u] = black
    for u in graph:
        if color[u] == white:
            dfs_visit(u)
    print(f'{color=}')
    print(f'{predecessors=}')
    print(f'{discovery=}')
    print(f'{finish=}')
    print(f'{edge_type=}')

        
def dfs_pred(graph):
    visited = set()
    predecessors = {}
    for v in graph:
        if v in visited:
            continue
        stack = [v]
        visited.add(v)
        while stack:
            cur = stack.pop()
            for u in graph[cur]:
                if u in visited:
                    continue
                predecessors[u] = cur
                stack.append(u)
    return predecessors

def dfs_cycle(graph):

    def dfs_cycle_visit(cur):
        on_stack.add(cur)
        visited.add(cur)
        for v in graph[cur]:
            # Nodes that are on the stack at the time represent a cycle
            # We begin exploring a node and put it on the stack
            # When we stop exploring the node it means we have discovered all of the paths that out from the node
            # So if we see a node on the stack that means that one of the outgoing paths of the node returns back to it
            if v in on_stack:
                cycle = [cur]
                cycle_cur = cur
                while cycle_cur != v:
                    cycle_cur = predecessors[cycle_cur]
                    cycle.append(cycle_cur)
                cycles.append(cycle[::-1])
            if v not in visited:
                predecessors[v] = cur
                dfs_cycle_visit(v)
        on_stack.remove(cur)

    visited = set()
    on_stack = set()
    predecessors = {}
    cycles = []
    for v in graph:
        if v not in visited:
            dfs_cycle_visit(v)
    return predecessors, cycles

edges = {0: [1, 2], 1: [3, 4], 2: [5, 6], 3: [], 4: [], 5: [], 6: []}
edges_w_cycle = {0: [1], 1: [0, 2], 2: [3], 3: [2, 0]}
edges = {0: [1, 2], 1: [0, 2], 2: [], 3: [0]}
edges_directed = {0: [1, 2], 1: [0, 2], 2: [0, 1]}

# pred = dfs_pred(edges)
# print(pred)
#
# pred = dfs_cycle(edges_w_cycle)
# print(pred)

# dfs_iter(edges)
print('Running full')
# dfs_full(edges, False)
dfs_full(edges_directed, True)
