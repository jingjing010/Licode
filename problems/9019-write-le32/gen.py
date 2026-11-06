from genlib import *


def samples():
    return [
        (lines(arr([0, 0, 0, 0]), 0, 305419896), "[120,86,52,18]"),
        (lines(arr([2, 1, 0, 0, 0, 0, 255]), 2, 1000), "[2,1,232,3,0,0,255]"),
        (lines(arr([9, 9, 9, 9, 9]), 1, 4294967295), "[9,255,255,255,255]"),
    ]


def cases():
    res = [
        lines(arr([255, 255, 255, 255]), 0, 0),
        lines(arr([0, 0, 0, 0]), 0, 0x80000000),
        lines(arr([0, 0, 0, 0, 0, 0]), 2, 0x7FFFFFFF),
        lines(arr([170, 170, 170, 170, 170, 170, 170, 170]), 3, 0xDEADBEEF),
        lines(arr([1, 2, 3, 4, 5]), 0, 1),
    ]
    for n in (6, 30, 1000):
        buf = rand_arr(n, 0, 255)
        res.append(lines(arr(buf), random.randint(0, n - 4), random.randint(0, 0xFFFFFFFF)))
    for _ in range(3):
        buf = rand_arr(12, 0, 255)
        res.append(lines(arr(buf), random.randint(0, 8), random.randint(0x80000000, 0xFFFFFFFF)))
    buf = rand_arr(1000, 0, 255)
    res.append(lines(arr(buf), 996, random.randint(0, 0xFFFFFFFF)))
    return res
