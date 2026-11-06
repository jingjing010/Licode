from genlib import *

U32 = 2**32 - 1


def samples():
    return [
        (lines(U32, 4, 4, 0), "4294967055"),
        (lines(180, 2, 3, 2), "168"),
        (lines(0, 0, 4, 255), "15"),
    ]


def ref(reg, pos, width, val):
    mask = (1 << width) - 1
    return (reg & ~(mask << pos) & U32) | ((val & mask) << pos)


def cases():
    res = [
        lines(0x12345678, 0, 32, 0xCAFEBABE),
        lines(U32, 0, 32, 0),
        lines(0, 31, 1, 1),
        lines(U32, 31, 1, 0),
        lines(0, 31, 1, U32),
        lines(0, 28, 4, U32),
        lines(U32, 0, 1, 2),
        lines(0xDEADBEEF, 8, 8, 0x1FF),
        lines(0xDEADBEEF, 16, 16, 0),
    ]
    for _ in range(8):
        width = random.randint(1, 32)
        pos = random.randint(0, 32 - width)
        res.append(lines(random.randint(0, U32), pos, width, random.randint(0, U32)))
    assert ref(U32, 4, 4, 0) == 4294967055 and ref(180, 2, 3, 2) == 168 and ref(0, 0, 4, 255) == 15
    return res
