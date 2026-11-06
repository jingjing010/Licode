import json

from genlib import *


def ref(inp):
    a = json.loads(inp.split("\n")[0])
    out = []
    for x in a:
        if not out or out[-1] != x:
            out.append(x)
    return arr(out)


def samples():
    res = [
        (lines(arr([1, 1, 2])), "[1,2]"),
        (lines(arr([1, 1, 2, 3, 3])), "[1,2,3]"),
    ]
    for inp, want in res:
        assert ref(inp) == want
    return res


def cases():
    res = [
        lines(arr([])),
        lines(arr([0])),
        lines(arr([5, 5])),
        lines(arr([1, 2, 3, 4])),
        lines(arr([7] * 300)),
        lines(arr([-100, -100, 100, 100])),
        lines(arr(list(range(-100, 100)))),
    ]
    for n in (5, 20, 100):
        res.append(lines(arr(rand_sorted(n, -10, 10))))
    for _ in range(3):
        res.append(lines(arr(rand_sorted(300, -100, 100))))
    res.append(lines(arr(rand_sorted(300, -5, 5))))
    return res
