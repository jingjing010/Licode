from genlib import *


def samples():
    return [
        (lines(arr([1, 2, 3, 4, 5]), 3), "[1,2,3,0,0]"),
        (lines(arr([255, 0, 128, 7]), 4), "[255,0,128,7]"),
        (lines(arr([9, 8, 7]), 0), "[0,0,0]"),
    ]


def cases():
    res = [
        lines(arr([42]), 1),
        lines(arr([42]), 0),
        lines(arr([255] * 8), 7),
        lines(arr([0, 1, 0, 1, 0]), 5),
    ]
    for n in (7, 31, 64, 1000):
        res.append(lines(arr(rand_arr(n, 1, 255)), random.randint(1, n)))
    for n in (33, 4097):
        res.append(lines(arr(rand_arr(n, 0, 255)), n))
    res.append(lines(arr(rand_arr(10**5, 1, 255)), 10**5))
    res.append(lines(arr(rand_arr(10**5, 1, 255)), 10**5 - 1))
    return res
