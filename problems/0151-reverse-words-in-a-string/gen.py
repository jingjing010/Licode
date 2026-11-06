import json

from genlib import *

WCH = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def ref(x):
    return " ".join(reversed(x.split()))


def _manual(x):
    words, cur = [], ""
    for c in x + " ":
        if c == " ":
            if cur:
                words.append(cur)
            cur = ""
        else:
            cur += c
    return " ".join(words[::-1])


def expected(inp):
    return s(ref(json.loads(inp.strip())))


def rand_sentence(n, word_max=8, space_max=3):
    """长度恰好为 n、至少含一个单词的随机句子"""
    while True:
        parts = [" " * random.randint(0, space_max)]
        while sum(map(len, parts)) < n:
            parts.append(rand_str(random.randint(1, word_max), WCH))
            parts.append(" " * random.randint(1, space_max))
        t = "".join(parts)[:n]
        if t.strip():
            return t


for _ in range(2000):
    _x = rand_sentence(random.randint(1, 20), 3, 3)
    assert ref(_x) == _manual(_x)


def samples():
    return [
        (lines(s("the sky is blue")), '"blue is sky the"'),
        (lines(s("  hello world  ")), '"world hello"'),
        (lines(s("a good   example")), '"example good a"'),
    ]


def cases():
    res = [
        "a",
        " 1 ",
        "Alice does not even like bob",
        "   EPY2giL   ",
        "ab  cd",
        "x" * 10**4,
        " " * 9999 + "q",
        " ".join(rand_str(1, WCH) for _ in range(5000)),
        rand_sentence(100),
        rand_sentence(1000, 12, 5),
        rand_sentence(10**4),
        rand_sentence(10**4, 1, 1),
        rand_sentence(10**4, 50, 20),
    ]
    return [lines(s(x)) for x in res]
