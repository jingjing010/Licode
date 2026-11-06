from collections import Counter

from genlib import *


def make(n, k=2, dup=None):
    """长度 n+1，值在 [1, n]，dup 出现 k 次，其余 n+1-k 个数互不相同且不等于 dup"""
    if dup is None:
        dup = random.randint(1, n)
    rest = random.sample([v for v in range(1, n + 1) if v != dup], n + 1 - k)
    a = [dup] * k + rest
    random.shuffle(a)
    return a


def check(a):
    n = len(a) - 1
    assert n >= 1 and all(1 <= x <= n for x in a)
    c = Counter(a)
    dups = [v for v, t in c.items() if t >= 2]
    assert len(dups) == 1
    return dups[0]


def floyd(a):
    slow = fast = 0
    while True:
        slow = a[slow]
        fast = a[a[fast]]
        if slow == fast:
            break
    slow = 0
    while slow != fast:
        slow, fast = a[slow], a[fast]
    return slow


def samples():
    return [
        (lines(arr([1, 3, 4, 2, 2])), "2"),
        (lines(arr([3, 1, 3, 4, 2])), "3"),
        (lines(arr([3, 3, 3, 3, 3])), "3"),
    ]


def cases():
    for _ in range(500):
        n = random.randint(1, 10)
        a = make(n, random.randint(2, n + 1))
        assert check(a) == floyd(a)
    N = 10**5
    arrays = [
        [1, 1],
        [2, 2, 2],
        [1, 2, 2],
        [2, 1, 1],
        make(10),
        make(100, 30),
        make(1000, 2, 1),
        make(N),
        make(N, 2, N),
        make(N, 2, 1),
        make(N, N + 1),
        make(N, 50000),
        list(range(1, N + 1)) + [N // 2],
        [N] + list(range(1, N + 1)),
    ]
    for a in arrays:
        assert check(a) == floyd(a)
    return [lines(arr(a)) for a in arrays]
