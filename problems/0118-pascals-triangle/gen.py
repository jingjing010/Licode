from genlib import *
from math import comb


def fast(n):
    return [[comb(i, j) for j in range(i + 1)] for i in range(n)]


def samples():
    return [
        (lines(5), "[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]"),
        (lines(1), "[[1]]"),
    ]


def cases():
    assert mat(fast(5)) == "[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]"
    assert max(max(r) for r in fast(30)) < 2**31
    return [lines(n) for n in (2, 3, 4, 6, 10, 15, 20, 25, 29, 30)]
