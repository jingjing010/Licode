from math import comb

from genlib import *


def brute(r):
    row = [1]
    for _ in range(r):
        row = [1] + [row[j] + row[j + 1] for j in range(len(row) - 1)] + [1]
    return row


def samples():
    res = []
    for r, want in ((3, "[1,3,3,1]"), (0, "[1]"), (1, "[1,1]")):
        assert arr(brute(r)) == want
        res.append((lines(r), want))
    return res


def cases():
    for r in range(34):
        assert brute(r) == [comb(r, k) for k in range(r + 1)]
        assert max(brute(r)) < 2**31
    return [lines(r) for r in (2, 4, 5, 6, 10, 13, 20, 25, 29, 30, 31, 32, 33)]
