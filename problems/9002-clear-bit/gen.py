from genlib import *

U32 = 2**32 - 1


def samples():
    return [
        (lines(15, 2), "11"),
        (lines(8, 3), "0"),
        (lines(5, 1), "5"),
    ]


def cases():
    res = [
        lines(0, 0),
        lines(0, 31),
        lines(U32, 0),
        lines(U32, 31),
        lines(2**31, 31),
        lines(2**31, 0),
        lines(1, 0),
    ]
    for _ in range(8):
        res.append(lines(random.randint(0, U32), random.randint(0, 31)))
    return res
