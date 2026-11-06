import json

from genlib import *

N = 10**5


def brute(a):
    return str(max(len(seg) for seg in "".join(map(str, a)).split("0")))


def ref(text):
    return brute(json.loads(text.strip()))


def samples():
    res = []
    for a, want in (([1, 1, 0, 1, 1, 1], "3"), ([1, 0, 1, 1, 0, 1], "2")):
        assert brute(a) == want
        res.append((lines(arr(a)), want))
    return res


def cases():
    res = [
        lines(arr([0])),
        lines(arr([1])),
        lines(arr([0, 0, 0])),
        lines(arr([1, 1, 1, 0])),
        lines(arr([0, 1, 1])),
        lines(arr([1] * N)),
        lines(arr([0] * N)),
        lines(arr([1, 0] * (N // 2))),
        lines(arr([0] * (N - 1) + [1])),
    ]
    for n in (10, 100, 1000):
        res.append(lines(arr(rand_arr(n, 0, 1))))
    res.append(lines(arr(rand_arr(N, 0, 1))))
    a = [1 if random.random() < 0.95 else 0 for _ in range(N)]
    res.append(lines(arr(a)))
    return res
