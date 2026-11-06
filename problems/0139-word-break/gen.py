from genlib import *
from functools import lru_cache


def brute(t, words):
    ws = set(words)

    @lru_cache(None)
    def ok(i):
        if i == len(t):
            return True
        return any(t[i:j] in ws and ok(j) for j in range(i + 1, min(len(t), i + 20) + 1))

    return ok(0)


def rand_dict(m, lo, hi, alphabet):
    ws = set()
    while len(ws) < m:
        ws.add(rand_str(random.randint(lo, hi), alphabet))
    return sorted(ws, key=lambda _: random.random())


def concat(words, maxlen):
    t = ""
    while True:
        w = random.choice(words)
        if len(t) + len(w) > maxlen:
            break
        t += w
    return t or words[0]


def case(t, words):
    assert 1 <= len(t) <= 300 and 1 <= len(words) <= 1000
    assert len(set(words)) == len(words) and all(1 <= len(w) <= 20 for w in words)
    return lines(s(t), sarr(words))


def samples():
    return [
        (case("leetcode", ["leet", "code"]), "true"),
        (case("applepenapple", ["apple", "pen"]), "true"),
        (case("catsandog", ["cats", "dog", "sand", "and", "cat"]), "false"),
    ]


def fast(t, words):
    dp = [True] + [False] * len(t)
    for i in range(1, len(t) + 1):
        dp[i] = any(len(w) <= i and dp[i - len(w)] and t[i - len(w):i] == w for w in words)
    return dp[-1]


def cases():
    for _ in range(300):
        words = rand_dict(random.randint(1, 5), 1, 3, "ab")
        t = rand_str(random.randint(1, 12), "ab")
        assert brute(t, words) == fast(t, words)
    res = [
        case("a", ["a"]),
        case("a", ["b"]),
        case("aaaaaaa", ["aaaa", "aaa"]),
        case("aaaaaaa", ["aaaa", "aa"]),
        case("cars", ["car", "ca", "rs"]),
        case("a" * 299 + "b", ["a" * k for k in range(1, 11)]),
        case("a" * 300, ["a" * k for k in range(1, 21)]),
        case("ab" * 150, ["a", "b", "ab", "ba"]),
    ]
    # 小规模随机，与暴力交叉验证
    for _ in range(3):
        words = rand_dict(5, 1, 3, "ab")
        t = concat(words, 30)
        if random.random() < 0.5:
            t += "c"
        res.append(case(t, words))
    # 大规模：能拆分 / 末尾多一个字符不能拆分
    words = rand_dict(1000, 1, 20, "abcde")
    t = concat(words, 300)
    res.append(case(t, words))
    words = rand_dict(1000, 1, 20, "ab")
    t = concat(words, 299)
    res.append(case(t + "c", words))
    words = rand_dict(50, 1, 5, "ab")
    res.append(case(concat(words, 300), words))
    res.append(case(rand_str(300, "ab"), rand_dict(30, 1, 6, "ab")))
    return res
