from genlib import *


def samples():
    return [
        (lines(arr([18, 52, 255, 254, 128, 0])), "[4660,-2,-32768]"),
        (lines(arr([64, 0, 192, 0, 0, 16])), "[16384,-16384,16]"),
        (lines(arr([127, 255])), "[32767]"),
    ]


def cases():
    res = [
        lines(arr([0, 0])),
        lines(arr([255, 255])),
        lines(arr([128, 1])),
        lines(arr([0, 128, 0, 255, 1, 0])),
        lines(arr([255, 0, 0, 255, 254, 255])),
    ]
    for n in (14, 100, 1000):
        res.append(lines(arr(rand_arr(n, 0, 255))))
    for _ in range(3):
        res.append(lines(arr(rand_arr(20, 128, 255))))
    res.append(lines(arr(rand_arr(1000, 0, 255))))
    return res
