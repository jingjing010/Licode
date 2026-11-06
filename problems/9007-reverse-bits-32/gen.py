from genlib import *

U32 = 2**32 - 1


def samples():
    return [
        (lines(1), "2147483648"),
        (lines(43261596), "964176192"),
        (lines(4294967293), "3221225471"),
    ]


def ref(x):
    return int(format(x, "032b")[::-1], 2)


def ref_loop(x):
    r = 0
    for i in range(32):
        if (x >> i) & 1:
            r |= 1 << (31 - i)
    return r


def cases():
    res = [
        lines(0),
        lines(U32),
        lines(2**31),
        lines(0xAAAAAAAA),
        lines(0x0000FFFF),
        lines(0x12345678),
        lines(0x80000001),
        lines(0x000000F0),
    ]
    for _ in range(8):
        res.append(lines(random.randint(0, U32)))
    for _ in range(3000):
        x = random.randint(0, U32)
        assert ref(x) == ref_loop(x) and ref(ref(x)) == x
    assert ref(1) == 2147483648 and ref(43261596) == 964176192 and ref(4294967293) == 3221225471
    return res
