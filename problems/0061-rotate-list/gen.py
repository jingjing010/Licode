import json

from genlib import *


def ref(inp):
    ls = inp.split("\n")
    a, k = json.loads(ls[0]), int(ls[1])
    if not a:
        return "[]"
    k %= len(a)
    cut = len(a) - k
    return arr(a[cut:] + a[:cut])


def samples():
    res = [
        (lines(arr([1, 2, 3, 4, 5]), 2), "[4,5,1,2,3]"),
        (lines(arr([0, 1, 2]), 4), "[2,0,1]"),
    ]
    for inp, want in res:
        assert ref(inp) == want
    return res


def cases():
    res = [
        lines(arr([]), 0),
        lines(arr([]), 7),
        lines(arr([5]), 2 * 10**9),
        lines(arr([1, 2]), 1),
        lines(arr([1, 2]), 2),
        lines(arr([1, 2, 3, 4, 5]), 0),
        lines(arr([1, 2, 3, 4, 5]), 5),
        lines(arr([1, 2, 3, 4, 5]), 4),
        lines(arr([-100, 100, -100]), 31),
    ]
    for n in (10, 50, 200):
        res.append(lines(arr(rand_arr(n, -100, 100)), random.randint(0, 1000)))
    res.append(lines(arr(rand_arr(500, -100, 100)), 2 * 10**9))
    res.append(lines(arr(rand_arr(500, -100, 100)), 499))
    res.append(lines(arr(rand_arr(500, -100, 100)), random.randint(0, 2 * 10**9)))
    return res
