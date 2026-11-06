import json

from genlib import *


def brute(inp):
    ls = inp.split("\n")
    a = json.loads(ls[0])
    n = int(ls[1])
    del a[len(a) - n]
    return arr(a)


def samples():
    res = [
        (lines(arr([1, 2, 3, 4, 5]), 2), "[1,2,3,5]"),
        (lines(arr([1]), 1), "[]"),
        (lines(arr([1, 2]), 1), "[1]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines(arr([1, 2]), 2),
        lines(arr([0, 100, 50]), 2),
        lines(arr([7, 7, 7]), 3),
        lines(arr(list(range(1, 31))), 30),
        lines(arr(list(range(1, 31))), 1),
        lines(arr(list(range(1, 31))), 15),
    ]
    for _ in range(8):
        sz = random.randint(1, 30)
        res.append(lines(arr(rand_arr(sz, 0, 100)), random.randint(1, sz)))
    return res
