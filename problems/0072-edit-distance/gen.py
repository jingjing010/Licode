from functools import lru_cache

from genlib import *


def brute(a, b):
    """记忆化递归（从前往后），与 solution 的二维表写法不同，用于交叉验证"""
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        if a[i] == b[j]:
            return f(i + 1, j + 1)
        return 1 + min(f(i + 1, j + 1), f(i + 1, j), f(i, j + 1))
    return f(0, 0)


def fast(a, b):
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        left_up, dp[0] = dp[0], i
        for j in range(1, n + 1):
            up = dp[j]
            dp[j] = left_up if a[i - 1] == b[j - 1] else 1 + min(left_up, up, dp[j - 1])
            left_up = up
    return dp[n]


def mutate(t, k):
    """对 t 做 k 次随机编辑"""
    t = list(t)
    for _ in range(k):
        op = random.randint(0, 2)
        p = random.randint(0, len(t))
        if op == 0 or not t:
            t.insert(p, rand_str(1))
        elif op == 1:
            del t[min(p, len(t) - 1)]
        else:
            t[min(p, len(t) - 1)] = rand_str(1)
    return "".join(t)


def samples():
    return [
        (lines(s("horse"), s("ros")), "3"),
        (lines(s("intention"), s("execution")), "5"),
    ]


def cases():
    for _ in range(400):
        a = rand_str(random.randint(0, 8), "abc")
        b = rand_str(random.randint(0, 8), "abc")
        assert brute(a, b) == fast(a, b)
    big = rand_str(500)
    return [
        lines(s(""), s("")),
        lines(s(""), s("abc")),
        lines(s("abc"), s("")),
        lines(s("a"), s("a")),
        lines(s("a"), s("b")),
        lines(s("abc"), s("cba")),
        lines(s("dinitrophenylhydrazine"), s("benzalphenylhydrazone")),
        lines(s(rand_str(20, "ab")), s(rand_str(25, "ab"))),
        lines(s(rand_str(100, "abc")), s(rand_str(80, "abc"))),
        lines(s(big), s(mutate(big, 30))),
        lines(s(big), s(big)),
        lines(s("a" * 500), s("b" * 500)),
        lines(s(rand_str(500)), s(rand_str(500))),
        lines(s(""), s(rand_str(500))),
        lines(s(rand_str(500, "ab")), s(rand_str(499, "ab"))),
    ]
