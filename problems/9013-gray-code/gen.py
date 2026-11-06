from genlib import *

U32 = 2**32 - 1


def samples():
    return [
        (lines(6), "4"),
        (lines(3), "2"),
        (lines(2**31), "4294967295"),
    ]


def to_gray(b):
    return b ^ (b >> 1)


def ref(g):
    b = 0
    while g:
        b ^= g
        g >>= 1
    return b


def cases():
    res = [
        lines(0),
        lines(1),
        lines(U32),
        lines(to_gray(7)),
        lines(to_gray(8)),
        lines(0xC0000000),
        lines(0x55555555),
        lines(0xAAAAAAAA),
        lines(to_gray(1023)),
        lines(to_gray(2**31)),
    ]
    for _ in range(6):
        res.append(lines(random.randint(0, U32)))
    for _ in range(3000):
        b = random.randint(0, U32)
        assert ref(to_gray(b)) == b
        g = random.randint(0, U32)
        assert to_gray(ref(g)) == g
    for b in range(4096):
        assert ref(to_gray(b)) == b and bin(to_gray(b) ^ to_gray(b + 1)).count("1") == 1
    assert ref(6) == 4 and ref(3) == 2 and ref(2**31) == U32
    return res
