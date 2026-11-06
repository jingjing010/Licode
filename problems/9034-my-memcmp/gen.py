import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403


def ref(inp):
    """Python 对照解：Python 的 list 比较本身就是按元素（0~255）的字典序"""
    ls = inp.split("\n")
    a, b, n = json.loads(ls[0]), json.loads(ls[1]), int(ls[2])
    x, y = a[:n], b[:n]
    return str((x > y) - (x < y))


def samples():
    res = [
        (lines(arr([1, 2, 3]), arr([1, 2, 4]), 3), "-1"),
        (lines(arr([1, 2, 3]), arr([1, 2, 4]), 2), "0"),
        (lines(arr([200, 0]), arr([100, 0]), 2), "1"),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def differ_at(n, pos, bigger):
    a = rand_arr(n, 0, 255)
    b = list(a)
    if bigger:
        a[pos], b[pos] = random.randint(129, 255), random.randint(0, 127)
    else:
        a[pos], b[pos] = random.randint(0, 127), random.randint(129, 255)
    return a, b


def cases():
    res = [
        lines(arr([5]), arr([9]), 0),                     # n = 0
        lines(arr([0]), arr([0]), 1),
        lines(arr([128]), arr([127]), 1),                 # 有符号会判反
        lines(arr([0]), arr([255]), 1),
        lines(arr([1, 2, 3, 9]), arr([1, 2, 3]), 3),      # 长度不同，只比较前 n 个
        lines(arr([0, 0, 1]), arr([0, 0, 0]), 3),         # 中间有 0 也要继续比较
        lines(arr([7, 255, 1]), arr([7, 1, 255]), 3),
    ]
    a = rand_arr(1000, 0, 255)
    res.append(lines(arr(a), arr(a), 1000))
    a, b = differ_at(1000, 500, True)
    res.append(lines(arr(a), arr(b), 1000))
    a, b = differ_at(1000, 500, False)
    res.append(lines(arr(a), arr(b), 500))                # 不同的字节在 n 之外
    N = 10**5
    a = rand_arr(N, 0, 255)
    res.append(lines(arr(a), arr(a), N))
    a, b = differ_at(N, N - 1, False)
    res.append(lines(arr(a), arr(b), N))
    a, b = differ_at(N, N - 1, True)
    res.append(lines(arr(a), arr(b), N))
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
