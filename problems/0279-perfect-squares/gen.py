from genlib import *

N = 10**4
DP = [0] + [N] * N
for _i in range(1, N + 1):
    _j = 1
    while _j * _j <= _i:
        DP[_i] = min(DP[_i], DP[_i - _j * _j] + 1)
        _j += 1


def fast(n):
    """与 solution.c 相同的数学解法"""
    def sq(x):
        r = int(x ** 0.5)
        while r * r > x:
            r -= 1
        while (r + 1) * (r + 1) <= x:
            r += 1
        return r * r == x
    if sq(n):
        return 1
    m = n
    while m % 4 == 0:
        m //= 4
    if m % 8 == 7:
        return 4
    i = 1
    while i * i < n:
        if sq(n - i * i):
            return 2
        i += 1
    return 3


assert all(fast(i) == DP[i] for i in range(1, N + 1))


def samples():
    return [
        (lines(12), "3"),
        (lines(13), "2"),
    ]


def cases():
    res = []
    for k in (1, 2, 3, 4):
        with_k = [i for i in range(1, N + 1) if DP[i] == k]
        res += [with_k[0], with_k[1], with_k[-1]]
    res += random.sample(range(1, N + 1), 6)
    return [lines(n) for n in res]
