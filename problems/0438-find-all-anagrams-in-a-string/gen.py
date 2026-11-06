from genlib import *


def samples():
    return [
        (lines(s("cbaebabacd"), s("abc")), "[0,6]"),
        (lines(s("abab"), s("ab")), "[0,1,2]"),
    ]


def brute(t, p):
    sp, m = sorted(p), len(p)
    return [i for i in range(len(t) - m + 1) if sorted(t[i:i + m]) == sp]


def fast(t, p):
    m, res = len(p), []
    if m > len(t):
        return res
    need = [0] * 26
    win = [0] * 26
    for c in p:
        need[ord(c) - 97] += 1
    for i, c in enumerate(t):
        win[ord(c) - 97] += 1
        if i >= m:
            win[ord(t[i - m]) - 97] -= 1
        if i >= m - 1 and win == need:
            res.append(i - m + 1)
    return res


for _ in range(300):
    _t = rand_str(random.randint(1, 25), "abc")
    _p = rand_str(random.randint(1, 5), "abc")
    assert brute(_t, _p) == fast(_t, _p)


def cases():
    N = 3 * 10**4
    res = [
        lines(s("a"), s("a")),
        lines(s("a"), s("b")),
        lines(s("ab"), s("abc")),
        lines(s("aaaaaaaaaa"), s("aa")),
        lines(s("baa"), s("aa")),
        lines(s("abacbabc"), s("abc")),
    ]
    for n in (30, 300):
        res.append(lines(s(rand_str(n, "ab")), s(rand_str(3, "ab"))))
    res.append(lines(s(rand_str(N, "abc")), s(rand_str(5, "abc"))))
    res.append(lines(s(rand_str(N)), s(rand_str(N))))
    res.append(lines(s("a" * N), s("a" * (N // 2))))
    big = rand_str(N, "ab")
    res.append(lines(s(big), s(big[100:100 + N // 3])))
    res.append(lines(s(rand_str(N - 1)), s(rand_str(N))))
    letters = "abcdefghijklmnopqrstuvwxyz"
    res.append(lines(s(letters * (N // 26)), s(letters[::-1])))
    return res
