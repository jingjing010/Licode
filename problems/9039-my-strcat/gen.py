import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403

ASCII = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 +-=,.:;!?*()_"


def ref(inp):
    """Python 对照解：直接拼接"""
    ls = inp.split("\n")
    return s(json.loads(ls[0]) + json.loads(ls[1]))


def samples():
    res = [
        (lines(s("Temp="), s("25C")), '"Temp=25C"'),
        (lines(s(""), s("abc")), '"abc"'),
        (lines(s("abc"), s("")), '"abc"'),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def cases():
    res = [
        lines(s(""), s("")),
        lines(s("a"), s("b")),
        lines(s("AT+CWJAP="), s("\"MyWiFi\",\"12345678\"")),
        lines(s("温度"), s("=25℃")),
        lines(s("##"), s("##")),
        lines(s(rand_str(30, ASCII)), s(rand_str(40, ASCII))),
        lines(s(rand_str(1000, ASCII)), s(rand_str(1, ASCII))),
        lines(s(rand_str(1, ASCII)), s(rand_str(1000, ASCII))),
        lines(s(rand_str(10**5, ASCII)), s(rand_str(10**5, ASCII))),
        lines(s(rand_str(10**5, ASCII)), s("")),
        lines(s(""), s(rand_str(10**5, ASCII))),
        lines(s(rand_str(20000, "日志数据abc")), s(rand_str(20000, "串口XYZ"))),
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
