import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403

ASCII = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 +-=,.:;!?#*()[]{}<>/_\"\\"


def ref(inp):
    """Python 对照解：UTF-8 字节数"""
    return str(len(json.loads(inp.split("\n")[0]).encode("utf-8")))


def samples():
    res = [
        (lines(s("hello")), "5"),
        (lines(s("")), "0"),
        (lines(s("温度:25C")), "10"),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def cases():
    res = [
        lines(s("a")),
        lines(s(" ")),
        lines(s("AT+CSQ")),
        lines(s("OK\nERROR\n")),
        lines(s("\t\"quoted\"\\")),
        lines(s("嵌入式C语言")),
        lines(s(rand_str(37, ASCII))),
        lines(s(rand_str(1000, ASCII))),
        lines(s(rand_str(3000, "中文串口测试abc"))),
        lines(s(rand_str(10**5, ASCII))),
        lines(s("x" * 99999)),
        lines(s(rand_str(33333, "温度湿度"))),            # 99999 字节
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
