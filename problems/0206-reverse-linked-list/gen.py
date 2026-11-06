import json

from genlib import *


def brute(inp):
    a = json.loads(inp.split("\n")[0])
    return arr(a[::-1])


def samples():
    res = [
        (lines(arr([1, 2, 3, 4, 5])), "[5,4,3,2,1]"),
        (lines(arr([1, 2])), "[2,1]"),
        (lines(arr([])), "[]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines(arr([7])),
        lines(arr([-5000, 5000])),
        lines(arr([3, 3, 3, 3])),
        lines(arr([1, 2, 3])),
        lines(arr(list(range(1, 5001)))),
    ]
    for n in (5, 10, 50, 300):
        res.append(lines(arr(rand_arr(n, -5000, 5000))))
    for _ in range(3):
        res.append(lines(arr(rand_arr(5000, -5000, 5000))))
    return res
