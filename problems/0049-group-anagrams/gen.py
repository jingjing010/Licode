from genlib import *


def samples():
    return [
        (lines(sarr(["eat", "tea", "tan", "ate", "nat", "bat"])), '[["ate","eat","tea"],["bat"],["nat","tan"]]'),
        (lines(sarr([""])), '[[""]]'),
        (lines(sarr(["a"])), '[["a"]]'),
    ]


def norm(groups):
    return sorted(sorted(g) for g in groups)


def brute(strs):
    """两两比较字母计数，逐个归入第一个匹配的组"""
    groups = []
    for w in strs:
        cw = sorted(w)
        for g in groups:
            if sorted(g[0]) == cw:
                g.append(w)
                break
        else:
            groups.append([w])
    return norm(groups)


def fast(strs):
    d = {}
    for w in strs:
        d.setdefault("".join(sorted(w)), []).append(w)
    return norm(d.values())


for _ in range(200):
    _a = [rand_str(random.randint(0, 3), "abc") for _ in range(random.randint(1, 10))]
    assert brute(_a) == fast(_a)


def shuffled(w):
    c = list(w)
    random.shuffle(c)
    return "".join(c)


def anagram_case(n, n_base, lo, hi, alphabet="abcdefghijklmnopqrstuvwxyz"):
    bases = [rand_str(random.randint(lo, hi), alphabet) for _ in range(n_base)]
    return [shuffled(random.choice(bases)) for _ in range(n)]


def checked(strs):
    out = sum(len(w) + 3 for w in strs) + 3 * len(fast(strs))
    assert out < 900000, out
    return lines(sarr(strs))


def cases():
    N = 10**4
    res = [
        checked(["", ""]),
        checked(["", "b", ""]),
        checked(["abc", "bca", "cab", "abc"]),
        checked(["ab", "ba", "aab", "aba", "abb"]),
        checked(["a", "b", "c", "d"]),
        checked(["z" * 100, "z" * 99 + "y", "y" + "z" * 99]),
        checked(["ddddddddddg", "dgggggggggg"]),
    ]
    res.append(checked(anagram_case(30, 6, 1, 5, "abcd")))
    res.append(checked(anagram_case(1000, 100, 0, 10)))
    res.append(checked([rand_str(random.randint(0, 3), "ab") for _ in range(500)]))
    res.append(checked(anagram_case(N, 3000, 30, 70)))
    res.append(checked(anagram_case(N, 1, 60, 60)))
    res.append(checked([rand_str(60) for _ in range(N)]))
    res.append(checked(anagram_case(N, 500, 0, 8, "abc")))
    res.append(checked(anagram_case(5000, 2000, 100, 100)))
    return res
