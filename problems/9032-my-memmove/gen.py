import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403


def ref(inp):
    """Python 对照解：先对源数据"拍快照"再贴到目标位置"""
    ls = inp.split("\n")
    buf = json.loads(ls[0])
    d, s, n = int(ls[1]), int(ls[2]), int(ls[3])
    buf[d:d + n] = buf[s:s + n]
    return arr(buf)


def samples():
    res = [
        (lines(arr([1, 2, 3, 4, 5, 6, 7, 8]), 2, 0, 5), "[1,2,1,2,3,4,5,8]"),
        (lines(arr([1, 2, 3, 4, 5, 6, 7, 8]), 0, 3, 5), "[4,5,6,7,8,6,7,8]"),
        (lines(arr([10, 20, 30]), 1, 1, 2), "[10,20,30]"),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def case(length, d, s, n):
    return lines(arr(rand_arr(length, 0, 255)), d, s, n)


def cases():
    res = [
        lines(arr([7]), 0, 0, 1),
        lines(arr([7]), 0, 0, 0),
        lines(arr([1, 2]), 1, 0, 1),
        lines(arr([1, 2]), 0, 1, 1),
        lines(arr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 1, 0, 9),
        lines(arr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 0, 1, 9),
        lines(arr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 6, 0, 4),
        lines(arr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 0, 6, 4),
    ]
    for _ in range(3):
        length = random.randint(20, 200)
        n = random.randint(1, length - 1)
        d, s = random.randint(0, length - n), random.randint(0, length - n)
        res.append(case(length, d, s, n))
    N = 10**5
    res.append(case(N, 3, 0, N - 3))
    res.append(case(N, 0, 5, N - 5))
    res.append(case(N, 50000, 0, 50000))
    return res


if __name__ == "__main__":
    tdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    k = 0
    while os.path.exists(os.path.join(tdir, "%d.in" % (k + 1))):
        k += 1
        with open(os.path.join(tdir, "%d.in" % k), encoding="utf-8") as f:
            inp = f.read()
        with open(os.path.join(tdir, "%d.out" % k), encoding="utf-8") as f:
            out = f.read()
        assert ref(inp).strip() == out.strip(), "测试点 %d 与 Python 对照解不一致" % k
    print("对照解校验通过：%d 个测试点" % k)
