from genlib import *


def brute(p):
    best = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            best = max(best, p[j] - p[i])
    return best


def fast(p):
    lo, best = 10**9, 0
    for x in p:
        lo = min(lo, x)
        best = max(best, x - lo)
    return best


def samples():
    return [
        (lines(arr([7, 1, 5, 3, 6, 4])), "5"),
        (lines(arr([7, 6, 4, 3, 1])), "0"),
    ]


def cases():
    for _ in range(200):
        p = rand_arr(random.randint(1, 12), 0, 20)
        assert brute(p) == fast(p)
    n = 10**5
    return [
        lines(arr([5])),
        lines(arr([0, 10000])),
        lines(arr([3, 3, 3, 3])),
        lines(arr([2, 4, 1])),
        lines(arr(rand_arr(10, 0, 20))),
        lines(arr(rand_arr(100, 0, 1000))),
        lines(arr(rand_arr(1000, 0, 10**4))),
        lines(arr(list(range(10**4, -1, -1)) + [0] * (n - 10**4 - 1))),
        lines(arr([i % 10**4 for i in range(n)])),
        lines(arr(rand_arr(n, 0, 10**4))),
        lines(arr([10**4] * (n - 1) + [0])),
    ]
