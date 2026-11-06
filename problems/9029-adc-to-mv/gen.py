from genlib import *
from fractions import Fraction


def ref(raw, bits, vref):
    fs = (1 << bits) - 1
    return [(r * vref + fs // 2) // fs for r in raw]


def ref2(raw, bits, vref):
    # 用精确分数四舍五入，与 ref 交叉验证（fs 为奇数，不会出现恰好 .5）
    fs = (1 << bits) - 1
    res = []
    for r in raw:
        q = Fraction(r * vref, fs)
        assert q - int(q) != Fraction(1, 2)
        res.append(int(q + Fraction(1, 2)))
    return res


def parse(line):
    line = line.strip()[1:-1]
    return [int(t) for t in line.split(",")] if line else []


def expected(text):
    ls = text.split("\n")
    return arr(ref(parse(ls[0]), int(ls[1]), int(ls[2])))


def samples():
    res = [
        (lines(arr([0, 4095, 2048]), 12, 3300), "[0,3300,1650]"),
        (lines(arr([1000, 3000]), 12, 5000), "[1221,3663]"),
        (lines(arr([65535, 40000, 12345]), 16, 50000), "[50000,30518,9419]"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        ([0], 8, 1),
        ([255], 8, 1),
        ([127, 128], 8, 1),
        ([65535], 16, 65535),
        ([65535, 65534, 32768, 32767, 1, 0], 16, 65535),
        ([1, 2, 3, 4094], 12, 3300),
        ([511, 1023, 0], 10, 5000),
        ([16383, 8192], 14, 2500),
        (list(range(256)), 8, 3300),
        (rand_arr(300, 0, 4095), 12, 3300),
    ]
    for bits in (8, 12, 16):
        fs = (1 << bits) - 1
        data.append((rand_arr(1000, 0, fs), bits, random.randint(1, 65535)))
    data.append((rand_arr(1000, 60000, 65535), 16, 65535))
    data.append((rand_arr(1000, 0, 65535), 16, random.randint(40000, 65535)))
    for raw, bits, vref in data:
        assert 1 <= len(raw) <= 1000 and 8 <= bits <= 16 and 1 <= vref <= 65535
        assert all(0 <= r < (1 << bits) for r in raw)
        assert ref(raw, bits, vref) == ref2(raw, bits, vref)
    return [lines(arr(raw), bits, vref) for raw, bits, vref in data]
