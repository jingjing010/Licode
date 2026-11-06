import json

from genlib import *

N = 10**4


def brute(a):
    s = set(a)
    return str(next(x for x in range(len(a) + 1) if x not in s))


def ref(text):
    return brute(json.loads(text.strip()))


def make(n, miss=None):
    if miss is None:
        miss = random.randint(0, n)
    a = [x for x in range(n + 1) if x != miss]
    random.shuffle(a)
    return lines(arr(a))


def samples():
    res = []
    for a, want in (([3, 0, 1], "2"), ([0, 1], "2"), ([9, 6, 4, 2, 3, 5, 7, 0, 1], "8")):
        assert brute(a) == want
        res.append((lines(arr(a)), want))
    return res


def cases():
    res = [
        lines(arr([0])),
        lines(arr([1])),
        lines(arr([1, 2])),
        make(5, 0),
        make(10, 10),
        lines(arr(list(range(N, 0, -1)))),
        lines(arr(list(range(N)))),
    ]
    for n in (7, 100, 1000, N, N):
        res.append(make(n))
    res.append(make(N, N // 2))
    return res
