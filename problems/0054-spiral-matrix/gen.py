from genlib import *
import json


def samples():
    return [
        (lines(mat([[1, 2, 3], [4, 5, 6], [7, 8, 9]])), "[1,2,3,6,9,8,7,4,5]"),
        (lines(mat([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])), "[1,2,3,4,8,12,11,10,9,5,6,7]"),
    ]


def brute(text):
    """方向数组 + visited 模拟"""
    g = json.loads(text.split("\n")[0])
    m, n = len(g), len(g[0])
    seen = [[False] * n for _ in range(m)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    i = j = d = 0
    out = []
    for _ in range(m * n):
        out.append(g[i][j])
        seen[i][j] = True
        ni, nj = i + dirs[d][0], j + dirs[d][1]
        if not (0 <= ni < m and 0 <= nj < n) or seen[ni][nj]:
            d = (d + 1) % 4
            ni, nj = i + dirs[d][0], j + dirs[d][1]
        i, j = ni, nj
    return arr(out)


def rand_mat(m, n):
    return [rand_arr(n, -100, 100) for _ in range(m)]


def cases():
    res = [
        lines(mat([[7]])),
        lines(mat([[1, 2, 3, 4, 5]])),
        lines(mat([[1], [2], [3], [4]])),
        lines(mat([[1, 2], [3, 4]])),
        lines(mat([[1, 2], [3, 4], [5, 6]])),
        lines(mat([[1, 2, 3], [4, 5, 6]])),
        lines(mat([[-100, 100, 0], [0, -100, 100], [100, 0, -100], [5, 5, 5]])),
    ]
    for m, n in ((4, 4), (5, 3), (3, 7), (10, 10), (10, 1), (1, 10), (9, 10), (10, 7)):
        res.append(lines(mat(rand_mat(m, n))))
    return res
