from genlib import *

V = 10**4


def samples():
    return [
        (lines(arr([1, 2, 3, 4, 5]), 4, 3), "[1,2,3,4]"),
        (lines(arr([1, 1, 2, 3, 4, 5]), 4, -1), "[1,1,2,3]"),
    ]


def brute(a, k, x):
    return sorted(sorted(a, key=lambda v: (abs(v - x), v))[:k])


def binary(a, k, x):
    lo, hi = 0, len(a) - k
    while lo < hi:
        mid = (lo + hi) // 2
        if x - a[mid] > a[mid + k] - x:
            lo = mid + 1
        else:
            hi = mid
    return a[lo:lo + k]


def cases():
    res = [
        ([5], 1, 5),
        ([5], 1, -V),
        ([1, 2, 3, 4, 5], 5, 100),
        ([1, 2, 3, 4, 5], 1, 100),
        ([1, 3], 1, 2),
        ([1, 1, 1, 10, 10, 10], 1, 9),
        ([0, 0, 1, 2, 3, 3, 4, 7, 7, 8], 3, 5),
        ([-V, V], 1, 0),
    ]
    for n in (10, 100, 1000):
        a = rand_sorted(n, -100, 100)
        res.append((a, random.randint(1, n), random.randint(-120, 120)))
    for a, k, x in res:
        assert brute(a, k, x) == binary(a, k, x)
    for _ in range(300):
        n = random.randint(1, 15)
        a = rand_sorted(n, -10, 10)
        k, x = random.randint(1, n), random.randint(-12, 12)
        assert brute(a, k, x) == binary(a, k, x)
    N = 10**4
    res.append((rand_sorted(N, -V, V), N // 2, random.randint(-V, V)))
    res.append((rand_sorted(N, -V, V), 1, V))
    res.append((rand_sorted(N, -V, V), N, -V))
    res.append(([7] * N, 777, 7))
    for a, k, x in res[-4:]:
        assert brute(a, k, x) == binary(a, k, x)
    return [lines(arr(a), k, x) for a, k, x in res]
