import json

from genlib import *

N = 10**4
T = 10**7


def brute(ts, d):
    """合并区间 [t, t + d) 求并集长度"""
    total, end = 0, -1
    for t in ts:
        lo = max(t, end)
        if t + d > lo:
            total += t + d - lo
        end = max(end, t + d)
    return str(total)


def brute_small(ts, d):
    sec = set()
    for t in ts:
        sec.update(range(t, t + d))
    return str(len(sec))


def ref(text):
    ts, d = [json.loads(x) for x in text.split("\n") if x.strip()]
    return brute(ts, d)


def samples():
    res = []
    for ts, d, want in (([1, 4], 2, "4"), ([1, 2], 2, "3")):
        assert brute(ts, d) == want
        res.append((lines(arr(ts), d), want))
    return res


def cases():
    for _ in range(300):
        ts = rand_sorted(random.randint(1, 10), 0, 20)
        d = random.randint(0, 8)
        assert brute(ts, d) == brute_small(ts, d)
    res = [
        lines(arr([0]), 0),
        lines(arr([5]), T),
        lines(arr([1, 2, 3]), 0),
        lines(arr([3, 3, 3]), 4),
        lines(arr([0, T]), T),
        lines(arr([T] * N), T),
        lines(arr(list(range(N))), 1),
    ]
    for n in (10, 100, 1000):
        res.append(lines(arr(rand_sorted(n, 0, 5 * n)), random.randint(0, 10)))
    res.append(lines(arr(rand_sorted(N, 0, T)), T))
    res.append(lines(arr(rand_sorted(N, 0, T)), 1000))
    res.append(lines(arr(rand_sorted(N, 0, T)), random.randint(0, T)))
    return res
