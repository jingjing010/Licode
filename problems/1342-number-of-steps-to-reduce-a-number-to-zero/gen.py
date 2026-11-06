from genlib import *


def ref(n):
    steps = 0
    while n > 0:
        n = n // 2 if n % 2 == 0 else n - 1
        steps += 1
    return steps


def brute(text):
    return str(ref(int(text.split()[0])))


def samples():
    res = [
        (lines(14), "6"),
        (lines(8), "4"),
        (lines(123), "12"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    ns = [
        0,
        1,
        2,
        3,
        10**6,
        999999,
        2**19,           # 只有一个 1：全是除法
        524287,          # 2^19 - 1：全是 1，步数最多的一类
        786431,          # 2^19 + 2^18 - 1
        1000,
    ]
    ns.append(random.randint(4, 1000))
    for _ in range(3):
        ns.append(random.randint(1000, 10**6))
    return [lines(n) for n in ns]


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 1342，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
