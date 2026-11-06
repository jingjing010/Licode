import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403


def ref(inp):
    """Python 对照解：用整除计算"""
    ls = inp.split("\n")
    addr, al = int(ls[0]), int(ls[1])
    up = (addr + al - 1) // al * al
    down = addr // al * al
    return "%d\n%d" % (up, down)


def samples():
    res = [
        (lines(13, 8), "16\n8"),
        (lines(16, 8), "16\n16"),
        (lines(0x20000001, 4), "536870916\n536870912"),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def cases():
    res = [
        lines(0, 1),
        lines(0, 4096),
        lines(1, 4096),
        lines(4095, 4096),
        lines(4097, 4096),
        lines(7, 1),
        lines(0x20000000, 4),
        lines(0x0800ABCD, 2048),         # Flash 页对齐
        lines(0xFFFF0000, 4096),         # 上限，已对齐
        lines(0xFFFEFFFF, 4096),         # 向上对齐到上限
        lines(0x7FFFFFFF, 2),            # 超过 int 范围的地址
        lines(0x80000001, 8),
    ]
    for _ in range(5):
        res.append(lines(random.randint(0, 0xFFFF0000), 1 << random.randint(0, 12)))
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
