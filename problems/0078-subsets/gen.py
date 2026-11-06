from genlib import *
import itertools
import json


def samples():
    return [
        (lines(arr([1, 2, 3])), "[[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]"),
        (lines(arr([0])), "[[],[0]]"),
    ]


def cases():
    res = [
        lines(arr([-10])),
        lines(arr([10, -10])),
        lines(arr([3, 2, 1])),
        lines(arr([5, -3, 0, 8])),
        lines(arr(list(range(1, 11)))),
        lines(arr(list(range(10, 0, -1)))),
        lines(arr([-10, -8, -6, -4, -2, 0, 2, 4, 6, 8])),
    ]
    for n in (2, 4, 6, 8, 9, 10, 10):
        res.append(lines(arr(rand_distinct(n, -10, 10))))
    return res


def brute(text):
    nums = json.loads(text.strip().splitlines()[0])
    out = []
    for k in range(len(nums) + 1):
        for c in itertools.combinations(nums, k):
            out.append(sorted(c))
    return mat(sorted(out))


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 78，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
