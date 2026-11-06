from genlib import *
from math import isqrt

INT_MAX = 2**31 - 1


def samples():
    return [
        (lines(5), "2"),
        (lines(8), "3"),
    ]


def brute(n):
    k, used = 0, 0
    while used + k + 1 <= n:
        k += 1
        used += k
    return k


def formula(n):
    return (isqrt(8 * n + 1) - 1) // 2


def cases():
    ns = [1, 2, 3, 6, 10, 2**30, INT_MAX, INT_MAX - 1,
          65535 * 65536 // 2, 65535 * 65536 // 2 - 1, 65534 * 65535 // 2]
    ns += [random.randint(1, 10**5) for _ in range(3)]
    ns += [random.randint(10**9, INT_MAX) for _ in range(3)]
    for n in ns:
        assert 1 <= n <= INT_MAX
    for n in list(range(1, 3000)) + [n for n in ns if n <= 10**6]:
        assert brute(n) == formula(n)
    return [lines(n) for n in ns]
