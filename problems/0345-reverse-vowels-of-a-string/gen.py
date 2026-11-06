import json

from genlib import *

PRINTABLE = "".join(chr(c) for c in range(32, 127))
VOWELS = "aeiouAEIOU"


def ref(x):
    pos = [i for i, c in enumerate(x) if c in VOWELS]
    t = list(x)
    for a, bb in zip(pos, reversed(pos)):
        t[a] = x[bb]
    return "".join(t)


def _two_ptr(x):
    t = list(x)
    l, r = 0, len(t) - 1
    while l < r:
        if t[l] not in VOWELS:
            l += 1
        elif t[r] not in VOWELS:
            r -= 1
        else:
            t[l], t[r] = t[r], t[l]
            l += 1
            r -= 1
    return "".join(t)


def expected(inp):
    return s(ref(json.loads(inp.strip())))


for _ in range(2000):
    _x = rand_str(random.randint(1, 15), "aEbx \"\\o")
    assert ref(_x) == _two_ptr(_x)


def samples():
    return [
        (lines(s("IceCreAm")), '"AceCreIm"'),
        (lines(s("leetcode")), '"leotcede"'),
    ]


def cases():
    res = [
        "a",
        "b",
        " ",
        "ai",
        "hello",
        "aA",
        "xyz.,!",
        "\"a\\b\"E",
        "AEIOUaeiou",
        rand_str(50, "abcdeiouAEIOU"),
        rand_str(1000, PRINTABLE),
        rand_str(3 * 10**5, PRINTABLE),
        rand_str(3 * 10**5, VOWELS),
        rand_str(3 * 10**5, "bcdfgxyz"),
        rand_str(3 * 10**5, "aeiouAEIOUbcd"),
    ]
    return [lines(s(x)) for x in res]
