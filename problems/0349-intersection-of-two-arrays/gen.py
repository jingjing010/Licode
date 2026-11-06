from genlib import *
import json


def brute(text):
    a, c = [json.loads(x) for x in text.strip().splitlines()[:2]]
    return arr(sorted(set(a) & set(c)))


def samples():
    res = [
        (lines(arr([1, 2, 2, 1]), arr([2, 2])), "[2]"),
        (lines(arr([4, 9, 5]), arr([9, 4, 9, 8, 4])), "[4,9]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    full = perm(1001, 0)
    res = [
        lines(arr([0]), arr([0])),
        lines(arr([1000]), arr([0])),                                # 交集为空
        lines(arr([1, 2, 3]), arr([4, 5, 6])),
        lines(arr([7] * 1000), arr([7] * 1000)),                     # 全相同
        lines(arr(full[:1000]), arr(perm(1001, 0)[:1000])),          # 值域几乎全覆盖
        lines(arr(rand_arr(1000, 0, 500)), arr(rand_arr(1000, 501, 1000))),  # 大规模但不相交
        lines(arr([5]), arr(rand_arr(1000, 0, 10) + [5])),
    ]
    for _ in range(2):
        res.append(lines(arr(rand_arr(random.randint(1, 20), 0, 15)), arr(rand_arr(random.randint(1, 20), 0, 15))))
    for _ in range(2):
        res.append(lines(arr(rand_arr(1000, 0, 1000)), arr(rand_arr(1000, 0, 1000))))
    res.append(lines(arr(rand_arr(1000, 0, 50)), arr(rand_arr(1000, 0, 50))))
    return res


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 349，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
