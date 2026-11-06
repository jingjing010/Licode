from genlib import *

U32 = 2**32 - 1


def samples():
    return [
        (lines(4, 6), "5"),
        (lines(U32, U32 - 2), "4294967294"),
        (lines(3, 4), "3"),
    ]


def ref(a, b):
    return (a + b) // 2


def ref_bits(a, b):
    return (a & b) + ((a ^ b) >> 1)


def cases():
    res = [
        lines(0, 0),
        lines(U32, U32),
        lines(0, U32),
        lines(U32, 0),
        lines(1, 0),
        lines(2**31, 2**31),
        lines(2**31, 2**31 - 1),
        lines(U32, 1),
        lines(U32 - 1, U32),
        lines(123456789, 123456789),
    ]
    for _ in range(3):
        res.append(lines(random.randint(2**31, U32), random.randint(2**31, U32)))
    for _ in range(3):
        res.append(lines(random.randint(0, U32), random.randint(0, U32)))
    for _ in range(5000):
        a, b = random.randint(0, U32), random.randint(0, U32)
        assert ref(a, b) == ref_bits(a, b) <= U32
    assert ref(4, 6) == 5 and ref(U32, U32 - 2) == 4294967294 and ref(3, 4) == 3
    return res
