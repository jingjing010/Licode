from genlib import *
import json


def samples():
    return [
        (lines(arr([2, 3, 6, 7]), 7), "[[2,2,3],[7]]"),
        (lines(arr([2, 3, 5]), 8), "[[2,2,2,2],[2,3,3],[3,5]]"),
        (lines(arr([2]), 1), "[]"),
    ]


def solve(cands, target):
    cands = sorted(cands)
    out = []

    def go(i, remain, path):
        if remain == 0:
            out.append(path[:])
            return
        if i == len(cands) or cands[i] > remain:
            return
        path.append(cands[i])
        go(i, remain - cands[i], path)      # 再选一次 cands[i]
        path.pop()
        go(i + 1, remain, path)             # 不再选 cands[i]

    go(0, target, [])
    return sorted(out)


def ok_case(cands, target):
    assert len(set(cands)) == len(cands) and 1 <= len(cands) <= 30
    assert all(2 <= x <= 40 for x in cands) and 1 <= target <= 40
    assert len(solve(cands, target)) < 150
    return lines(arr(cands), target)


def rand_case(size, target_lo, target_hi, vlo=2, need_nonempty=True):
    for _ in range(100000):
        cands = rand_distinct(size, vlo, 40)
        t = random.randint(target_lo, target_hi)
        k = len(solve(cands, t))
        if k < 150 and (k > 0 or not need_nonempty):
            return ok_case(cands, t)
    raise RuntimeError("找不到满足条件的数据")


def cases():
    res = [
        ok_case([40], 40),
        ok_case([3], 40),
        ok_case([2], 40),
        ok_case([7, 3, 2], 18),
        ok_case([5, 10, 8, 4, 3, 12, 9], 27),
        ok_case(list(range(11, 41)), 40),
        ok_case(list(range(40, 10, -1)), 39),
        ok_case([39, 37, 35], 2),
        ok_case([4, 6, 8, 10], 33),
    ]
    for (size, lo, hi, vlo) in [(3, 10, 20, 2), (5, 20, 30, 2), (8, 25, 40, 3), (12, 30, 40, 6),
                                (20, 35, 40, 9), (25, 38, 40, 10), (30, 1, 40, 2)]:
        res.append(rand_case(size, lo, hi, vlo))
    return res


def brute(text):
    ls = text.strip().splitlines()
    return mat(solve(json.loads(ls[0]), int(ls[1])))


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 39，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
