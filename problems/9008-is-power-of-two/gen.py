from genlib import *

U32 = 2**32 - 1
POWERS = {1 << k for k in range(32)}


def samples():
    return [
        (lines(64), "true"),
        (lines(0), "false"),
        (lines(96), "false"),
    ]


def ref(x):
    return x != 0 and (x & (x - 1)) == 0


def cases():
    res = [
        lines(1),
        lines(2),
        lines(3),
        lines(2**31),
        lines(2**31 - 1),
        lines(2**31 + 1),
        lines(U32),
        lines(1024),
        lines(1023),
        lines(0x00010000),
        lines(0x80000001),
    ]
    for _ in range(3):
        res.append(lines(1 << random.randint(0, 31)))
    for _ in range(3):
        res.append(lines(random.randint(0, U32)))
    for x in list(POWERS) + [random.randint(0, U32) for _ in range(3000)] + list(range(0, 5000)):
        assert ref(x) == (x in POWERS)
    assert ref(64) and not ref(0) and not ref(96)
    return res
