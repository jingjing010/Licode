from genlib import *

M = 0xFFFFFFFF


def ref_carry(a, b):
    """模拟 32 位无符号的「异或 + 进位」循环"""
    x, y = a & M, b & M
    while y:
        x, y = x ^ y, ((x & y) << 1) & M
    return x - (1 << 32) if x >> 31 else x


def samples():
    return [
        (lines(1, 2), "3"),
        (lines(2, 3), "5"),
    ]


def cases():
    pairs = [
        (0, 0), (-1000, -1000), (1000, 1000), (-1000, 1000), (-1, 1), (-1, -1),
        (1000, -1), (-7, 3), (0, -1000), (512, 512), (-512, -512), (999, 1),
    ]
    for _ in range(4):
        pairs.append((random.randint(-1000, 1000), random.randint(-1000, 1000)))
    for a in range(-1000, 1001, 7):
        for b in range(-1000, 1001, 3):
            assert ref_carry(a, b) == a + b
    return [lines(a, b) for a, b in pairs]
