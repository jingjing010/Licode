from genlib import *
import json


def samples():
    return [
        (lines(s("aab")), '[["a","a","b"],["aa","b"]]'),
        (lines(s("a")), '[["a"]]'),
    ]


def cases():
    res = [lines(s(x)) for x in [
        "z", "ab", "aa", "aba", "abcba", "racecar", "abcdefghijklmnop",
        "a" * 16,                      # 2^15 种分割，最大输出
        "ab" * 8,
        "aabbaabbaabbaabb",
        "abbaabbaabbaabba",
    ]]
    for n in (5, 10, 16):
        res.append(lines(s(rand_str(n, "ab"))))
    res.append(lines(s(rand_str(16, "abc"))))
    res.append(lines(s(rand_str(16))))
    return res


def brute(text):
    t = json.loads(text.strip().splitlines()[0])
    n, out = len(t), []
    # 枚举 n-1 个缝隙切不切
    for mask in range(1 << (n - 1)):
        parts, st = [], 0
        for i in range(n - 1):
            if mask >> i & 1:
                parts.append(t[st:i + 1])
                st = i + 1
        parts.append(t[st:])
        if all(p == p[::-1] for p in parts):
            out.append(parts)
    out.sort()
    return "[" + ",".join(sarr(p) for p in out) + "]"


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 131，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
