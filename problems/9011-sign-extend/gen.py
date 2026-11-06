from genlib import *

U32 = 2**32 - 1


def samples():
    return [
        (lines(4095, 12), "-1"),
        (lines(2047, 12), "2047"),
        (lines(8388608, 24), "-8388608"),
    ]


def ref(raw, bits):
    return raw - (1 << bits) if (raw >> (bits - 1)) & 1 else raw


def ref_xor(raw, bits):
    m = 1 << (bits - 1)
    v = ((raw ^ m) - m) & U32
    return v - (1 << 32) if v >> 31 else v


def cases():
    res = [
        lines(0, 1),
        lines(1, 1),
        lines(U32, 32),
        lines(2**31, 32),
        lines(2**31 - 1, 32),
        lines(0, 32),
        lines(2048, 12),
        lines(0x8000, 16),
        lines(0xFF38, 16),
        lines(0x7FFFFF, 24),
        lines(0xFFFFFF, 24),
        lines(0x1FFF, 13),
    ]
    for _ in range(5):
        bits = random.randint(2, 31)
        res.append(lines(random.randint(0, (1 << bits) - 1), bits))
    for _ in range(5000):
        bits = random.randint(1, 32)
        raw = random.randint(0, (1 << bits) - 1)
        v = ref(raw, bits)
        assert v == ref_xor(raw, bits) and -(1 << (bits - 1)) <= v < (1 << (bits - 1))
    assert ref(4095, 12) == -1 and ref(2047, 12) == 2047 and ref(8388608, 24) == -8388608
    return res
