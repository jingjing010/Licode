from genlib import *
import json

EX = ["ABCE", "SFCS", "ADEE"]


def samples():
    return [
        (lines(cmat(EX), s("ABCCED")), "true"),
        (lines(cmat(EX), s("SEE")), "true"),
        (lines(cmat(EX), s("ABCB")), "false"),
    ]


def rand_board(m, n, alpha):
    return ["".join(random.choice(alpha) for _ in range(n)) for _ in range(m)]


def path_word(g, length):
    """在网格上随机走一条不重复的路径，返回路径上的单词（一定存在）"""
    m, n = len(g), len(g[0])
    while True:
        r, c = random.randrange(m), random.randrange(n)
        seen = {(r, c)}
        w = [g[r][c]]
        while len(w) < length:
            nb = [(a, b2) for a, b2 in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
                  if 0 <= a < m and 0 <= b2 < n and (a, b2) not in seen]
            if not nb:
                break
            r, c = random.choice(nb)
            seen.add((r, c))
            w.append(g[r][c])
        if len(w) == length:
            return "".join(w)


def cases():
    allA = ["AAAAAA"] * 6
    res = [
        lines(cmat(["a"]), s("a")),
        lines(cmat(["a"]), s("b")),
        lines(cmat(["a"]), s("aa")),
        lines(cmat(["ab", "cd"]), s("abdc")),
        lines(cmat(["ab", "cd"]), s("abcd")),
        lines(cmat(["aA"]), s("aA")),
        lines(cmat(["aA"]), s("AA")),
        lines(cmat(allA), s("A" * 15)),
        lines(cmat(allA), s("A" * 14 + "B")),
        lines(cmat(["BAAAAA"] + ["AAAAAA"] * 5), s("A" * 14 + "B")),
        lines(cmat(["BBAAAA"] + ["AAAAAA"] * 5), s("B" + "A" * 13 + "B")),
        lines(cmat(EX), s("ABCESEEEFS")),
        lines(cmat(EX), s("ABCESCFSADEE")),
    ]
    for (m, n, alpha, ln) in [(3, 4, "ab", 5), (6, 6, "AB", 10), (6, 6, "abc", 15), (5, 6, "aAbB", 8)]:
        g = rand_board(m, n, alpha)
        res.append(lines(cmat(g), s(path_word(g, ln))))
        res.append(lines(cmat(g), s("".join(random.choice(alpha) for _ in range(ln)))))
    return res


def brute(text):
    ls = text.strip().splitlines()
    g = [list(r) for r in json.loads(ls[0])]
    w = json.loads(ls[1])
    m, n = len(g), len(g[0])
    from collections import Counter
    cb, cw = Counter(c for r in g for c in r), Counter(w)
    if any(cw[c] > cb[c] for c in cw):
        return "false"
    if cb[w[0]] > cb[w[-1]]:
        w = w[::-1]

    def go(r, c, k, used):
        if g[r][c] != w[k]:
            return False
        if k == len(w) - 1:
            return True
        used.add((r, c))
        for a, b2 in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= a < m and 0 <= b2 < n and (a, b2) not in used and go(a, b2, k + 1, used):
                return True
        used.discard((r, c))
        return False

    return b(any(go(i, j, 0, set()) for i in range(m) for j in range(n)))


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 79，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
