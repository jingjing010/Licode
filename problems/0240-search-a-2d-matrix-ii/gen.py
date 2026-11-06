from genlib import *
import json

EX = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]


def samples():
    return [
        (lines(mat(EX), 5), "true"),
        (lines(mat(EX), 20), "false"),
    ]


def brute(text):
    ls = text.split("\n")
    g = json.loads(ls[0])
    t = int(ls[1])
    return b(any(t in row for row in g))


def sorted_mat(m, n, start, step):
    """每个元素 = max(上方, 左方) + [0, step] 的随机数，保证行、列都升序"""
    g = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            base = start
            if i > 0:
                base = max(base, g[i - 1][j])
            if j > 0:
                base = max(base, g[i][j - 1])
            g[i][j] = base + random.randint(0, step)
    assert all(-10**9 <= x <= 10**9 for row in g for x in row)
    return g


def absent_target(g, lo, hi):
    vals = set(x for row in g for x in row)
    while True:
        t = random.randint(lo, hi)
        if t not in vals:
            return t


def present_target(g):
    return random.choice(random.choice(g))


def cases():
    res = [
        lines(mat([[5]]), 5),
        lines(mat([[5]]), -5),
        lines(mat([[1, 3, 5, 7, 9]]), 7),
        lines(mat([[1], [3], [5], [7], [9]]), 4),
        lines(mat([[-10**9, 0], [0, 10**9]]), 10**9),
        lines(mat([[-10**9, 0], [0, 10**9]]), -10**9),
        lines(mat([[1, 1], [1, 1]]), 2),
        lines(mat(EX), 30),
        lines(mat(EX), 0),
        lines(mat(EX), 18),
    ]
    g = sorted_mat(8, 6, -50, 5)
    res.append(lines(mat(g), present_target(g)))
    res.append(lines(mat(g), absent_target(g, -60, 120)))
    big = sorted_mat(300, 300, -10**9, 3 * 10**6)
    res.append(lines(mat(big), present_target(big)))
    res.append(lines(mat(big), absent_target(big, -10**9, 10**9)))
    res.append(lines(mat(big), big[299][0]))
    res.append(lines(mat(big), big[0][299]))
    wide = sorted_mat(1, 300, -10**9, 6 * 10**6)
    res.append(lines(mat(wide), absent_target(wide, -10**9, 10**9)))
    return res
