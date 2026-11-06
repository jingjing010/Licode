from genlib import *

INT_MIN, INT_MAX = -2**31, 2**31 - 1


def samples():
    return [
        (lines(arr([1, 2, 3, 1])), "true"),
        (lines(arr([1, 2, 1, 3, 5, 6, 4])), "true"),
    ]


def no_equal_neighbors(n, lo, hi):
    a = [random.randint(lo, hi)]
    while len(a) < n:
        x = random.randint(lo, hi)
        if x != a[-1]:
            a.append(x)
    return a


def peaks(a):
    n = len(a)
    return [i for i in range(n)
            if (i == 0 or a[i] > a[i - 1]) and (i == n - 1 or a[i] > a[i + 1])]


def binary_peak(a):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < a[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


def cases():
    res = [
        [1],
        [INT_MIN],
        [1, 2],
        [2, 1],
        [INT_MIN, INT_MAX],
        [INT_MAX, INT_MIN],
        list(range(1000)),
        list(range(1000, 0, -1)),
        [INT_MIN + (i % 2) for i in range(1000)],
        list(range(500)) + list(range(500, 0, -1)),
        no_equal_neighbors(10, -5, 5),
        no_equal_neighbors(100, -3, 3),
        no_equal_neighbors(1000, INT_MIN, INT_MAX),
        no_equal_neighbors(1000, 0, 1),
    ]
    for a in res:
        assert all(a[i] != a[i + 1] for i in range(len(a) - 1))
        assert binary_peak(a) in peaks(a)
    return [lines(arr(a)) for a in res]
