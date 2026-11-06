import json

from genlib import *


def ref(inp):
    ls = inp.split("\n")
    a, k = json.loads(ls[0]), int(ls[1])
    base, extra = divmod(len(a), k)
    out, pos = [], 0
    for i in range(k):
        size = base + (1 if i < extra else 0)
        out.append(a[pos:pos + size])
        pos += size
    return mat(out)


def samples():
    res = [
        (lines(arr([1, 2, 3]), 5), "[[1],[2],[3],[],[]]"),
        (lines(arr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 3), "[[1,2,3,4],[5,6,7],[8,9,10]]"),
    ]
    for inp, want in res:
        assert ref(inp) == want
    return res


def cases():
    res = [
        lines(arr([]), 1),
        lines(arr([]), 50),
        lines(arr([7]), 1),
        lines(arr([7]), 3),
        lines(arr([1, 2, 3, 4]), 4),
        lines(arr([1, 2, 3, 4]), 1),
        lines(arr([0, 1000, 0, 1000, 5]), 2),
    ]
    for n, k in ((11, 3), (49, 50), (100, 7), (200, 50)):
        res.append(lines(arr(rand_arr(n, 0, 1000)), k))
    res.append(lines(arr(rand_arr(1000, 0, 1000)), 50))
    res.append(lines(arr(rand_arr(1000, 0, 1000)), 1))
    res.append(lines(arr(rand_arr(1000, 0, 1000)), 33))
    return res
