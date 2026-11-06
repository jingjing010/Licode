from genlib import *


def samples():
    return [
        (lines(arr([7, 2, 5, 10, 8]), 2), "18"),
        (lines(arr([1, 2, 3, 4, 5]), 2), "9"),
        (lines(arr([1, 4, 4]), 3), "4"),
    ]


def brute(nums, k):
    """O(k n^2) 区间 DP：dp[j][i] = 前 i 个数分成 j 段的最优值"""
    n = len(nums)
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    INF = float("inf")
    dp = [[INF] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 0
    for j in range(1, k + 1):
        for i in range(j, n + 1):
            best = INF
            for p in range(j - 1, i):
                best = min(best, max(dp[j - 1][p], pre[i] - pre[p]))
            dp[j][i] = best
    return dp[k][n]


def binary(nums, k):
    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        pieces, cur = 1, 0
        for x in nums:
            if cur + x > mid:
                pieces += 1
                cur = 0
            cur += x
        if pieces <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def cases():
    res = [
        ([0], 1),
        ([10**6], 1),
        ([0, 0, 0, 0], 2),
        ([1, 2, 3, 4, 5], 5),
        ([5, 1, 1, 1, 1], 2),
        ([1, 1, 1, 1, 100], 3),
    ]
    for n in (8, 15, 30, 60):
        res.append((rand_arr(n, 0, 20), random.randint(1, min(50, n))))
    for nums, k in list(res):
        assert brute(nums, k) == binary(nums, k)
    for _ in range(40):
        n = random.randint(1, 12)
        nums = rand_arr(n, 0, random.choice([3, 100]))
        k = random.randint(1, n)
        assert brute(nums, k) == binary(nums, k)
    res.append(([10**6] * 1000, 1))
    res.append(([10**6] * 1000, 50))
    res.append((rand_arr(1000, 0, 10**6), 50))
    res.append((rand_arr(1000, 0, 10**6), 7))
    res.append((rand_arr(1000, 0, 10), 50))
    return [lines(arr(a), k) for a, k in res]
