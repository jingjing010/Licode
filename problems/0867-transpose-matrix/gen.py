from genlib import *


def samples():
    return [
        (lines(mat([[1, 2, 3], [4, 5, 6], [7, 8, 9]])), "[[1,4,7],[2,5,8],[3,6,9]]"),
        (lines(mat([[1, 2, 3], [4, 5, 6]])), "[[1,4],[2,5],[3,6]]"),
    ]


def rand_mat(m, n, lo=-10**9, hi=10**9):
    return [rand_arr(n, lo, hi) for _ in range(m)]


def cases():
    return [
        lines(mat([[5]])),
        lines(mat([[-10**9]])),
        lines(mat([[1, 2, 3, 4, 5]])),
        lines(mat([[1], [2], [3], [4]])),
        lines(mat([[10**9, -10**9], [0, 7]])),
        lines(mat(rand_mat(3, 7, -9, 9))),
        lines(mat(rand_mat(20, 13))),
        lines(mat(rand_mat(100, 1000))),
        lines(mat(rand_mat(1000, 100))),
        lines(mat(rand_mat(316, 316))),
        lines(mat(rand_mat(1, 1000))),
        lines(mat(rand_mat(1000, 1))),
        lines(mat(rand_mat(250, 400))),
    ]
