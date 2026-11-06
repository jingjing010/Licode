import json

from genlib import *

V = 10**4


def brute(inp):
    m = json.loads(inp.split("\n")[0])
    return arr(sorted(x for row in m for x in row))


def lists_of(sizes, lo=-V, hi=V):
    return [rand_sorted(n, lo, hi) for n in sizes]


def samples():
    res = [
        (lines(mat([[1, 4, 5], [1, 3, 4], [2, 6]])), "[1,1,2,3,4,4,5,6]"),
        (lines(mat([])), "[]"),
        (lines(mat([[]])), "[]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines(mat([[], []])),
        lines(mat([[5]])),
        lines(mat([[], [1], []])),
        lines(mat([[1, 2, 3], [4, 5, 6], [7, 8, 9]])),
        lines(mat([[2, 2, 2], [2, 2], [2]])),
        lines(mat(lists_of([random.randint(0, 10) for _ in range(10)], -20, 20))),
        lines(mat(lists_of([random.randint(0, 50) for _ in range(100)]))),
        lines(mat(lists_of([500]))),
        lines(mat(lists_of([500] * 20))),
        lines(mat(lists_of([1] * V))),
        lines(mat([[] for _ in range(V)])),
        lines(mat(lists_of([2] * (V // 2), -5, 5))),
    ]
    sizes = []
    while sum(sizes) < V - 500:
        sizes.append(random.randint(0, 500))
    res.append(lines(mat(lists_of(sizes))))
    sizes = [random.randint(0, 2) for _ in range(V)]
    while sum(sizes) > V:
        sizes[random.randrange(V)] = 0
    res.append(lines(mat(lists_of(sizes))))
    return res
