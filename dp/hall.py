"""
16.1-4
Suppose that we have a set of activities to schedule among a large number of lecture
halls, where any activity can take place in any lecture hall. We wish to schedule
all the activities using as few lecture halls as possible. Give an efficient greedy
algorithm to determine which activity should use which lecture hall.
(This problem is also known as the interval-graph coloring problem. We can
create an interval graph whose vertices are the given activities and whose edges
connect incompatible activities. The smallest number of colors required to color
every vertex so that no two adjacent vertices have the same color corresponds to
finding the fewest lecture halls needed to schedule all of the given activities.)
"""


def print_diag(n):
    for L in range(1, n+1):         # interval length
        for i in range(1, n-L+1):   # start
            j = i + L               # end
            for k in range(i+1, j+1):
                print((i, k), (k, j))


def print_row(n):
    for i in range(1, n+1):
        for j in range(i, 0, -1):
            print((i, j))


print_diag(4)
print()
print_row(4)
