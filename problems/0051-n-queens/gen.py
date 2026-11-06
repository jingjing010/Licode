from genlib import *
import itertools


def samples():
    return [
        (lines(4), '[["..Q.","Q...","...Q",".Q.."],[".Q..","...Q","Q...","..Q."]]'),
        (lines(1), '[["Q"]]'),
    ]


def cases():
    # n 只有 1~9 这 9 种取值，全部覆盖（含无解的 2、3）
    return [lines(n) for n in range(1, 10)]


def brute(text):
    n = int(text.strip().splitlines()[0])
    out = []
    for p in itertools.permutations(range(n)):
        if len({r + p[r] for r in range(n)}) == n and len({r - p[r] for r in range(n)}) == n:
            out.append(["." * c + "Q" + "." * (n - 1 - c) for c in p])
    out.sort()
    return "[" + ",".join(sarr(b) for b in out) + "]"


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 51，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
