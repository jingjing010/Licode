import json

from genlib import *

ALNUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def ref(x):
    """中心扩展，返回最靠左的最长回文子串"""
    n, best, start = len(x), 0, 0
    for c in range(2 * n - 1):
        l, r = c // 2, c // 2 + c % 2
        while l >= 0 and r < n and x[l] == x[r]:
            l -= 1
            r += 1
        if r - l - 1 > best or (r - l - 1 == best and l + 1 < start):
            best, start = r - l - 1, l + 1
    return x[start:start + best]


def _brute(x):
    n = len(x)
    for ln in range(n, 0, -1):
        for i in range(n - ln + 1):
            t = x[i:i + ln]
            if t == t[::-1]:
                return t
    return ""


def expected(inp):
    return s(ref(json.loads(inp.strip())))


for _ in range(500):
    _x = rand_str(random.randint(1, 12), "ab" if random.random() < 0.5 else "abc")
    assert _brute(_x) == ref(_x)


def samples():
    return [
        (lines(s("babad")), '"bab"'),
        (lines(s("cbbd")), '"bb"'),
    ]


def embed_pal(n, plen, alphabet=ALNUM):
    """长度 n 的随机串，中间嵌入一段长度 plen 的回文"""
    half = rand_str(plen // 2, alphabet)
    pal = half + (rand_str(1, alphabet) if plen % 2 else "") + half[::-1]
    pos = random.randint(0, n - plen)
    return rand_str(pos, alphabet) + pal + rand_str(n - plen - pos, alphabet)


def cases():
    return [
        lines(s("a")),
        lines(s("ac")),
        lines(s("aaaa")),
        lines(s("abacdfgdcaba")),
        lines(s("Aa1aA")),
        lines(s(rand_str(20, "ab"))),
        lines(s(rand_str(200, "abc"))),
        lines(s(embed_pal(1000, 301))),
        lines(s(embed_pal(1000, 600))),
        lines(s(rand_str(1000, ALNUM))),
        lines(s("a" * 1000)),
        lines(s("a" * 500 + "b" + "a" * 499)),
        lines(s(("ab" * 500))),
        lines(s(("a" * 9 + "b") * 100)),
        lines(s(rand_str(1000, "ab"))),
    ]
