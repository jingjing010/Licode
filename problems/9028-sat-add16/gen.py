from genlib import *

MAX, MIN = 32767, -32768


def ref(a, b):
    return [max(MIN, min(MAX, x + y)) for x, y in zip(a, b)]


def ref2(a, b):
    # 模拟"16 位补码相加 + 溢出检测"的写法，与 ref 交叉验证
    res = []
    for x, y in zip(a, b):
        r = (x + y) & 0xFFFF
        r = r - 0x10000 if r >= 0x8000 else r
        if (x < 0) == (y < 0) and (r < 0) != (x < 0):
            r = MIN if x < 0 else MAX
        res.append(r)
    return res


def parse(line):
    line = line.strip()[1:-1]
    return [int(t) for t in line.split(",")] if line else []


def expected(text):
    ls = text.split("\n")
    return arr(ref(parse(ls[0]), parse(ls[1])))


def samples():
    res = [
        (lines(arr([1000, -2000, 30000]), arr([234, 500, 10000])), "[1234,-1500,32767]"),
        (lines(arr([-32768, -20000, 32767]), arr([-1, -20000, -32768])), "[-32768,-32768,-1]"),
        (lines(arr([32767, 0, -100]), arr([32767, 0, 100])), "[32767,0,0]"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        ([0], [0]),
        ([32767], [1]),
        ([-32768], [-1]),
        ([-32768], [-32768]),
        ([32767], [-32768]),
        ([16384], [16383]),
        ([16384], [16384]),
        ([-16384], [-16384]),
        ([-16384], [-16385]),
        ([100, -100, 32000, -32000, 1, -1], [-100, 100, 767, -768, 32767, -32768]),
    ]
    for n in (10, 100):
        data.append((rand_arr(n, MIN, MAX), rand_arr(n, MIN, MAX)))
    n = 20000
    data.append((rand_arr(n, MIN, MAX), rand_arr(n, MIN, MAX)))
    data.append((rand_arr(n, -16384, 16383), rand_arr(n, -16384, 16383)))
    data.append((rand_arr(n, 20000, MAX), rand_arr(n, 20000, MAX)))
    data.append((rand_arr(n, MIN, -20000), rand_arr(n, MIN, -20000)))
    for a, b in data:
        assert len(a) == len(b) and 1 <= len(a) <= 20000
        assert all(MIN <= v <= MAX for v in a + b)
        assert ref(a, b) == ref2(a, b)
    return [lines(arr(a), arr(b)) for a, b in data]
