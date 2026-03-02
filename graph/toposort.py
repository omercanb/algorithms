import random
from collections import defaultdict, deque


def random_dag(n_nodes, edge_prob=0.9):
    # Nodes 0..n-1, edges only go from lower to higher index
    adj = {}
    for i in range(n_nodes):
        adj[i] = []
        for j in range(i+1, n_nodes):
            if random.random() < edge_prob:
                adj[i].append(j)
    return adj

# adj is an adjacency list for a dag
def toposort(adj):
    # maintain a list of visited and result
    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in adj[node]:
            dfs(neighbor)
        result.append(node)
    visited = set()
    result = []
    for node in adj:
        dfs(node)
    result.reverse()
    return result

"""
Pick vertices with 'dependency' 0 (in adj len = 0)
Remove the vertex (add to toposorted list) and update outgoing adjacencies (for each u in adj(v) remove v from in_adj(u))
"""
def toposort2(adj):
    in_deg = get_in_deg(adj) 
    q = deque()
    res = []
    # Start with in degrees of 0
    for v in in_deg:
       if in_deg[v] == 0:
           q.append(v)
    while q:
        # Currently using as a stack but can be anything
        v = q.pop()
        res.append(v)
        for u in adj[v]:
            in_deg[u] -= 1
            if in_deg[u] == 0:
                q.append(u)
    return res


def toposort_check_dag(adj):
    in_deg = get_in_deg(adj) 
    q = deque()
    res = []
    # Start with in degrees of 0
    for v in in_deg:
       if in_deg[v] == 0:
           q.append(v)
    count = 0
    while q:
        # Currently using as a stack but can be anything
        v = q.pop()
        res.append(v)
        count += 1
        for u in adj[v]:
            in_deg[u] -= 1
            if in_deg[u] == 0:
                q.append(u)
    if count != len(adj):
        # If it's a dag, the q should only be empty after all vertices have been processed
        # Otherwise the 'dependencies' can't be brought to zero, ie, not a dag, so a back edge is found
        return None
    return res

def is_dag_rooted_better(adj):
    in_deg = get_in_deg(adj)
    num_zero_indeg = 0
    for deg in in_deg.values():
        if deg == 0:
            num_zero_indeg += 1
    return num_zero_indeg == 1

"""
Assumes adj is a dag
"""
def is_dag_rooted(adj):
    l = toposort(adj)
    fst = l[0]
    stack = [fst]
    visited = set()
    while stack:
        v = stack.pop()
        visited.add(v)
        for u in adj[v]:
            if u not in visited:
                stack.append(u)
                visited.add(u)
    # Visited is the reachable nodes from the first vertex in the toposorted order
    return len(adj) == len(visited)


def get_in_deg(adj):
    in_deg = {}
    for v in adj:
        in_deg[v] = 0
    for v in adj:
        for u in adj[v]:
            in_deg[u] += 1
    return in_deg

def get_in_adj(adj):
    in_adj = defaultdict(list)
    for v in adj:
        for u in adj[v]:
            in_adj[u].append(v)
    return in_adj

a = 'a'
b = 'b'
c = 'c'
d = 'd'
e = 'e'
f = 'f'

graph = {
        a: [b, c],
        b: [d],
        c: [d],
        d: []
        }

graph2 = {
        a: [b],
        b: [c],
        c: [a],
        }
graph3 = {
        a: [b],
        b: [],
        c: [],
        }
rooted1 = {
        a: [b],
        b: [c, d],
        c: [e],
        d: [e],
        e: [],
        }

unrooted1 = {
        a: [b],
        b: [c, d],
        c: [e],
        d: [e],
        e: [],
        f: [],
        }
print(toposort(graph))
print(toposort_check_dag(graph3))
print(is_dag_rooted(rooted1))
print(is_dag_rooted(unrooted1))
for i in range(100):
    adj = random_dag(100)
    if is_dag_rooted(adj) != is_dag_rooted_better(adj):
        print(adj)
