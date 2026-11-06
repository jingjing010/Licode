from genlib import *

INF = float("inf")


def brute(a):
    n = len(a)
    dp = [INF] * n
    dp[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + a[i] + 1)):
            dp[j] = min(dp[j], dp[i] + 1)
    return dp[-1]


def fast(a):
    steps = end = far = 0
    for i in range(len(a) - 1):
        far = max(far, i + a[i])
        if i == end:
            steps += 1
            end = far
    return steps


def reachable(a):
    far = 0
    for i, x in enumerate(a):
        if i > far:
            return False
        far = max(far, i + x)
    return True


def rand_reachable(n, lo, hi):
    while True:
        a = rand_arr(n, lo, hi)
        if reachable(a):
            return a


def samples():
    return [
        (lines(arr([2, 3, 1, 1, 4])), "2"),
        (lines(arr([2, 3, 0, 1, 4])), "2"),
    ]


def cases():
    for _ in range(300):
        a = rand_reachable(random.randint(1, 10), 0, 4)
        assert brute(a) == fast(a)
    n = 10**4
    return [
        lines(arr([0])),
        lines(arr([1000])),
        lines(arr([1, 2])),
        lines(arr([1, 1, 1, 1])),
        lines(arr([5, 0, 0, 0, 0, 0])),
        lines(arr([1, 2, 1, 1, 1])),
        lines(arr(rand_reachable(10, 0, 4))),
        lines(arr(rand_reachable(100, 0, 6))),
        lines(arr(rand_reachable(1000, 1, 10))),
        lines(arr([1] * n)),
        lines(arr([1000] * n)),
        lines(arr([2, 0] * (n // 2 - 1) + [1, 0])),
        lines(arr(rand_reachable(n, 1, 20))),
        lines(arr(rand_reachable(n, 0, 1000))),
    ]
