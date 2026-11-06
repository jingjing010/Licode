import json

from genlib import *


def ref(inp):
    ls = inp.split("\n")
    a, x = json.loads(ls[0]), int(ls[1])
    return arr([v for v in a if v < x] + [v for v in a if v >= x])


def samples():
    res = [
        (lines(arr([1, 4, 3, 2, 5, 2]), 3), "[1,2,2,4,3,5]"),
        (lines(arr([2, 1]), 2), "[1,2]"),
    ]
    for inp, want in res:
        assert ref(inp) == want
    return res


def cases():
    res = [
        lines(arr([]), 0),
        lines(arr([1]), 1),
        lines(arr([1]), 2),
        lines(arr([3, 1, 2]), 200),
        lines(arr([3, 1, 2]), -200),
        lines(arr([5, 4, 3, 2, 1]), 3),
        lines(arr([1, 1, 1, 1]), 1),
        lines(arr([-100, 100, -100, 100]), 0),
    ]
    for n in (8, 30, 100):
        res.append(lines(arr(rand_arr(n, -100, 100)), random.randint(-50, 50)))
    for _ in range(3):
        res.append(lines(arr(rand_arr(200, -100, 100)), random.randint(-100, 100)))
    return res
