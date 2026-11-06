from genlib import *

V = 9999


def samples():
    return [
        (lines(arr([-1, 0, 3, 5, 9, 12]), 9), "4"),
        (lines(arr([-1, 0, 3, 5, 9, 12]), 2), "-1"),
    ]


def brute(a, t):
    return a.index(t) if t in a else -1


def binary(a, t):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == t:
            return mid
        if a[mid] < t:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def cases():
    res = [
        ([5], 5),
        ([5], -5),
        ([5], 6),
        ([-V, V], -V),
        ([-V, V], V),
        ([-V, V], 0),
    ]
    for n in (10, 100, 1000):
        a = sorted(rand_distinct(n, -V, V))
        res.append((a, random.choice(a)))
        res.append((a, random.randint(-V, V)))
    a = list(range(-V, V + 1))[:10**4]
    res.append((a, a[0]))
    res.append((a, a[-1]))
    res.append((a, a[-1] + 1))
    b = sorted(rand_distinct(10**4, -V, V))
    res.append((b, random.choice(b)))
    t = next(v for v in range(-V, V + 1) if v not in set(b))
    res.append((b, t))
    for a, t in res:
        assert brute(a, t) == binary(a, t)
    return [lines(arr(a), t) for a, t in res]
