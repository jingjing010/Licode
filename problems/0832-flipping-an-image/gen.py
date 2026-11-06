from genlib import *


def samples():
    return [
        (lines(mat([[1, 1, 0], [1, 0, 1], [0, 0, 0]])), "[[1,0,0],[0,1,0],[1,1,1]]"),
        (lines(mat([[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0]])),
         "[[1,1,0,0],[0,1,1,0],[0,0,0,1],[1,0,1,0]]"),
    ]


def rand_img(n):
    return [rand_arr(n, 0, 1) for _ in range(n)]


def cases():
    return [
        lines(mat([[0]])),
        lines(mat([[1]])),
        lines(mat([[1, 0], [0, 1]])),
        lines(mat([[0, 0], [0, 0]])),
        lines(mat([[1] * 5 for _ in range(5)])),
        lines(mat(rand_img(3))),
        lines(mat(rand_img(6))),
        lines(mat(rand_img(9))),
        lines(mat(rand_img(15))),
        lines(mat(rand_img(19))),
        lines(mat(rand_img(20))),
        lines(mat(rand_img(20))),
    ]
