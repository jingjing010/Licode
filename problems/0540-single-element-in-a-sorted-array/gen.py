from genlib import *
from collections import Counter

MAXV = 10**5


def samples():
    return [
        (lines(arr([1, 1, 2, 3, 3, 4, 4, 8, 8])), "2"),
        (lines(arr([3, 3, 7, 7, 10, 11, 11])), "10"),
    ]


def make(pairs, lo=0, hi=MAXV, pos=None):
    """pairs 个出现两次的数 + 1 个单一元素，单一元素在排序后第 pos 组（None 为随机）"""
    vals = sorted(rand_distinct(pairs + 1, lo, hi))
    if pos is None:
        pos = random.randint(0, pairs)
    single = vals[pos]
    a = []
    for v in vals:
        a += [v] if v == single else [v, v]
    return a, single


def brute(a):
    return [v for v, c in Counter(a).items() if c == 1][0]


def binary(a):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mid % 2:
            mid -= 1
        if a[mid] == a[mid + 1]:
            lo = mid + 2
        else:
            hi = mid
    return a[lo]


def cases():
    res = [
        ([0], 0),
        ([MAXV], MAXV),
        ([1, 2, 2], 1),
        ([1, 1, 2], 2),
        ([0, 0, MAXV], MAXV),
    ]
    for p in (3, 10, 100, 1000):
        res.append(make(p))
    P = (10**5 - 1) // 2
    res.append(make(P, pos=0))
    res.append(make(P, pos=P))
    res.append(make(P, pos=P // 2))
    res.append(make(P))
    res.append(make(P))
    for a, single in res:
        assert brute(a) == single == binary(a)
    for _ in range(200):
        a, single = make(random.randint(0, 20), 0, 60)
        assert brute(a) == single == binary(a)
    return [lines(arr(a)) for a, _ in res]
