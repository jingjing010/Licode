from genlib import *

INT_MAX = 2**31 - 1


def samples():
    return [
        (lines(5, 4), "4"),
        (lines(1, 1), "1"),
    ]


def calls_needed(n, bad):
    """Python 模拟参考解，返回 (答案, 调用次数)，用于确认上限足够"""
    lo, hi, c = 1, n, 0
    while lo < hi:
        mid = (lo + hi) // 2
        c += 1
        if mid >= bad:
            hi = mid
        else:
            lo = mid + 1
    return lo, c


def cases():
    pairs = [
        (2, 1), (2, 2), (3, 2), (10, 1), (10, 10),
        (INT_MAX, 1), (INT_MAX, INT_MAX), (INT_MAX, INT_MAX - 1),
        (INT_MAX, 2**30), (2**30, 2**30),
    ]
    for _ in range(3):
        n = random.randint(1, 1000)
        pairs.append((n, random.randint(1, n)))
    for _ in range(3):
        n = random.randint(10**8, INT_MAX)
        pairs.append((n, random.randint(1, n)))
    for n, bad in pairs:
        ans, c = calls_needed(n, bad)
        assert ans == bad and c <= 2 * n.bit_length() + 2
    return [lines(n, bad) for n, bad in pairs]
