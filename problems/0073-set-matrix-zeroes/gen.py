from genlib import *
import json

INT_MIN, INT_MAX = -2**31, 2**31 - 1


def samples():
    return [
        (lines(mat([[1, 1, 1], [1, 0, 1], [1, 1, 1]])), "[[1,0,1],[0,0,0],[1,0,1]]"),
        (lines(mat([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]])), "[[0,0,0,0],[0,4,5,0],[0,3,1,0]]"),
    ]


def brute(text):
    g = json.loads(text.split("\n")[0])
    m, n = len(g), len(g[0])
    zr = {i for i in range(m) for j in range(n) if g[i][j] == 0}
    zc = {j for i in range(m) for j in range(n) if g[i][j] == 0}
    return mat([[0 if i in zr or j in zc else g[i][j] for j in range(n)] for i in range(m)])


def rand_mat(m, n, zeros, lo=INT_MIN, hi=INT_MAX):
    g = [[random.randint(lo, hi) or 1 for _ in range(n)] for _ in range(m)]
    for _ in range(zeros):
        g[random.randrange(m)][random.randrange(n)] = 0
    return g


def cases():
    res = [
        lines(mat([[0]])),
        lines(mat([[5]])),
        lines(mat([[1, 0, 3]])),
        lines(mat([[1], [0], [3]])),
        lines(mat([[0, 0], [0, 0]])),
        lines(mat([[1, 2, 3], [4, 5, 6]])),
        lines(mat([[1, 2, 0], [4, 5, 6], [7, 8, 9]])),
        lines(mat([[1, 2, 3], [4, 5, 6], [0, 8, 9]])),
        lines(mat([[INT_MIN, INT_MAX], [0, -1]])),
    ]
    for m, n, z in ((3, 5, 1), (6, 4, 2), (10, 10, 3), (30, 20, 5)):
        res.append(lines(mat(rand_mat(m, n, z, -100, 100))))
    res.append(lines(mat(rand_mat(200, 200, 0))))
    res.append(lines(mat(rand_mat(200, 200, 15))))
    res.append(lines(mat(rand_mat(200, 1, 2))))
    res.append(lines(mat(rand_mat(1, 200, 2))))
    return res
