from genlib import *

DIG = "0123456789ABCDEF"


def ref(value, base):
    if base == 10:
        return str(value)
    u = value & 0xFFFFFFFF
    out = ""
    while True:
        out = DIG[u % base] + out
        u //= base
        if u == 0:
            return out


def expected(text):
    ls = text.split("\n")
    return s(ref(int(ls[0]), int(ls[1])))


def samples():
    res = [
        (lines(1234, 10), s("1234")),
        (lines(-255, 10), s("-255")),
        (lines(255, 16), s("FF")),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        (0, 10), (0, 2), (0, 16),
        (-1, 10), (-1, 16), (-1, 2),
        (-2147483648, 10), (-2147483648, 16), (2147483647, 2),
        (2147483647, 10), (10, 16), (5, 2), (511, 8), (100, 3),
        (35, 16), (-123456, 7), (65535, 16), (1000000, 10),
    ]
    for _ in range(3):
        data.append((random.randint(-2 ** 31, 2 ** 31 - 1), random.randint(2, 16)))
    for v, b in data:
        r = ref(v, b)
        assert len(r) <= 33
        if b == 10:
            assert int(r) == v
        else:
            assert int(r, b) == v & 0xFFFFFFFF
    return [lines(v, b) for v, b in data]
