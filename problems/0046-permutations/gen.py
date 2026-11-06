from genlib import *
import itertools
import json


def samples():
    return [
        (lines(arr([1, 2, 3])), "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"),
        (lines(arr([0, 1])), "[[0,1],[1,0]]"),
        (lines(arr([1])), "[[1]]"),
    ]


def cases():
    res = [
        lines(arr([-10])),
        lines(arr([5, -5])),
        lines(arr([3, 2, 1])),
        lines(arr([10, -10, 0, 7])),
        lines(arr([1, 2, 3, 4, 5, 6])),
        lines(arr([6, 5, 4, 3, 2, 1])),
        lines(arr([-10, 10, -9, 9, 0, 1])),
    ]
    for n in (2, 3, 4, 5, 6, 6):
        res.append(lines(arr(rand_distinct(n, -10, 10))))
    return res


def brute(text):
    nums = json.loads(text.strip().splitlines()[0])
    return mat(sorted(list(p) for p in itertools.permutations(nums)))


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 46，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
