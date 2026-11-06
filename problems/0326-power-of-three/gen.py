from genlib import *

INT_MAX = 2**31 - 1
INT_MIN = -2**31
POWS = {3**k for k in range(20)}


def brute(text):
    return b(int(text.split()[0]) in POWS)


def samples():
    res = [
        (lines(27), "true"),
        (lines(0), "false"),
        (lines(9), "true"),
        (lines(45), "false"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    ns = [
        1,
        3,
        -3,
        -27,
        INT_MIN,
        INT_MAX,
        1162261467,      # 3^19，int 范围内最大的 3 的幂
        1162261466,
        387420489,       # 3^18
        774840978,       # 2 * 3^18
        6,
        2,
        3**random.randint(2, 17),
        3**random.randint(2, 17) + 3,
        random.randint(1, INT_MAX),
    ]
    return [lines(n) for n in ns]


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 326，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
