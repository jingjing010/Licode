from genlib import *


def brute(t):
    """逐个尝试切点：每次取最短的合法前缀"""
    res, start, n = [], 0, len(t)
    while start < n:
        for e in range(start, n):
            if not set(t[start:e + 1]) & set(t[e + 1:]):
                res.append(e - start + 1)
                start = e + 1
                break
    return res


def fast(t):
    last = {c: i for i, c in enumerate(t)}
    res, start, end = [], 0, 0
    for i, c in enumerate(t):
        end = max(end, last[c])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res


def blocks(sizes, alphabet="abcdefghijklmnopqrstuvwxyz"):
    """按 sizes 拼出若干段，每段使用互不相同的字母集合"""
    letters = list(alphabet)
    random.shuffle(letters)
    out, k = [], 0
    for sz in sizes:
        use = letters[k:k + random.randint(1, 2)]
        k += len(use)
        seg = [random.choice(use) for _ in range(sz)]
        seg[0] = seg[-1] = use[0]
        out.append("".join(seg))
    return "".join(out)


def samples():
    return [
        (lines(s("ababcbacadefegdehijhklij")), "[9,7,8]"),
        (lines(s("eccbbbbdec")), "[10]"),
    ]


def cases():
    for _ in range(500):
        t = rand_str(random.randint(1, 12), "abcde"[:random.randint(1, 5)])
        assert brute(t) == fast(t)
    letters = "abcdefghijklmnopqrstuvwxyz"
    return [
        lines(s("a")),
        lines(s("ab")),
        lines(s("aa")),
        lines(s("caedbdedda")),
        lines(s(letters)),
        lines(s(rand_str(30, "abc"))),
        lines(s(blocks([5, 1, 7, 3, 2]))),
        lines(s(rand_str(500))),
        lines(s("a" * 500)),
        lines(s((letters * 20)[:500])),
        lines(s("".join(c * 19 for c in letters)[:494])),
        lines(s(blocks([60, 40, 1, 100, 80, 19, 50, 70, 30, 50]))),
        lines(s("a" + rand_str(498, "bcdefgh") + "a")),
    ]
