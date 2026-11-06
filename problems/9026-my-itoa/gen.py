from genlib import *

DIG = "0123456789ABCDEF"


def ref(value, base):
    neg = base == 10 and value < 0
    u = -value if neg else value & 0xFFFFFFFF
    out = ""
    while True:
        out = DIG[u % base] + out
        u //= base
        if u == 0:
            break
    return ("-" if neg else "") + out


def expected(text):
    ls = text.split("\n")
    return s(ref(int(ls[0]), int(ls[1])))


def samples():
    res = [
        (lines(255, 16), '"FF"'),
        (lines(-1234, 10), '"-1234"'),
        (lines(10, 2), '"1010"'),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        (0, 10),
        (0, 2),
        (-2147483648, 10),
        (2147483647, 10),
        (-1, 16),
        (-1, 2),
        (-2147483648, 2),
        (-255, 16),
        (12345, 8),
        (-7, 8),
        (100, 3),
        (987654321, 7),
        (65535, 16),
        (random.randint(-2**31, 2**31 - 1), 10),
        (random.randint(-2**31, -1), 16),
        (random.randint(0, 2**31 - 1), random.randint(2, 16)),
    ]
    for v, b in data:
        assert 2 <= b <= 16 and -2**31 <= v < 2**31
        r = ref(v, b)
        assert len(r) <= 33
        if b == 10:
            assert int(r) == v
        else:
            assert int(r, b) == v & 0xFFFFFFFF
    return [lines(v, b) for v, b in data]
