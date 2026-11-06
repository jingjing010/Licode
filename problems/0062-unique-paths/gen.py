from math import comb

from genlib import *

LIMIT = 2 * 10**9


def ref(m, n):
    return comb(m + n - 2, m - 1)


def expected(inp):
    m, n = map(int, inp.split())
    return str(ref(m, n))


def _brute(m, n):
    """暴力递归数路径，只用于小数据交叉验证"""
    if m == 1 or n == 1:
        return 1
    return _brute(m - 1, n) + _brute(m, n - 1)


for _m in range(1, 9):
    for _n in range(1, 9):
        assert _brute(_m, _n) == ref(_m, _n)


def samples():
    return [
        (lines(3, 7), "28"),
        (lines(3, 2), "3"),
        (lines(7, 3), "28"),
        (lines(3, 3), "6"),
    ]


def max_n_for(m):
    """行数为 m 时，答案不超过 2*10^9 的最大列数"""
    n = 1
    while n < 100 and ref(m, n + 1) <= LIMIT:
        n += 1
    return n


def cases():
    res = [
        lines(1, 1),
        lines(1, 100),
        lines(100, 1),
        lines(2, 100),
        lines(100, 2),
        lines(17, 18),
        lines(18, 17),
        lines(10, 10),
    ]
    for m in (3, 5, 9, 13):
        res.append(lines(m, max_n_for(m)))
    for _ in range(4):
        m = random.randint(1, 20)
        n = random.randint(1, max_n_for(m))
        res.append(lines(m, n))
    for t in res:
        m, n = map(int, t.split())
        assert ref(m, n) <= LIMIT
    return res
