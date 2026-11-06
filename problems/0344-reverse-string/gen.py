import json

from genlib import *

PRINTABLE = "".join(chr(c) for c in range(32, 127))


def ref(a):
    return a[::-1]


def expected(inp):
    return carr(ref(json.loads(inp.strip())))


def samples():
    return [
        (lines(carr("hello")), '["o","l","l","e","h"]'),
        (lines(carr("Hannah")), '["h","a","n","n","a","H"]'),
    ]


def cases():
    res = [
        "a",
        "ab",
        "abc",
        " ",
        "\"\\",
        "A man, a plan",
        rand_str(10, PRINTABLE),
        rand_str(11, PRINTABLE),
        rand_str(1000, PRINTABLE),
        rand_str(10**5, PRINTABLE),
        rand_str(10**5 - 1, "abcdefghijklmnopqrstuvwxyz"),
        "x" * 10**5,
    ]
    return [lines(carr(x)) for x in res]
