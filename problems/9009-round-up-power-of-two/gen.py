from genlib import *

MAXX = 2**31


def samples():
    return [
        (lines(5), "8"),
        (lines(16), "16"),
        (lines(1), "1"),
    ]


def ref(x):
    return 1 << (x - 1).bit_length()


def ref_loop(x):
    p = 1
    while p < x:
        p *= 2
    return p


def cases():
    res = [
        lines(2),
        lines(3),
        lines(100),
        lines(MAXX),
        lines(MAXX - 1),
        lines(2**30 + 1),
        lines(2**30),
        lines(65535),
        lines(65537),
        lines(1000000),
    ]
    for _ in range(6):
        res.append(lines(random.randint(1, MAXX)))
    xs = list(range(1, 5000)) + [random.randint(1, MAXX) for _ in range(3000)]
    xs += [1 << k for k in range(32)] + [(1 << k) + 1 for k in range(31)] + [(1 << k) - 1 for k in range(2, 32)]
    for x in xs:
        assert ref(x) == ref_loop(x)
    assert ref(5) == 8 and ref(16) == 16 and ref(1) == 1
    return res
