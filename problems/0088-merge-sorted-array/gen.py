from genlib import *

V = 10**9


def brute(a, m, b, n):
    return arr(sorted(a[:m] + b[:n]))


def make(a, b):
    m, n = len(a), len(b)
    return lines(arr(sorted(a) + [0] * n), m, arr(sorted(b)), n)


def samples():
    res = []
    for a, m, b, n, want in (([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, "[1,2,2,3,5,6]"),
                             ([1], 1, [], 0, "[1]"),
                             ([0], 0, [1], 1, "[1]")):
        assert brute(a, m, b, n) == want
        res.append((lines(arr(a), m, arr(b), n), want))
    return res


def cases():
    res = [
        make([], [5]),
        make([-3], [-3]),
        make([1, 2, 3], [4, 5, 6]),
        make([4, 5, 6], [1, 2, 3]),
        make([0, 0, 0], [0, 0]),
        make([-V, V], [-V, 0, V]),
        make([2, 2, 2, 2], [1, 3]),
        make(rand_arr(200, -V, V), []),
        make([], rand_arr(200, -V, V)),
        make([1] * 100, [1] * 100),
    ]
    for m, n, lo, hi in ((3, 5, -5, 5), (10, 10, -10, 10), (50, 30, -100, 100),
                         (100, 100, -V, V), (150, 50, -V, V), (1, 199, -V, V), (199, 1, -V, V)):
        res.append(make(rand_arr(m, lo, hi), rand_arr(n, lo, hi)))
    return res
