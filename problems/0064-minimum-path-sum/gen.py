import json

from genlib import *


def ref(g):
    m, n = len(g), len(g[0])
    dp = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                dp[i][j] = g[0][0]
            elif i == 0:
                dp[i][j] = dp[i][j - 1] + g[i][j]
            elif j == 0:
                dp[i][j] = dp[i - 1][j] + g[i][j]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + g[i][j]
    return dp[m - 1][n - 1]


def _brute(g, i=0, j=0):
    """枚举所有路径，只用于小数据交叉验证"""
    m, n = len(g), len(g[0])
    if i == m - 1 and j == n - 1:
        return g[i][j]
    best = None
    if i + 1 < m:
        best = _brute(g, i + 1, j)
    if j + 1 < n:
        r = _brute(g, i, j + 1)
        best = r if best is None else min(best, r)
    return g[i][j] + best


def expected(inp):
    return str(ref(json.loads(inp.strip())))


for _ in range(200):
    _m, _n = random.randint(1, 6), random.randint(1, 6)
    _g = [rand_arr(_n, 0, 9) for _ in range(_m)]
    assert _brute(_g) == ref(_g)


def samples():
    return [
        (lines(mat([[1, 3, 1], [1, 5, 1], [4, 2, 1]])), "7"),
        (lines(mat([[1, 2, 3], [4, 5, 6]])), "12"),
    ]


def rand_grid(m, n, lo=0, hi=200):
    return [rand_arr(n, lo, hi) for _ in range(m)]


def cases():
    return [
        lines(mat([[0]])),
        lines(mat([[200]])),
        lines(mat([rand_arr(200, 0, 200)])),
        lines(mat([[x] for x in rand_arr(200, 0, 200)])),
        lines(mat([[0] * 50 for _ in range(50)])),
        lines(mat(rand_grid(3, 4, 0, 9))),
        lines(mat(rand_grid(7, 5, 0, 9))),
        lines(mat(rand_grid(20, 30))),
        lines(mat(rand_grid(100, 37))),
        lines(mat([[200] * 200 for _ in range(200)])),
        lines(mat(rand_grid(200, 200))),
        lines(mat(rand_grid(200, 200, 0, 3))),
    ]
