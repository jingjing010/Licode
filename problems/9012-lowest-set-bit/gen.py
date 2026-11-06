from genlib import *

U32 = 2**32 - 1


def samples():
    return [
        (lines(12), "2"),
        (lines(2**31), "31"),
        (lines(0), "-1"),
    ]


def ref(x):
    return (x & -x).bit_length() - 1 if x else -1


def ref_loop(x):
    for i in range(32):
        if (x >> i) & 1:
            return i
    return -1


def cases():
    res = [
        lines(1),
        lines(U32),
        lines(0xFFFF0000),
        lines(0x00010000),
        lines(0xAAAAAAAA),
        lines(0x80000001),
        lines(0x00000100),
        lines(0x40000000),
    ]
    for k in random.sample(range(32), 4):
        res.append(lines(random.randint(0, U32 >> (k + 1)) << (k + 1) | (1 << k)))
    for _ in range(3):
        res.append(lines(random.randint(1, U32)))
    xs = [random.randint(0, U32) for _ in range(3000)] + [1 << k for k in range(32)] + list(range(0, 2000))
    for x in xs:
        assert ref(x) == ref_loop(x)
    assert ref(12) == 2 and ref(2**31) == 31 and ref(0) == -1
    return res
