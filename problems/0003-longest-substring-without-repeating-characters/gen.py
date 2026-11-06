from genlib import *

PRINTABLE = "".join(chr(c) for c in range(32, 127))


def samples():
    return [
        (lines(s("abcabcbb")), "3"),
        (lines(s("bbbbb")), "1"),
        (lines(s("pwwkew")), "3"),
    ]


def brute(t):
    best = 0
    for i in range(len(t)):
        seen = set()
        for j in range(i, len(t)):
            if t[j] in seen:
                break
            seen.add(t[j])
        best = max(best, len(seen))
    return best


def fast(t):
    last, left, best = {}, 0, 0
    for i, c in enumerate(t):
        if last.get(c, -1) >= left:
            left = last[c] + 1
        last[c] = i
        best = max(best, i - left + 1)
    return best


for _ in range(300):
    _t = rand_str(random.randint(0, 30), "abcde ")
    assert brute(_t) == fast(_t)


def cases():
    N = 5 * 10**4
    res = [
        lines(s("")),
        lines(s(" ")),
        lines(s("au")),
        lines(s("dvdf")),
        lines(s("abba")),
        lines(s("tmmzuxt")),
        lines(s("a b\"c\\d a")),
        lines(s(PRINTABLE)),
    ]
    for n in (20, 200):
        res.append(lines(s(rand_str(n, "abcdefgh"))))
    res.append(lines(s(rand_str(N))))
    res.append(lines(s(rand_str(N, PRINTABLE))))
    res.append(lines(s("a" * N)))
    res.append(lines(s((PRINTABLE * (N // len(PRINTABLE) + 1))[:N])))
    return res
