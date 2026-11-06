from genlib import *
import json


def samples():
    return [
        (lines(mat([[1, 2, 3], [4, 5, 6], [7, 8, 9]])), "[[7,4,1],[8,5,2],[9,6,3]]"),
        (lines(mat([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]])),
         "[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]"),
    ]


def brute(text):
    g = json.loads(text.split("\n")[0])
    n = len(g)
    return mat([[g[n - 1 - j][i] for j in range(n)] for i in range(n)])


def rand_sq(n):
    return [rand_arr(n, -1000, 1000) for _ in range(n)]


def cases():
    res = [
        lines(mat([[1]])),
        lines(mat([[-1000]])),
        lines(mat([[1, 2], [3, 4]])),
        lines(mat([[0, 0, 0], [0, 0, 0], [0, 0, 0]])),
        lines(mat([[i * 5 + j + 1 for j in range(5)] for i in range(5)])),
        lines(mat([[1000, -1000], [-1000, 1000]])),
    ]
    for n in (3, 4, 6, 7, 10, 15, 19, 20, 20):
        res.append(lines(mat(rand_sq(n))))
    return res
