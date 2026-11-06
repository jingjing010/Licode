from genlib import *
import math

INT_MAX = 2**31 - 1


def brute(text):
    return str(math.isqrt(int(text.split()[0])))


def samples():
    res = [
        (lines(4), "2"),
        (lines(8), "2"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    xs = [
        0,
        1,
        2,
        3,
        INT_MAX,            # 46340
        2147395600,         # 46340^2
        2147395599,         # 46340^2 - 1
        2147483646,
        1000000000,
        99980001,           # 9999^2
        random.randint(2, 100),
        random.randint(100, 10**6),
    ]
    for _ in range(3):
        xs.append(random.randint(10**6, INT_MAX))
    k = random.randint(1000, 46340)
    xs.append(k * k)
    return [lines(x) for x in xs]


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 69，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
