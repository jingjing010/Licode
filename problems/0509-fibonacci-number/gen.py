from genlib import *

F = [0, 1]
while len(F) <= 30:
    F.append(F[-1] + F[-2])
assert F[30] == 832040


def brute(text):
    return str(F[int(text.split()[0])])


def samples():
    res = [
        (lines(2), "1"),
        (lines(3), "2"),
        (lines(4), "3"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    ns = [0, 1, 5, 10, 20, 25, 29, 30, random.randint(6, 19), random.randint(21, 28)]
    return [lines(n) for n in ns]


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 509，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
