from genlib import *


def ref(n):
    res = []
    for i in range(1, n + 1):
        t = ("Fizz" if i % 3 == 0 else "") + ("Buzz" if i % 5 == 0 else "")
        res.append(t or str(i))
    return res


def brute(text):
    return sarr(ref(int(text.split()[0])))


def samples():
    res = [
        (lines(3), '["1","2","Fizz"]'),
        (lines(5), '["1","2","Fizz","4","Buzz"]'),
        (lines(15), '["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]'),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    ns = [1, 2, 6, 10, 30, 31, 100, 9999, 10000, random.randint(16, 200), random.randint(1000, 10000)]
    return [lines(n) for n in ns]


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 412，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
