
def permutations_rec(arr):
    yield from permute_helper(arr, 0)

def permute_helper(arr, start):
    n = len(arr)
    if start == n:
        yield list(arr)

    for i in range(start, n):
        arr[i], arr[start] = arr[start], arr[i]
        yield from permute_helper(arr, start + 1)
        arr[i], arr[start] = arr[start], arr[i]

arr = list(range(3))
print(list(permutations_rec(arr)))

for a in permutations_rec(arr):
    print(a)

print([1,2,3][:1])
print(tuple([1,2,3]))
