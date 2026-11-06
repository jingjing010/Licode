from genlib import *


def samples():
    return [
        (lines(arr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 5), "15"),
        (lines(arr([3, 2, 2, 4, 1, 4]), 3), "6"),
        (lines(arr([1, 2, 3, 1, 1]), 4), "3"),
    ]


def days_needed(w, cap):
    d, cur = 1, 0
    for x in w:
        if cur + x > cap:
            d += 1
            cur = 0
        cur += x
    return d


def brute(w, days):
    cap = max(w)
    while days_needed(w, cap) > days:
        cap += 1
    return cap


def dp(w, days):
    """O(days * n^2) 动态规划，与贪心无关的独立校验"""
    n = len(w)
    pre = [0]
    for x in w:
        pre.append(pre[-1] + x)
    INF = float("inf")
    f = [[INF] * (n + 1) for _ in range(days + 1)]
    f[0][0] = 0
    for j in range(1, days + 1):
        for i in range(1, n + 1):
            f[j][i] = min(max(f[j - 1][p], pre[i] - pre[p]) for p in range(i))
    return min(f[j][n] for j in range(1, days + 1))


def binary(w, days):
    lo, hi = max(w), sum(w)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(w, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo


def cases():
    N = 5 * 10**4
    res = [
        ([1], 1),
        ([500], 1),
        ([1, 1, 1, 1], 4),
        ([1, 1, 1, 1], 1),
        ([10, 50, 100, 100, 50, 100, 100, 100], 5),
    ]
    for n in (10, 50, 300):
        res.append((rand_arr(n, 1, 500), random.randint(1, n)))
    for w, d in res:
        if len(w) <= 50:
            assert brute(w, d) == binary(w, d)
    for _ in range(150):
        n = random.randint(1, 10)
        w = rand_arr(n, 1, random.choice([5, 500]))
        d = random.randint(1, n)
        assert dp(w, d) == brute(w, d) == binary(w, d)
    res.append(([500] * N, 1))
    res.append(([500] * N, N))
    res.append((rand_arr(N, 1, 500), 1))
    res.append((rand_arr(N, 1, 500), N))
    res.append((rand_arr(N, 1, 500), random.randint(1, 100)))
    res.append((rand_arr(N, 1, 500), random.randint(1000, N)))
    return [lines(arr(a), d) for a, d in res]
