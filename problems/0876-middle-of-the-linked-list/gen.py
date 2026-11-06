import json

from genlib import *


def ref(inp):
    a = json.loads(inp.split("\n")[0])
    return arr(a[len(a) // 2:])


def samples():
    res = [
        (lines(arr([1, 2, 3, 4, 5])), "[3,4,5]"),
        (lines(arr([1, 2, 3, 4, 5, 6])), "[4,5,6]"),
    ]
    for inp, want in res:
        assert ref(inp) == want
    return res


def cases():
    res = [
        lines(arr([1])),
        lines(arr([1, 2])),
        lines(arr([1, 2, 3])),
        lines(arr([7, 7, 7, 7])),
        lines(arr(list(range(1, 101)))),
        lines(arr(list(range(1, 100)))),
    ]
    for n in (5, 10, 31, 50, 77, 99, 100):
        res.append(lines(arr(rand_arr(n, 1, 100))))
    return res
