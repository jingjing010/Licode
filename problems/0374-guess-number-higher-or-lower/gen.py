from genlib import *

INT_MAX = 2**31 - 1


def samples():
    return [
        (lines(10, 6), "6"),
        (lines(1, 1), "1"),
        (lines(2, 1), "1"),
    ]


def simulate(n, pick):
    """Python 模拟参考解，返回 (答案, 调用次数)，用于确认上限足够"""
    lo, hi, c = 1, n, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        c += 1
        if mid == pick:
            return mid, c
        if mid > pick:
            hi = mid - 1
        else:
            lo = mid + 1
    return -1, c


def cases():
    pairs = [
        (2, 2), (3, 1), (3, 3), (100, 50), (100, 100),
        (INT_MAX, 1), (INT_MAX, INT_MAX), (INT_MAX, INT_MAX - 1),
        (INT_MAX, 2**30), (2**30, 2**30 - 1),
    ]
    for _ in range(3):
        n = random.randint(1, 1000)
        pairs.append((n, random.randint(1, n)))
    for _ in range(3):
        n = random.randint(10**8, INT_MAX)
        pairs.append((n, random.randint(1, n)))
    for n, pick in pairs:
        ans, c = simulate(n, pick)
        assert ans == pick and c <= 2 * n.bit_length() + 2
    return [lines(n, pick) for n, pick in pairs]
