from genlib import *


def samples():
    return [
        (lines(arr([18, 52, 86, 120]), 0), "305419896"),
        (lines(arr([170, 0, 1, 134, 160, 85]), 1), "100000"),
        (lines(arr([1, 255, 255, 255, 255]), 1), "4294967295"),
    ]


def cases():
    res = [
        lines(arr([0, 0, 0, 0]), 0),
        lines(arr([128, 0, 0, 0]), 0),
        lines(arr([0, 0, 0, 128]), 0),
        lines(arr([127, 255, 255, 255]), 0),
        lines(arr([255, 1, 2, 3, 4]), 0),
        lines(arr([9, 8, 7, 6, 5, 4, 3, 2, 1]), 5),
    ]
    for n in (7, 50, 1000):
        buf = rand_arr(n, 0, 255)
        res.append(lines(arr(buf), random.randint(0, n - 4)))
    for _ in range(3):
        buf = rand_arr(20, 128, 255)
        res.append(lines(arr(buf), random.randint(0, 16)))
    buf = rand_arr(1000, 0, 255)
    res.append(lines(arr(buf), 996))
    return res
