from genlib import *
import math


def ref(n):
    f = str(math.factorial(n))
    return len(f) - len(f.rstrip("0"))


def brute(text):
    return str(ref(int(text.split()[0])))


def samples():
    res = [
        (lines(3), "0"),
        (lines(5), "1"),
        (lines(0), "0"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    ns = [1, 4, 10, 24, 25, 26, 100, 124, 125, 624, 625, 3125, 9999, 10000]
    ns.append(random.randint(1, 100))
    ns.append(random.randint(1000, 10000))
    return [lines(n) for n in ns]


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 172，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
