import json

from genlib import *


def brute(inp):
    a = json.loads(inp.split("\n")[0])
    for i in range(0, len(a) - 1, 2):
        a[i], a[i + 1] = a[i + 1], a[i]
    return arr(a)


def samples():
    res = [
        (lines(arr([1, 2, 3, 4])), "[2,1,4,3]"),
        (lines(arr([])), "[]"),
        (lines(arr([1]))  , "[1]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines(arr([1, 2])),
        lines(arr([1, 2, 3])),
        lines(arr([5, 5, 5, 5, 5])),
        lines(arr([0, 100])),
        lines(arr(list(range(100)))),
        lines(arr(list(range(99)))),
    ]
    for n in (6, 7, 20, 33, 64):
        res.append(lines(arr(rand_arr(n, 0, 100))))
    res.append(lines(arr(rand_arr(100, 0, 100))))
    return res
