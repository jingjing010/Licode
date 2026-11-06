from genlib import *

N = 2 * 10**4
XCHECK_LIMIT = 5000


def brute(t):
    while "abc" in t:
        t = t.replace("abc", "", 1)
    return t == ""


def expect(inp):
    import json
    return "true" if brute(json.loads(inp.splitlines()[0])) else "false"


def build_valid(n):
    """随机在任意位置插入 "abc"，直到长度为 n（n 是 3 的倍数）"""
    t = []
    while len(t) < n:
        p = random.randint(0, len(t))
        t[p:p] = ["a", "b", "c"]
    return "".join(t)


def corrupt(t):
    """随机交换两个不同的相邻字符，大概率变成无效"""
    t = list(t)
    for _ in range(20):
        i = random.randrange(len(t) - 1)
        if t[i] != t[i + 1]:
            t[i], t[i + 1] = t[i + 1], t[i]
            break
    return "".join(t)


def samples():
    res = []
    for t, want in (("aabcbc", True), ("abcabcababcc", True), ("abccba", False)):
        assert brute(t) == want
        res.append((lines(s(t)), "true" if want else "false"))
    return res


def cases():
    res = [
        lines(s("a")),
        lines(s("abc")),
        lines(s("cba")),
        lines(s("aabbcc")),
        lines(s("abcabc")),
        lines(s("ab")),
    ]
    for n in (9, 30, 300):
        v = build_valid(n)
        res.append(lines(s(v)))
        res.append(lines(s(corrupt(v))))
    res.append(lines(s(rand_str(200, "abc"))))
    k = N // 3 - 1
    res.append(lines(s("a" * k + "bc" * k)))
    res.append(lines(s("a" * k + "bc" * (k - 1) + "cb")))
    res.append(lines(s("abc" * (N // 3))))
    v = build_valid(N - 2)
    res.append(lines(s(v)))
    res.append(lines(s(corrupt(v))))
    res.append(lines(s(v[:-1] + "a")))
    return res
