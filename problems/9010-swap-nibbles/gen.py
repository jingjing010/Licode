from genlib import *


def samples():
    return [
        (lines(18), "33"),
        (lines(171), "186"),
        (lines(15), "240"),
    ]


def ref(x):
    return ((x & 0x0F) << 4) | (x >> 4)


def ref_str(x):
    h = "%02X" % x
    return int(h[1] + h[0], 16)


def cases():
    res = [
        lines(0),
        lines(255),
        lines(240),
        lines(1),
        lines(128),
        lines(0x59),
        lines(0x5A),
        lines(0x88),
        lines(0x7F),
    ]
    for _ in range(6):
        res.append(lines(random.randint(0, 255)))
    for x in range(256):
        assert ref(x) == ref_str(x) and ref(ref(x)) == x
    assert ref(18) == 33 and ref(171) == 186 and ref(15) == 240
    return res
