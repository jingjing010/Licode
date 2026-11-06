import itertools

from genlib import *


def ref(n):
    cur = "1"
    for _ in range(n - 1):
        cur = "".join(str(len(list(g))) + k for k, g in itertools.groupby(cur))
    return cur


def expected(inp):
    return s(ref(int(inp.strip())))


assert ref(4) == "1211" and ref(5) == "111221" and len(ref(30)) == 4462


def samples():
    return [
        (lines(4), '"1211"'),
        (lines(1), '"1"'),
    ]


def cases():
    return [lines(n) for n in (2, 3, 5, 6, 10, 15, 20, 25, 28, 29, 30)]
