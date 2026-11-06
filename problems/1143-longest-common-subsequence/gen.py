import json
from itertools import combinations

from genlib import *


def ref(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def _is_subseq(t, b):
    it = iter(b)
    return all(c in it for c in t)


def _brute(a, b):
    """枚举 a 的所有子序列（从长到短），只用于小数据交叉验证"""
    for k in range(len(a), 0, -1):
        for idx in combinations(range(len(a)), k):
            if _is_subseq("".join(a[i] for i in idx), b):
                return k
    return 0


def expected(inp):
    a, b = [json.loads(x) for x in inp.strip().split("\n")]
    return str(ref(a, b))


for _ in range(300):
    _a = rand_str(random.randint(1, 8), "abc")
    _b = rand_str(random.randint(1, 8), "abcd")
    assert _brute(_a, _b) == ref(_a, _b)


def samples():
    return [
        (lines(s("abcde"), s("ace")), "3"),
        (lines(s("abc"), s("abc")), "3"),
        (lines(s("abc"), s("def")), "0"),
    ]


def cases():
    big = rand_str(1000)
    return [
        lines(s("a"), s("a")),
        lines(s("a"), s("b")),
        lines(s("bsbininm"), s("jmjkbkjkv")),
        lines(s("ezupkr"), s("ubmrapg")),
        lines(s(rand_str(10, "ab")), s(rand_str(12, "ab"))),
        lines(s(rand_str(50, "abc")), s(rand_str(60, "abc"))),
        lines(s(rand_str(300)), s(rand_str(200))),
        lines(s("a" * 1000), s("a" * 1000)),
        lines(s("a" * 1000), s("b" * 1000)),
        lines(s(big), s(big[::-1])),
        lines(s(big), s(big)),
        lines(s(rand_str(1000)), s(rand_str(1000))),
        lines(s(rand_str(1000, "ab")), s(rand_str(1000, "ab"))),
        lines(s(rand_str(1000)), s("z")),
    ]
