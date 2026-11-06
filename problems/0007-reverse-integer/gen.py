from genlib import *

INT_MAX = 2**31 - 1
INT_MIN = -2**31


def ref(x):
    sign = -1 if x < 0 else 1
    r = sign * int(str(abs(x))[::-1])
    return r if INT_MIN <= r <= INT_MAX else 0


def brute(text):
    return str(ref(int(text.split()[0])))


def samples():
    res = [
        (lines(123), "321"),
        (lines(-123), "-321"),
        (lines(120), "21"),
        (lines(0), "0"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    xs = [
        INT_MAX,        # 反转后溢出
        INT_MIN,        # 取绝对值就会溢出
        1534236469,     # 经典溢出用例
        -1563847412,    # 负方向溢出
        1463847412,     # 反转后 2147483641，刚好不溢出
        -1463847412,    # 反转后 -2147483641
        1000000003,     # 3000000001 溢出
        1000000000,     # 末尾很多 0
        -1,
        7,
        -2147483412,
    ]
    for _ in range(3):
        xs.append(random.randint(INT_MIN, INT_MAX))
    xs.append(random.randint(-99999, 99999))
    return [lines(x) for x in xs]


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 7，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
