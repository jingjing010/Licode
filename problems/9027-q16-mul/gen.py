from genlib import *
from fractions import Fraction
import math

MAX, MIN = 2 ** 31 - 1, -2 ** 31


def ref(a, b):
    return max(MIN, min(MAX, (a * b) >> 16))


def ref2(a, b):
    return max(MIN, min(MAX, math.floor(Fraction(a * b, 65536))))


def expected(text):
    ls = text.split("\n")
    return str(ref(int(ls[0]), int(ls[1])))


def q(x):
    return int(round(x * 65536))


def samples():
    res = [
        (lines(98304, 131072), "196608"),
        (lines(-98304, 32768), "-49152"),
        (lines(2147483647, 131072), "2147483647"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        (0, 0), (1, 1), (-1, 1), (-1, -1), (65536, 65536), (65536, -1),
        (MIN, 65536), (MIN, -65536), (MIN, MIN), (MAX, MAX), (MIN, MAX),
        (MAX, -131072), (q(3.14159), q(-2.71828)), (q(0.001), q(0.001)),
        (q(-100.25), q(200.5)), (q(181.0), q(181.0)), (q(-181.0), q(181.0)),
        (12345, -7),
    ]
    for _ in range(3):
        data.append((random.randint(MIN, MAX), random.randint(-2 ** 20, 2 ** 20)))
    for a, b in data:
        assert MIN <= a <= MAX and MIN <= b <= MAX
        assert ref(a, b) == ref2(a, b)
    return [lines(a, b) for a, b in data]
