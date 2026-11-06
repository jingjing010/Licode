import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403


def ref(inp):
    """Python 对照解：写入 c 的低 8 位"""
    ls = inp.split("\n")
    buf = json.loads(ls[0])
    off, c, n = int(ls[1]), int(ls[2]), int(ls[3])
    buf[off:off + n] = [c & 0xFF] * n
    return arr(buf)


def samples():
    res = [
        (lines(arr([1, 2, 3, 4, 5, 6]), 1, 0, 3), "[1,0,0,0,5,6]"),
        (lines(arr([0, 0, 0, 0]), 0, 255, 4), "[255,255,255,255]"),
        (lines(arr([7, 7, 7]), 0, 300, 2), "[44,44,7]"),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def cases():
    res = [
        lines(arr([9]), 0, 0, 1),
        lines(arr([9]), 0, 5, 0),
        lines(arr([1, 2, 3, 4, 5]), 5, 7, 0),
        lines(arr([1, 2, 3, 4, 5]), 2, -1, 3),          # -1 的低 8 位是 0xFF
        lines(arr([0] * 8), 0, 0x1234, 8),               # 只写 0x34
        lines(arr([10, 20, 30, 40]), 3, -1000000, 1),
        lines(arr([255] * 6), 1, 256, 4),                # 256 的低 8 位是 0
    ]
    for length in (17, 100, 999):
        n = random.randint(1, length)
        off = random.randint(0, length - n)
        res.append(lines(arr(rand_arr(length, 0, 255)), off, random.randint(-10**6, 10**6), n))
    N = 10**5
    res.append(lines(arr(rand_arr(N, 0, 255)), 0, 0, N))
    res.append(lines(arr(rand_arr(N, 0, 255)), 1, 0xAB, N - 2))
    res.append(lines(arr(rand_arr(N, 0, 255)), 3, -77, N - 7))
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
