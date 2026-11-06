import json

from genlib import *


def brute(inp):
    ls = inp.split("\n")
    a = json.loads(ls[0])
    k = int(ls[1])
    res = []
    i = 0
    while i + k <= len(a):
        res += a[i:i + k][::-1]
        i += k
    res += a[i:]
    return arr(res)


def samples():
    res = [
        (lines(arr([1, 2, 3, 4, 5]), 2), "[2,1,4,3,5]"),
        (lines(arr([1, 2, 3, 4, 5]), 3), "[3,2,1,4,5]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    N = 5000
    res = [
        lines(arr([1]), 1),
        lines(arr([1, 2]), 2),
        lines(arr([1, 2, 3, 4, 5]), 1),
        lines(arr([1, 2, 3, 4, 5]), 5),
        lines(arr([1, 2, 3, 4, 5, 6]), 3),
        lines(arr([1, 2, 3, 4, 5, 6, 7]), 4),
    ]
    for n in (10, 37, 100):
        res.append(lines(arr(rand_arr(n, 0, 1000)), random.randint(1, n)))
    res.append(lines(arr(rand_arr(N, 0, 1000)), 1))
    res.append(lines(arr(rand_arr(N, 0, 1000)), 2))
    res.append(lines(arr(rand_arr(N, 0, 1000)), 7))
    res.append(lines(arr(rand_arr(N, 0, 1000)), N))
    res.append(lines(arr(rand_arr(N, 0, 1000)), N - 1))
    return res
