from collections import Counter

from genlib import *

V = 10**9


def make(n, lo=-V, hi=V, extra=0, others=None):
    """长度 n，多数元素恰好出现 n//2 + 1 + extra 次，其余从 others 个不同值里随机取"""
    k = min(n, n // 2 + 1 + extra)
    vals = rand_distinct((others or n) + 1, lo, hi)
    major = vals[0]
    a = [major] * k + [random.choice(vals[1:]) for _ in range(n - k)]
    random.shuffle(a)
    return a


def majority(a):
    v, c = Counter(a).most_common(1)[0]
    assert c > len(a) // 2
    return v


def moore(a):
    cand = cnt = 0
    for x in a:
        if cnt == 0:
            cand = x
        cnt += 1 if x == cand else -1
    return cand


def samples():
    return [
        (lines(arr([3, 2, 3])), "3"),
        (lines(arr([2, 2, 1, 1, 1, 2, 2])), "2"),
    ]


def cases():
    for _ in range(300):
        a = make(random.randint(1, 15), -3, 3, random.randint(0, 3), 3)
        assert majority(a) == moore(a)
    n = 5 * 10**4
    tail = [7] * (n // 2 + 1)
    arrays = [
        [-1000000000],
        [1, 1],
        [6, 5, 5],
        [1, 2, 1, 2, 1],
        make(10, -10, 10),
        make(1001),
        [V] * n,
        make(n),
        make(n - 1, others=1),
        make(n, extra=10000),
        list(range(-(n // 2) + 1, 0)) + tail,
        tail + rand_distinct(n // 2 - 1, -V, 0),
        make(n, -V, -V + n * 2),
    ]
    for a in arrays:
        assert 1 <= len(a) <= n and majority(a) == moore(a)
    return [lines(arr(a)) for a in arrays]
