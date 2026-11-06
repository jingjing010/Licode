import json

from genlib import *


def ref(inp):
    a = json.loads(inp.split("\n")[0])
    return str(int("".join(map(str, a)), 2))


def samples():
    res = [
        (lines(arr([1, 0, 1])), "5"),
        (lines(arr([0])), "0"),
    ]
    for inp, want in res:
        assert ref(inp) == want
    return res


def cases():
    res = [
        lines(arr([1])),
        lines(arr([0, 0])),
        lines(arr([1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0])),
        lines(arr([0, 0, 0, 1])),
        lines(arr([1] * 30)),
        lines(arr([1] + [0] * 29)),
        lines(arr([0] * 30)),
        lines(arr([0] * 15 + [1] * 15)),
    ]
    for n in (5, 10, 20, 29, 30, 30):
        res.append(lines(arr(rand_arr(n, 0, 1))))
    return res
