import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403


def ref(inp):
    """Python 对照解：输入文本 -> 预期输出"""
    ls = inp.split("\n")
    src, n = json.loads(ls[0]), int(ls[1])
    return arr(src[:n] + [0] * (len(src) - n))


def samples():
    res = [
        (lines(arr([1, 2, 3, 4, 5]), 3), "[1,2,3,0,0]"),
        (lines(arr([255, 0, 128, 7]), 4), "[255,0,128,7]"),
        (lines(arr([9, 8, 7]), 0), "[0,0,0]"),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def cases():
    res = [
        lines(arr([42]), 1),
        lines(arr([42]), 0),
        lines(arr([255] * 8), 7),
        lines(arr([0, 1, 0, 1, 0]), 5),
    ]
    for n in (7, 31, 64, 1000):
        res.append(lines(arr(rand_arr(n, 1, 255)), random.randint(1, n)))
    for n in (33, 4097):
        res.append(lines(arr(rand_arr(n, 0, 255)), n))
    res.append(lines(arr(rand_arr(10**5, 1, 255)), 10**5))
    res.append(lines(arr(rand_arr(10**5, 1, 255)), 10**5 - 1))
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
