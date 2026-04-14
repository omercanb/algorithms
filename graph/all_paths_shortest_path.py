import copy
from pprint import pp


# Extend takes an existing distance matrix D1 and composes it with D2 so that we get a new distance matrix that can minimize using both the distance matrices
# For slow all paths shortest paths D2 is just the weight matrix
# For fast all paths shortest paths D2 is the same as D1
def extend(D1, D2):
    V = len(D1)
    D_new = [[float("inf") for _ in range(V)] for _ in range(V)]
    for i in range(V):
        for j in range(V):
            new_distance = D1[i][j]
            for k in range(V):
                new_distance = min(new_distance, D1[i][k] + D2[k][j])
            D_new[i][j] = new_distance
    return D_new


def slow_all_paths_shortest_path(G: list[list[int]]):
    """
    Uses the following dp formulation
    A shortest path from i to j with a maximum of p intermediate vertices is either the same path (with a max of p - 1) or a path from i to an incoming vertex k and an edge from k to j
    """
    V = len(G)
    # We expect distance to be infinte for where there are no edges and have edge weight for existing edges
    distance = copy.deepcopy(G)
    for i in range(V - 1):
        distance = extend(distance, G)
    return distance


def faster_all_paths_shortest_paths(G: list[list[int]]):
    """
    This algorithm is the same as above but it uses repeated squaring, using the fact that the extend operation is associative.
    """
    V = len(G)
    distance = copy.deepcopy(G)
    p = 1
    # Here we use the fact that we don't have to match V - 1 exactly, as us finding the path for a larger number of max intermediate vertices
    # Will be the same value of shortest path (assuming no negative edge weight cycles)
    while p < V - 1:
        distance = extend(distance, distance)
        p *= 2
    return distance


def predecessors_from_distance_matrix(D, W):
    """
    This algorithm works by going starting vertex by starting vertex and incrementally finding edge weights that match the distances
    From closest to the starting vertex to farthes
    We know that if the distance to a vertex j is equal to the distance to a preceeding vertex k plus the weight of the edge from j to k
    Then k is the predecessor of j GIVEN THAT k is on the shortest length path to j (Otherwise j can be repeated in the path)
    Note: The above fact is why we can't 'follow' the ending vertex back to the starting vertex, because there can be multiple edge weights that match
    and from those we might unwantedly choose an edge that leads back to the current vertex
    This means we can't do a linear scan over j, but we instead have to do a breadth first search (because it's a tree a depth first search also works which is what we do)
    """
    V = len(D)
    pred = [[None for _ in range(V)] for _ in range(V)]
    for i in range(V):
        stack = [i]
        while stack:
            k = stack.pop()
            for j in range(V):
                # If the distances match, add the distance, use P as the visited vertex
                if j == k or j == i:
                    continue
                if pred[i][j] != None:
                    continue
                if D[i][j] == D[i][k] + W[k][j]:
                    pred[i][j] = k
                    stack.append(j)
    return pred


def floyd_warshall(G: list[list[int]]):
    """
    This algorithm uses a different, better subproblem structure.
    The structure is this, take a path from i to j that only has intermediate vertices from the set {1, ..., k}
    Here's how we decompose this solution into solutions to subproblems.
        If k is not an intermediate vertex (so it's not used despite being available in the set)
            Then the shortest path using vertices from the set {1, ..., k - 1} (So a smaller problem/subproblem) will be exactly the same
        If k is an intermediate vertex
            Then we know two shortest paths that don't use the vertex k. These are the path from i to k and the path from k to j.
            Because paths are assumed to be simple (we can check for negative cycles if we want) we know k is not in any of the paths.
            We know that both the paths that are part of the solution are solutions to subproblems, else we could cut and paste them to get a shorter path.
    So here's the recursive definition
    D[i, j, k] = min(D[i, j, k-1], D[i, k, k-1] + D[k, j, k-1])
    """
    # We start the distances from the edge weight
    # These are the paths with 0 intermediate vertices
    V = len(G)
    distance = copy.deepcopy(G)
    pred = [[None for _ in range(V)] for _ in range(V)]
    for i in range(V):
        for j in range(V):
            if i == j:
                continue
            if distance[i][j] != float("inf"):
                pred[i][j] = i

    for k in range(V):
        for i in range(V):
            for j in range(V):
                if distance[i][j] > distance[i][k] + distance[k][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]
                    pred[i][j] = pred[k][j]
                else:
                    distance[i][j] = distance[i][j]
                    pred[i][j] = pred[i][j]
    return distance, pred


inf = float("inf")
# the matrix from chapter 25 in clrs
g = [
    [0, 3, 8, inf, -4],
    [inf, 0, inf, 1, 7],
    [inf, 4, 0, inf, inf],
    [2, inf, -5, 0, inf],
    [inf, inf, inf, 6, 0],
]

true_shortest_distance = [
    [0, 1, -3, 2, -4],
    [3, 0, -4, 1, -1],
    [7, 4, 0, 5, 3],
    [2, -1, -5, 0, -2],
    [8, 5, 1, 6, 0],
]
distance = slow_all_paths_shortest_path(G)
assert distance == true_shortest_distance
print("Slow all paths")
print("Assertion passed")
pp(distance)
distance = faster_all_paths_shortest_paths(G)
assert distance == true_shortest_distance
print("Fast all paths")
print("Assertion passed")
pp(distance)
print("Predecessor Matrix for All Paths")
pred = predecessors_from_distance_matrix(distance, G)
pp(pred)
distance, pred = floyd_warshall(G)
assert distance == true_shortest_distance
print("Floyd-Warshall")
print("Assertion passed")
pp(distance)
print("Predecessor Matrix for Floyd-Warshall")
pp(pred)
