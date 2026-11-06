import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403

ASCII = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 +-=,.:;!?#*()[]{}<>/_"


def ref(inp):
    """Python 对照解：复制后的字符串就是 src 本身"""
    return s(json.loads(inp.split("\n")[0]))


def samples():
    res = [
        (lines(s("hello")), '"hello"'),
        (lines(s("")), '""'),
        (lines(s("AT+RST")), '"AT+RST"'),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def cases():
    res = [
        lines(s("a")),
        lines(s("#")),
        lines(s("####")),                 # 和 dst 初始填充一样的字符
        lines(s("say \"hi\" \\ ok")),
        lines(s("固件版本 V1.2.3")),
        lines(s("  leading and trailing  ")),
        lines(s(rand_str(15, ASCII))),
        lines(s(rand_str(256, ASCII))),
        lines(s(rand_str(4095, ASCII))),
        lines(s(rand_str(10**5, ASCII))),
        lines(s("z" * 99999)),
        lines(s(rand_str(30000, "设备名称ABC"))),
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
