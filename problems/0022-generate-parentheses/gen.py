from genlib import *
import itertools


def samples():
    return [
        (lines(3), sarr(["((()))", "(()())", "(())()", "()(())", "()()()"])),
        (lines(1), sarr(["()"])),
    ]


def cases():
    # n 只有 1~8 这 8 种取值，全部覆盖
    return [lines(n) for n in range(1, 9)]


def valid(t):
    bal = 0
    for ch in t:
        bal += 1 if ch == "(" else -1
        if bal < 0:
            return False
    return bal == 0


def brute(text):
    n = int(text.strip().splitlines()[0])
    return sarr(sorted("".join(p) for p in itertools.product("()", repeat=2 * n) if valid(p)))


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 22，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
