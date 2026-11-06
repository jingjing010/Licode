from genlib import *
import math

INT_MAX = 2**31 - 1


def brute(text):
    n = int(text.split()[0])
    return b(math.isqrt(n) ** 2 == n)


def samples():
    res = [
        (lines(16), "true"),
        (lines(14), "false"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    k = random.randint(1000, 46340)
    ns = [
        1,
        2,
        4,
        5,
        INT_MAX,
        2147395600,      # 46340^2，最大的完全平方数
        2147395599,
        2147395601,
        808201,          # 899^2
        2147483646,
        k * k,
        k * k + 1,
        k * k - 1,
        random.randint(1, INT_MAX),
    ]
    return [lines(n) for n in ns]


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 367，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
