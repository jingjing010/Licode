from genlib import *
from collections import Counter


def make(n, alphabet="abcdefghijklmnopqrstuvwxyz", extra=None):
    s = rand_str(n, alphabet)
    c = extra if extra is not None else random.choice(alphabet)
    t = list(s)
    t.insert(random.randint(0, n), c)
    random.shuffle(t)
    return s, "".join(t), c


def brute(s, t):
    d = Counter(t) - Counter(s)
    assert sum(d.values()) == 1
    return next(iter(d))


def ref_xor(s, t):
    x = 0
    for ch in s + t:
        x ^= ord(ch)
    return chr(x)


def samples():
    return [
        (lines(s("abcd"), s("abcde")), '"e"'),
        (lines(s(""), s("y")), '"y"'),
    ]


def cases():
    tests = [
        ("", "a", "a"),
        ("", "z", "z"),
        ("a", "aa", "a"),
        ("zzzz", "zzzzz", "z"),
        ("abc", "cbaa", "a"),
        make(10),
        make(100),
        make(1000),
        make(1000, extra="a"),
        make(1000, "ab"),
        make(1000, "z"),
        make(999, extra="z"),
    ]
    sorted_s = "".join(sorted(rand_str(1000)))
    tests.append((sorted_s, sorted_s + "q", "q"))
    tests.append((sorted_s, "m" + sorted_s, "m"))
    for _ in range(300):
        a, b, c = make(random.randint(0, 20), "abcde")
        assert brute(a, b) == ref_xor(a, b) == c
    res = []
    for a, b, c in tests:
        assert brute(a, b) == ref_xor(a, b) == c
        res.append(lines(s(a), s(b)))
    return res
