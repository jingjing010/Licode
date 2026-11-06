from genlib import *
from collections import Counter

UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"
LETTERS = UPPER + LOWER


def samples():
    return [
        (lines(s("ADOBECODEBANC"), s("ABC")), s("BANC")),
        (lines(s("a"), s("a")), s("a")),
        (lines(s("a"), s("aa")), s("")),
    ]


def brute(S, T):
    """枚举所有子串，返回 (最短长度, 最短覆盖子串的起点列表)"""
    need = Counter(T)
    best, starts = None, []
    for i in range(len(S)):
        c = Counter()
        for j in range(i, len(S)):
            c[S[j]] += 1
            if all(c[k] >= v for k, v in need.items()):
                ln = j - i + 1
                if best is None or ln < best:
                    best, starts = ln, [i]
                elif ln == best:
                    starts.append(i)
                break
    return best, starts


def fast(S, T):
    """滑动窗口：每个右端点找到最靠右的合法左端点，返回 (最短长度, 起点列表)"""
    need = Counter(T)
    missing = len(T)
    left, best, starts = 0, None, []
    for r, ch in enumerate(S):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing:
            continue
        while need[S[left]] < 0:
            need[S[left]] += 1
            left += 1
        ln = r - left + 1
        if best is None or ln < best:
            best, starts = ln, [left]
        elif ln == best:
            starts.append(left)
        need[S[left]] += 1
        missing += 1
        left += 1
    return best, starts


for _ in range(400):
    _s = rand_str(random.randint(1, 14), "abcAB")
    _t = rand_str(random.randint(1, 4), "abcA")
    assert brute(_s, _t) == fast(_s, _t)


def unique(S, T):
    best, starts = fast(S, T)
    return best is None or len(starts) == 1


def case(S, T):
    assert 1 <= len(S) <= 10**5 and 1 <= len(T) <= 10**5
    assert all(c in LETTERS for c in S + T)
    assert unique(S, T), (S[:30], T[:30])
    return lines(s(S), s(T))


def shuffled(w):
    c = list(w)
    random.shuffle(c)
    return "".join(c)


def planted(m, t, density):
    """s 主要由 t 中没有的字母组成，随机撒一些 t 的字母，再在随机位置埋一段 t 的排列；直到答案唯一"""
    inside = sorted(set(t))
    outside = [c for c in LETTERS if c not in set(t)]
    while True:
        a = [random.choice(outside) for _ in range(m)]
        for i in range(m):
            if random.random() < density:
                a[i] = random.choice(inside)
        p = random.randint(0, m - len(t))
        a[p:p + len(t)] = shuffled(t)
        S = "".join(a)
        if unique(S, t):
            return S


def random_unique(m, n, alpha_s, alpha_t):
    while True:
        S, T = rand_str(m, alpha_s), rand_str(n, alpha_t)
        if unique(S, T):
            return S, T


def cases():
    M = 10**5
    res = [
        case("a", "b"),
        case("ab", "b"),
        case("ab", "A"),
        case("aa", "aa"),
        case("bba", "ab"),
        case("abc", "cba"),
        case("abc", "abcd"),
        case("cabwefgewcwaefgcf", "cae"),
    ]
    res.append(case(*random_unique(40, 3, "abcAB", "abcA")))
    t = rand_str(8, "abcdeXYZ")
    res.append(case(planted(1000, t, 0.02), t))
    # 最大规模
    t = rand_str(M, LETTERS)
    res.append(case(shuffled(t), t))
    t = rand_str(50, UPPER[:20])
    res.append(case(planted(M, t, 0.05), t))
    t = rand_str(M, LETTERS)
    res.append(case(rand_str(M, LETTERS.replace("Q", "")), t.replace("Q", "q")[:-1] + "Q"))
    t = "Z"
    res.append(case(planted(M, t, 0.0), t))
    t = "a" * 500 + "b" * 500
    res.append(case(planted(M, t, 0.004), t))
    t = rand_str(5000, LOWER[:10])
    res.append(case(planted(M, t, 0.03), t))
    res.append(case("a" * (M - 1), "a" * M))
    return res
