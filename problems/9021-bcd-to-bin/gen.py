from genlib import *
import json


def ref(bcd):
    return int("%x" % bcd)


def expected(text):
    return arr([ref(v) for v in json.loads(text.split("\n")[0])])


def bcd(v):
    return (v // 10) * 16 + v % 10


def samples():
    res = [
        (lines(arr([89, 35, 18])), "[59,23,12]"),
        (lines(arr([0, 9, 16, 153])), "[0,9,10,99]"),
        (lines(arr([37])), "[25]"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        [0],
        [153],
        [9, 16],
        [bcd(v) for v in range(100)],
        [bcd(v) for v in range(99, -1, -1)],
        [bcd(59), bcd(59), bcd(23), bcd(31), bcd(12), bcd(99)],
        [0x80, 0x90, 0x08, 0x19, 0x91],
    ]
    for n in (10, 100, 1000):
        data.append([bcd(random.randint(0, 99)) for _ in range(n)])
    for _ in range(3):
        data.append([bcd(random.randint(50, 99)) for _ in range(20)])
    for regs in data:
        assert 1 <= len(regs) <= 1000
        for r in regs:
            assert (r >> 4) <= 9 and (r & 15) <= 9
            assert bcd(ref(r)) == r
    return [lines(arr(regs)) for regs in data]
