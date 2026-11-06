from genlib import *


def samples():
    return [
        (lines(65, 0), "0"),
        (lines(65, 1), "1"),
        (lines(7, 0), "1"),
    ]


def ref(data, odd):
    return (bin(data).count("1") & 1) ^ odd


def ref_xor(data, odd):
    p = 0
    for i in range(8):
        p ^= (data >> i) & 1
    return p ^ odd


def cases():
    res = [
        lines(0, 0),
        lines(0, 1),
        lines(255, 0),
        lines(255, 1),
        lines(128, 0),
        lines(128, 1),
        lines(0x55, 1),
        lines(0xFE, 0),
        lines(0x7F, 1),
    ]
    for _ in range(6):
        res.append(lines(random.randint(0, 255), random.randint(0, 1)))
    for data in range(256):
        for odd in (0, 1):
            p = ref(data, odd)
            assert p == ref_xor(data, odd)
            assert (bin(data).count("1") + p) % 2 == odd
    assert ref(65, 0) == 0 and ref(65, 1) == 1 and ref(7, 0) == 1
    return res
