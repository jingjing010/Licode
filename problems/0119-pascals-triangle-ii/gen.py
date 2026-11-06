from math import comb

from genlib import *


def brute(r):
    return arr([comb(r, k) for k in range(r + 1)])


def ref(text):
    return brute(int(text.strip()))


def samples():
    res = []
    for r, want in ((3, "[1,3,3,1]"), (0, "[1]"), (1, "[1,1]")):
        assert brute(r) == want
        res.append((lines(r), want))
    return res


def cases():
    return [lines(r) for r in (2, 4, 5, 7, 10, 16, 20, 25, 29, 30, 31, 32, 33)]
