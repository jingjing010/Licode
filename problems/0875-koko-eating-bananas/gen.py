from genlib import *

MAXV = 10**9


def samples():
    return [
        (lines(arr([3, 6, 7, 11]), 8), "4"),
        (lines(arr([30, 11, 23, 4, 20]), 5), "30"),
        (lines(arr([30, 11, 23, 4, 20]), 6), "23"),
    ]


def hours(piles, k):
    return sum((p + k - 1) // k for p in piles)


def brute(piles, h):
    k = 1
    while hours(piles, k) > h:
        k += 1
    return k


def binary(piles, h):
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours(piles, mid) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo


def cases():
    N = 10**4
    res = [
        ([1], 1),
        ([MAXV], 1),
        ([MAXV], MAXV),
        ([MAXV], 2),
        ([312884470], 312884469),
        ([5, 5, 5, 5], 4),
        ([1, 1, 1, 999], 10),
    ]
    for n in (5, 30, 200):
        piles = rand_arr(n, 1, 50)
        res.append((piles, random.randint(n, 60 * n)))
    for piles, h in res:
        if max(piles) <= 10**6:
            assert brute(piles, h) == binary(piles, h)
    for _ in range(200):
        n = random.randint(1, 8)
        piles = rand_arr(n, 1, 30)
        h = random.randint(n, 40)
        assert brute(piles, h) == binary(piles, h)
    res.append(([MAXV] * N, N))
    res.append(([MAXV] * N, MAXV))
    res.append((rand_arr(N, 1, MAXV), N))
    res.append((rand_arr(N, 1, MAXV), random.randint(N, MAXV)))
    res.append((rand_arr(N, 1, MAXV), MAXV))
    for piles, h in res:
        assert len(piles) <= h <= MAXV
    return [lines(arr(a), h) for a, h in res]
