from genlib import *
from bisect import bisect_left


def brute(a):
    dp = [1] * len(a)
    for i in range(len(a)):
        for j in range(i):
            if a[j] < a[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def fast(a):
    tails = []
    for x in a:
        k = bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x
    return len(tails)


def samples():
    return [
        (lines(arr([10, 9, 2, 5, 3, 7, 101, 18])), "4"),
        (lines(arr([0, 1, 0, 3, 2, 3])), "4"),
        (lines(arr([7, 7, 7, 7, 7, 7, 7])), "1"),
    ]


def cases():
    for _ in range(300):
        a = rand_arr(random.randint(1, 15), -5, 5)
        assert brute(a) == fast(a)
    n = 2500
    return [
        lines(arr([5])),
        lines(arr([-10000, 10000])),
        lines(arr([3, 2, 1])),
        lines(arr([1, 3, 6, 7, 9, 4, 10, 5, 6])),
        lines(arr([4, 10, 4, 3, 8, 9])),
        lines(arr(rand_arr(20, -10, 10))),
        lines(arr(rand_arr(200, -100, 100))),
        lines(arr(list(range(-1250, 1250)))),
        lines(arr(list(range(10000, 10000 - n, -1)))),
        lines(arr([1, 1, 2, 2, 3, 3] * (n // 6))),
        lines(arr(rand_arr(n, -10**4, 10**4))),
        lines(arr(sorted(rand_arr(n, -10**4, 10**4)))),
        lines(arr([i // 2 if i % 2 == 0 else -i for i in range(n)])),
    ]
