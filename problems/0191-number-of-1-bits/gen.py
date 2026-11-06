from genlib import *

U32 = 2**32 - 1


def ref(x):
    return bin(x).count("1")


def ref_kernighan(x):
    c = 0
    while x:
        x &= x - 1
        c += 1
    return c


def samples():
    return [
        (lines(11), "3"),
        (lines(128), "1"),
        (lines(4294967293), "31"),
    ]


def cases():
    res = [
        lines(0),
        lines(1),
        lines(U32),
        lines(2**31),
        lines(2**31 - 1),
        lines(0xAAAAAAAA),
        lines(0x0F0F0F0F),
        lines(0x80000001),
        lines(2147483645),
    ]
    for _ in range(6):
        res.append(lines(random.randint(0, U32)))
    for _ in range(3000):
        x = random.randint(0, U32)
        assert ref(x) == ref_kernighan(x)
    assert ref(11) == 3 and ref(128) == 1 and ref(4294967293) == 31
    return res
