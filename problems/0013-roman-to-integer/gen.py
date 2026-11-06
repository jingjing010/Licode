import json

from genlib import *

VALS = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
        (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def to_roman(n):
    out = []
    for v, sym in VALS:
        while n >= v:
            out.append(sym)
            n -= v
    return "".join(out)


def ref(r):
    m = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    ans = 0
    for i, c in enumerate(r):
        if i + 1 < len(r) and m[c] < m[r[i + 1]]:
            ans -= m[c]
        else:
            ans += m[c]
    return ans


def expected(inp):
    return str(ref(json.loads(inp.strip())))


for _n in range(1, 4000):
    assert ref(to_roman(_n)) == _n


def samples():
    return [
        (lines(s("III")), "3"),
        (lines(s("IV")), "4"),
        (lines(s("IX")), "9"),
        (lines(s("LVIII")), "58"),
        (lines(s("MCMXCIV")), "1994"),
    ]


def cases():
    fixed = [1, 3999, 3888, 49, 999, 400, 90, 444, 2024, 1000]
    nums = fixed + random.sample(range(1, 4000), 5)
    return [lines(s(to_roman(n))) for n in nums]
