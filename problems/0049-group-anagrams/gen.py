from genlib import *


def samples():
    return [
        (lines(sarr(["eat", "tea", "tan", "ate", "nat", "bat"])), '[["ate","eat","tea"],["bat"],["nat","tan"]]'),
        (lines(sarr([""])), '[[""]]'),
        (lines(sarr(["a"])), '[["a"]]'),
    ]


def expect(strs):
    """Python 参考答案（与 driver 的规范化方式一致），用来估算输出大小"""
    groups = {}
    for w in strs:
        groups.setdefault("".join(sorted(w)), []).append(w)
    rows = sorted(sorted(g) for g in groups.values())
    return "[" + ",".join(sarr(r) for r in rows) + "]"


def shuffled(w):
    c = list(w)
    random.shuffle(c)
    return "".join(c)


def anagram_family(n, bases):
    return [shuffled(random.choice(bases)) for _ in range(n)]


def cases():
    res = [
        ["", ""],
        ["a", "b", "a"],
        ["abc", "bca", "cab", "xyz", "zyx", "abcd"],
        ["ab", "ba", "abb", "bab", "aab"],
        ["aaa", "aaa", "aaa"],
        list("abcdefghijklmnopqrstuvwxyz"),
        ["", "a", "", "a", "aa"],
        ["z" * 100, shuffled("ab" * 50), "ab" * 50, "a" * 100],
    ]
    res.append([rand_str(random.randint(0, 4), "abc") for _ in range(50)])
    res.append([rand_str(random.randint(0, 6), "abcd") for _ in range(1000)])
    res.append(anagram_family(500, [rand_str(random.randint(1, 10)) for _ in range(30)]))
    # 最大规模（输出上限 1MB，单词长度控制在 80 以内）
    res.append([rand_str(80) for _ in range(10**4)])
    res.append([rand_str(random.randint(0, 80)) for _ in range(10**4)])
    res.append(anagram_family(10**4, [rand_str(random.randint(60, 80)) for _ in range(100)]))
    res.append([rand_str(random.randint(0, 3), "ab") for _ in range(10**4)])
    res.append(anagram_family(10**4, ["abcdefghijklmnopqrstuvwxyz" * 3]))
    for strs in res:
        assert 1 <= len(strs) <= 10**4 and all(len(w) <= 100 for w in strs)
        assert len(expect(strs)) < 1000000
    return [lines(sarr(x)) for x in res]
