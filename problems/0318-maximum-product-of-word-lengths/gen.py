from genlib import *

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def brute(words):
    sets = [set(w) for w in words]
    best = 0
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if not (sets[i] & sets[j]):
                best = max(best, len(words[i]) * len(words[j]))
    return best


def ref_mask(words):
    masks = []
    for w in words:
        m = 0
        for c in w:
            m |= 1 << (ord(c) - 97)
        masks.append(m)
    best = 0
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if masks[i] & masks[j] == 0:
                best = max(best, len(words[i]) * len(words[j]))
    return best


def rand_words(n, maxlen, kmin=1, kmax=6):
    """每个单词只用随机挑出的 kmin~kmax 种字母，保证存在不相交的单词对"""
    res = []
    for _ in range(n):
        alpha = "".join(random.sample(LETTERS, random.randint(kmin, kmax)))
        res.append(rand_str(random.randint(1, maxlen), alpha))
    return res


def samples():
    return [
        (lines(sarr(["abcw", "baz", "foo", "bar", "xtfn", "abcdef"])), "16"),
        (lines(sarr(["a", "ab", "abc", "d", "cd", "bcd", "abcd"])), "4"),
        (lines(sarr(["a", "aa", "aaa", "aaaa"])), "0"),
    ]


def cases():
    tests = [
        ["a", "b"],
        ["a", "a"],
        ["z" * 1000, "y" * 1000],
        ["abcdefghijklm", "nopqrstuvwxyz", "a"],
        [LETTERS, "a", "b", "c"],
        rand_words(10, 8),
        rand_words(100, 30),
        rand_words(500, 200, 2, 10),
    ]
    tests.append(rand_words(1000, 1000, 1, 4))
    tests.append(rand_words(1000, 1000, 5, 13))
    tests.append(["a" + rand_str(random.randint(0, 999)) for _ in range(1000)])
    big = [rand_str(1000, random.choice(["abc", "def", "ghij", "klmno"])) for _ in range(999)]
    big.append(rand_str(1000, "pqrstuvwxyz"))
    tests.append(big)
    tests.append([rand_str(1000, LETTERS[:13]) if i % 2 else rand_str(1000, LETTERS[13:]) for i in range(1000)])
    for _ in range(300):
        w = rand_words(random.randint(2, 12), 6, 1, 5)
        assert brute(w) == ref_mask(w)
    for w in tests:
        assert brute(w) == ref_mask(w)
    return [lines(sarr(w)) for w in tests]
