from genlib import *

VALS = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
        (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def ref(n):
    out = []
    for v, sym in VALS:
        while n >= v:
            out.append(sym)
            n -= v
    return "".join(out)


def _by_digits(n):
    th = ["", "M", "MM", "MMM"]
    hu = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    te = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    on = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    return th[n // 1000] + hu[n // 100 % 10] + te[n // 10 % 10] + on[n % 10]


def expected(inp):
    return s(ref(int(inp.strip())))


for _n in range(1, 4000):
    assert ref(_n) == _by_digits(_n)


def samples():
    return [
        (lines(3749), '"MMMDCCXLIX"'),
        (lines(58), '"LVIII"'),
        (lines(1994), '"MCMXCIV"'),
    ]


def cases():
    fixed = [1, 3999, 3888, 4, 9, 40, 90, 400, 900, 49, 999, 2000]
    return [lines(n) for n in fixed + random.sample(range(1, 4000), 4)]
