from genlib import *

U32 = 2**32 - 1


def samples():
    return [
        (lines(11), "3"),
        (lines(128), "1"),
        (lines(U32), "32"),
    ]


def ref(x):
    return bin(x).count("1")


def ref_kernighan(x):
    c = 0
    while x:
        x &= x - 1
        c += 1
    return c


def cases():
    res = [
        lines(0),
        lines(1),
        lines(2**31),
        lines(2**31 - 1),
        lines(0xAAAAAAAA),
        lines(0x55555555),
        lines(0x0F0F0F0F),
        lines(0xFFFF0000),
        lines(U32 - 1),
    ]
    for _ in range(7):
        res.append(lines(random.randint(0, U32)))
    for _ in range(3000):
        x = random.randint(0, U32)
        assert ref(x) == ref_kernighan(x)
    assert ref(11) == 3 and ref(128) == 1 and ref(U32) == 32
    return res
