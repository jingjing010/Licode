from genlib import *

U32 = 2**32 - 1


def samples():
    return [
        (lines(0, 0), "1"),
        (lines(5, 0), "4"),
        (lines(0, 31), "2147483648"),
    ]


def ref(reg, n):
    return reg ^ (1 << n)


def ref_slow(reg, n):
    bit = (reg >> n) & 1
    return reg - 2**n if bit else reg + 2**n


def cases():
    res = [
        lines(U32, 0),
        lines(U32, 31),
        lines(2**31, 31),
        lines(2**31 - 1, 31),
        lines(1, 0),
        lines(0xAAAAAAAA, 1),
        lines(0x55555555, 1),
    ]
    for _ in range(8):
        res.append(lines(random.randint(0, U32), random.randint(0, 31)))
    for _ in range(2000):
        reg, n = random.randint(0, U32), random.randint(0, 31)
        assert ref(reg, n) == ref_slow(reg, n)
    assert ref(0, 0) == 1 and ref(5, 0) == 4 and ref(0, 31) == 2147483648
    return res
