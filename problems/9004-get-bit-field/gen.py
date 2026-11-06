from genlib import *

U32 = 2**32 - 1


def samples():
    return [
        (lines(0xABCD1234, 8, 8), "18"),
        (lines(180, 2, 3), "5"),
        (lines(U32, 0, 32), "4294967295"),
    ]


def ref(reg, pos, width):
    return (reg >> pos) & ((1 << width) - 1)


def ref_slow(reg, pos, width):
    bits = format(reg, "032b")[::-1][pos:pos + width]
    return int(bits[::-1], 2)


def cases():
    res = [
        lines(0, 0, 32),
        lines(0x12345678, 0, 32),
        lines(U32, 31, 1),
        lines(2**31, 31, 1),
        lines(U32, 0, 1),
        lines(0xDEADBEEF, 16, 16),
        lines(0xDEADBEEF, 0, 16),
        lines(0xDEADBEEF, 1, 31),
    ]
    for _ in range(8):
        width = random.randint(1, 32)
        pos = random.randint(0, 32 - width)
        res.append(lines(random.randint(0, U32), pos, width))
    for _ in range(2000):
        width = random.randint(1, 32)
        pos = random.randint(0, 32 - width)
        reg = random.randint(0, U32)
        assert ref(reg, pos, width) == ref_slow(reg, pos, width)
    assert ref(0xABCD1234, 8, 8) == 18 and ref(180, 2, 3) == 5 and ref(U32, 0, 32) == U32
    return res
