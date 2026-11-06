import json
from collections import Counter

from genlib import *

LOWER = "abcdefghijklmnopqrstuvwxyz"


def ref(x):
    c = Counter(x)
    for i, ch in enumerate(x):
        if c[ch] == 1:
            return i
    return -1


def _brute(x):
    for i, ch in enumerate(x):
        if x.count(ch) == 1:
            return i
    return -1


def expected(inp):
    return str(ref(json.loads(inp.strip())))


for _ in range(2000):
    _x = rand_str(random.randint(1, 10), "abcd")
    assert ref(_x) == _brute(_x)


def unique_at(n, pos, ch="z", alphabet="abcdefghijklmnopqrstuvwxy"):
    """除了下标 pos 处的 ch 之外，其余字符都至少出现两次"""
    body = list(alphabet * 2) + [random.choice(alphabet) for _ in range(n - 1 - 2 * len(alphabet))]
    random.shuffle(body)
    return "".join(body[:pos]) + ch + "".join(body[pos:])


def samples():
    return [
        (lines(s("leetcode")), "0"),
        (lines(s("loveleetcode")), "2"),
        (lines(s("aabb")), "-1"),
    ]


def cases():
    res = [
        "z",
        "zz",
        "ab",
        "aab",
        "abcabcd",
        "dddccdbba",
        rand_str(20, "abc"),
        rand_str(100),
        unique_at(1000, 999),
        unique_at(10**5, 0),
        unique_at(10**5, 10**5 - 1),
        unique_at(10**5, 54321),
        "".join(random.sample(LOWER, 26)) * (10**5 // 26) + "abc",
        rand_str(10**5),
        rand_str(10**5 - 1, "ab") + "c",
    ]
    return [lines(s(x)) for x in res]
