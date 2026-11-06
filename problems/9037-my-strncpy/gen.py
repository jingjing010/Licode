import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403

ALPHA = "abcdefghijklmnopqrstuvwxyz0123456789 "


def ref(inp):
    """Python 对照解：恰好写 n 个字节，不足补 '\\0'，后面 3 个 '*' 不变"""
    ls = inp.split("\n")
    src, n = json.loads(ls[0]), int(ls[1])
    body = src[:n] + "\0" * max(0, n - len(src))
    return '"' + body.replace("\0", "\\0") + '***"'


def samples():
    res = [
        (lines(s("hi"), 5), '"hi\\0\\0\\0***"'),
        (lines(s("hello"), 3), '"hel***"'),
        (lines(s("abc"), 4), '"abc\\0***"'),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def cases():
    res = [
        lines(s("abc"), 0),              # n = 0：什么都不写
        lines(s(""), 0),
        lines(s(""), 4),                 # 全部补 '\0'
        lines(s("x"), 1),                # 正好写满，不补 '\0'
        lines(s("abc"), 3),              # strlen == n
        lines(s("a b c"), 10),
        lines(s(rand_str(20, ALPHA)), 7),
        lines(s(rand_str(50, ALPHA)), 120),
        lines(s(rand_str(1000, ALPHA)), 999),
        lines(s(rand_str(10**5, ALPHA)), 10**5),
        lines(s(rand_str(10**5, ALPHA)), 50000),
        lines(s(rand_str(10, ALPHA)), 10**5),          # 大量补 '\0'
        lines(s(rand_str(60000, ALPHA)), 90000),
    ]
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
