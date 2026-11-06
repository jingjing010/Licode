import json

from genlib import *


def brute(g, r, c):
    m, n = len(g), len(g[0])
    if m * n != r * c:
        return mat(g)
    flat = [x for row in g for x in row]
    return mat([flat[i * c:(i + 1) * c] for i in range(r)])


def ref(text):
    g, r, c = [json.loads(x) for x in text.split("\n") if x.strip()]
    return brute(g, r, c)


def rand_mat(m, n, lo=-1000, hi=1000):
    return [rand_arr(n, lo, hi) for _ in range(m)]


def samples():
    res = []
    g = [[1, 2], [3, 4]]
    for r, c, want in ((1, 4, "[[1,2,3,4]]"), (2, 4, "[[1,2],[3,4]]")):
        assert brute(g, r, c) == want
        res.append((lines(mat(g), r, c), want))
    return res


def cases():
    res = [
        lines(mat([[5]]), 1, 1),
        lines(mat([[5]]), 1, 2),
        lines(mat([[1, 2, 3, 4]]), 4, 1),
        lines(mat([[1], [2], [3], [4]]), 2, 2),
        lines(mat([[1, 2], [3, 4]]), 4, 1),
        lines(mat([[1, 2, 3], [4, 5, 6]]), 3, 2),
        lines(mat([[1, 2, 3], [4, 5, 6]]), 2, 3),
        lines(mat([[-1000, 1000]]), 2, 2),
        lines(mat(rand_mat(3, 8)), 6, 4),
        lines(mat(rand_mat(5, 7)), 7, 5),
        lines(mat(rand_mat(100, 100)), 40, 250),
        lines(mat(rand_mat(100, 100)), 250, 40),
        lines(mat(rand_mat(100, 100)), 300, 300),
        lines(mat(rand_mat(1, 100)), 100, 1),
        lines(mat(rand_mat(100, 3)), 1, 300),
    ]
    return res
