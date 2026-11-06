import itertools
import json
from collections import Counter

from genlib import *

ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def ref(x):
    c = Counter(x)
    pairs = sum(v // 2 * 2 for v in c.values())
    return pairs + (1 if any(v % 2 for v in c.values()) else 0)


def _brute(x):
    best = 0
    for r in range(1, len(x) + 1):
        for sub in itertools.combinations(x, r):
            odd = sum(v % 2 for v in Counter(sub).values())
            if odd <= 1:
                best = max(best, r)
    return best


def expected(inp):
    return str(ref(json.loads(inp.strip())))


for _ in range(200):
    _x = rand_str(random.randint(1, 7), "aAb")
    assert ref(_x) == _brute(_x)


def samples():
    return [
        (lines(s("abccccdd")), "7"),
        (lines(s("a")), "1"),
    ]


def cases():
    N = 2000
    return [lines(s(x)) for x in [
        "Aa",
        "bb",
        "ccc",
        "abc",
        "AaBbCcAaBbCc",
        rand_str(10, "aA"),
        rand_str(100),
        rand_str(N),
        rand_str(N, ALPHA),
        "z" * N,
        "z" * (N - 1),
        "".join(c * 2 for c in ALPHA) * 19 + ALPHA[:N - 1976],
        ALPHA * 38 + ALPHA[:24],
    ]]
