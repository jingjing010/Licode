import json
from collections import Counter

from genlib import *


def ref(inp):
    a = json.loads(inp.split("\n")[0])
    c = Counter(a)
    return arr([x for x in a if c[x] == 1])


def samples():
    res = [
        (lines(arr([1, 2, 3, 3, 4, 4, 5])), "[1,2,5]"),
        (lines(arr([1, 1, 1, 2, 3])), "[2,3]"),
    ]
    for inp, want in res:
        assert ref(inp) == want
    return res


def cases():
    res = [
        lines(arr([])),
        lines(arr([1])),
        lines(arr([1, 1])),
        lines(arr([1, 2])),
        lines(arr([1, 2, 2])),
        lines(arr([1, 1, 2, 3, 3])),
        lines(arr([-100] * 150 + [100] * 150)),
        lines(arr(list(range(-100, 101)))),
    ]
    for n in (6, 20, 100):
        res.append(lines(arr(rand_sorted(n, -10, 10))))
    for _ in range(2):
        res.append(lines(arr(rand_sorted(300, -100, 100))))
    res.append(lines(arr(rand_sorted(300, -5, 5))))
    return res
