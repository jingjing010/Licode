from genlib import *


def samples():
    return [
        (lines(4660), "13330"),
        (lines(255), "65280"),
        (lines(0), "0"),
    ]


def cases():
    res = [lines(v) for v in (65535, 65280, 1, 256, 0x8000, 0x0080, 0xABCD, 0x00FF + 0x0100)]
    for _ in range(6):
        res.append(lines(random.randint(0, 65535)))
    return res
