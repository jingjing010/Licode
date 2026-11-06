import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403


def ref(inp):
    """Python 对照解：用取余计算"""
    ls = inp.split("\n")
    addr, al = int(ls[0]), int(ls[1])
    r = addr % al
    return "%s\n%d" % (b(r == 0), 0 if r == 0 else al - r)


def samples():
    res = [
        (lines(12, 4), "true\n0"),
        (lines(13, 4), "false\n3"),
        (lines(0x20000001, 8), "false\n7"),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def cases():
    res = [
        lines(0, 1),
        lines(0, 4096),
        lines(1, 1),
        lines(1, 2),
        lines(1, 4096),
        lines(4095, 4096),
        lines(4096, 4096),
        lines(0xFFFFFFFF, 4096),         # 最大地址
        lines(0xFFFFFFFF, 1),
        lines(0x80000000, 4096),
        lines(0x7FFFFFFD, 4),
        lines(0x08000002, 4),
    ]
    for _ in range(5):
        res.append(lines(random.randint(0, 0xFFFFFFFF), 1 << random.randint(0, 12)))
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
