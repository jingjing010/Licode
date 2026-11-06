from genlib import *


def samples():
    return [
        (lines(305419896), "2018915346"),
        (lines(4278190080), "255"),
        (lines(1), "16777216"),
    ]


def cases():
    res = [lines(v) for v in (0, 0xFFFFFFFF, 0x80000000, 0x7FFFFFFF, 0x000000FF,
                              0x0000FF00, 0x00FF0000, 0xC0A80001, 0xDEADBEEF)]
    for _ in range(6):
        res.append(lines(random.randint(0, 0xFFFFFFFF)))
    return res
