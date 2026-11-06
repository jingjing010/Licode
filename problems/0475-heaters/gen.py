from genlib import *
from bisect import bisect_left

MAXV = 10**9


def samples():
    return [
        (lines(arr([1, 2, 3]), arr([2])), "1"),
        (lines(arr([1, 2, 3, 4]), arr([1, 4])), "1"),
        (lines(arr([1, 5]), arr([2])), "3"),
    ]


def brute(houses, heaters):
    return max(min(abs(h - t) for t in heaters) for h in houses)


def fast(houses, heaters):
    hs = sorted(heaters)
    ans = 0
    for h in houses:
        i = bisect_left(hs, h)
        best = min([hs[j] - h if hs[j] >= h else h - hs[j] for j in (i - 1, i) if 0 <= j < len(hs)])
        ans = max(ans, best)
    return ans


def cases():
    res = [
        ([1], [1]),
        ([1], [MAXV]),
        ([MAXV], [1]),
        ([1, MAXV], [MAXV // 2]),
        ([5, 5, 5], [5, 5]),
        ([1, 2, 3, 4, 5], [10, 1, 7]),
    ]
    for n, m in ((10, 3), (50, 50), (200, 5)):
        res.append((rand_arr(n, 1, 100), rand_arr(m, 1, 100)))
    for hs, ts in res:
        assert brute(hs, ts) == fast(hs, ts)
    for _ in range(100):
        hs = rand_arr(random.randint(1, 30), 1, random.choice([20, 10**9]))
        ts = rand_arr(random.randint(1, 30), 1, random.choice([20, 10**9]))
        assert brute(hs, ts) == fast(hs, ts)
    N = 3 * 10**4
    res.append((rand_arr(N, 1, MAXV), rand_arr(N, 1, MAXV)))
    res.append((rand_arr(N, 1, MAXV), [1]))
    res.append((rand_arr(N, 1, MAXV), rand_arr(3, 1, MAXV)))
    res.append((list(range(1, N + 1)), list(range(N, 0, -1))))
    res.append((rand_arr(N, 1, MAXV), [MAXV] * N))
    return [lines(arr(a), arr(b)) for a, b in res]
