from dataclasses import dataclass


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
pred = dfs_pred(edges)
print(pred)

pred = dfs_cycle(edges_w_cycle)
print(pred)


