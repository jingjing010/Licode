import json

from genlib import *


def ref(x):
    return (x + x)[1:-1].find(x) != -1


def _brute(x):
    n = len(x)
    return any(n % k == 0 and x[:k] * (n // k) == x for k in range(1, n // 2 + 1))


def expected(inp):
    return b(ref(json.loads(inp.strip())))


for _ in range(3000):
    _x = rand_str(random.randint(1, 12), "ab") if random.random() < 0.5 else rand_str(random.randint(1, 4), "ab") * random.randint(1, 4)
    assert ref(_x) == _brute(_x), _x


def rep(unit_len, times, alphabet="abcdefghijklmnopqrstuvwxyz"):
    return rand_str(unit_len, alphabet) * times


def samples():
    return [
        (lines(s("abab")), "true"),
        (lines(s("aba")), "false"),
        (lines(s("abcabcabcabc")), "true"),
    ]


def cases():
    u = rand_str(100)
    res = [
        "a",
        "aa",
        "ab",
        "aabaaba",
        "abac",
        "ababab",
        "abaababaab",
        rep(3, 7, "ab"),
        "a" * 10**4,
        "a" * 9999 + "b",
        rep(5000, 2),
        rep(1, 9973),
        rep(97, 103),
        rep(100, 100)[:-1] + "z",
        u * 99 + u[:-1] + "z",
        rand_str(10**4),
    ]
    return [lines(s(x)) for x in res]
