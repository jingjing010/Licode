from genlib import *

MAXV = 10**6


def samples():
    return [
        (lines(arr([0, 1, 0])), "1"),
        (lines(arr([0, 2, 1, 0])), "1"),
        (lines(arr([0, 10, 5, 2])), "1"),
    ]


def mountain(n, peak, top=MAXV):
    """长度 n、峰顶下标 peak 的随机山脉数组（严格单调）"""
    left = sorted(rand_distinct(peak, 0, top - 1))
    right = sorted(rand_distinct(n - 1 - peak, 0, top - 1), reverse=True)
    return left + [top] + right


def is_mountain(a):
    p = a.index(max(a))
    return (0 < p < len(a) - 1 and all(a[i] < a[i + 1] for i in range(p))
            and all(a[i] > a[i + 1] for i in range(p, len(a) - 1)))


def binary(a):
    lo, hi = 1, len(a) - 2
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < a[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


def cases():
    N = 10**5
    res = [
        [0, MAXV, 0],
        [1, 2, 3, 4, 5, 0],
        [9, 0 + 10, 8, 7, 6, 5, 4],
        mountain(10, 1, 50),
        mountain(10, 8, 50),
        mountain(100, 37, 1000),
        mountain(1000, 500),
        mountain(N, 1),
        mountain(N, N - 2),
        mountain(N, N // 2),
        mountain(N, random.randint(1, N - 2)),
        list(range(N - 1)) + [0],
        [N - 1 - i if i else 0 for i in range(N)],
    ]
    for _ in range(200):
        n = random.randint(3, 30)
        a = mountain(n, random.randint(1, n - 2), 100)
        assert binary(a) == a.index(max(a))
    for a in res:
        assert is_mountain(a), a[:10]
        assert binary(a) == a.index(max(a))
    return [lines(arr(a)) for a in res]
