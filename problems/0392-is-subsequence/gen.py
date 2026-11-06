import itertools
import json

from genlib import *


def ref(x, y):
    it = iter(y)
    return all(c in it for c in x)


def _brute(x, y):
    """枚举 y 的所有子序列（只用于很短的串）"""
    for k in range(len(y) + 1):
        for comb in itertools.combinations(y, k):
            if "".join(comb) == x:
                return True
    return False


def expected(inp):
    ls = inp.strip().split("\n")
    return b(ref(json.loads(ls[0]), json.loads(ls[1])))


for _ in range(500):
    _t = rand_str(random.randint(0, 7), "abc")
    _s = rand_str(random.randint(0, 4), "abc")
    assert ref(_s, _t) == _brute(_s, _t)


def planted(slen, tlen, alphabet="abcdefghijklmnopqrstuvwxyz"):
    """t 随机，s 是从 t 中按顺序挑出的 slen 个字符（一定是子序列）"""
    t = rand_str(tlen, alphabet)
    idx = sorted(random.sample(range(tlen), slen))
    return "".join(t[i] for i in idx), t


def broken(slen, tlen, alphabet="abcdefghijklmnopqrstuvwxyz"):
    """在 planted 的基础上把 s 的最后一个字符改成 t 中不存在的字母，一定不是子序列"""
    x, y = planted(slen, tlen, alphabet[:-1])
    return x[:-1] + alphabet[-1], y


def samples():
    return [
        (lines(s("abc"), s("ahbgdc")), "true"),
        (lines(s("axc"), s("ahbgdc")), "false"),
    ]


def cases():
    res = [
        ("", ""),
        ("", "abc"),
        ("a", ""),
        ("a", "a"),
        ("b", "abc"),
        ("acb", "ahbgdc"),
        ("aaaaaa", "bbaaaa"),
        ("abc", "abc"),
        planted(10, 50),
        planted(100, 10**4),
        broken(100, 10**4),
        ("a" * 100, "a" * 99 + "b" * 9901),
        ("ab" * 50, "a" * 5000 + "b" * 5000),
        (rand_str(100, "ab"), rand_str(10**4, "ab")),
        ("z" * 100, "y" * 10**4),
    ]
    return [lines(s(x), s(y)) for x, y in res]
