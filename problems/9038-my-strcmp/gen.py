import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403

ASCII = "abcdefghijklmnopqrstuvwxyz0123456789 +-=_"


def ref(inp):
    """Python 对照解：bytes 比较就是按 unsigned char 的字典序"""
    ls = inp.split("\n")
    a = json.loads(ls[0]).encode("utf-8")
    b = json.loads(ls[1]).encode("utf-8")
    return str((a > b) - (a < b))


def samples():
    res = [
        (lines(s("apple"), s("apply")), "-1"),
        (lines(s("led on"), s("led on")), "0"),
        (lines(s("abcd"), s("abc")), "1"),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def cases():
    res = [
        lines(s(""), s("")),
        lines(s(""), s("a")),
        lines(s("a"), s("")),
        lines(s("A"), s("a")),                 # 大写字母更小
        lines(s("abc"), s("abcd")),
        lines(s("中"), s("a")),                 # 中文首字节 >= 128，有符号比较会判反
        lines(s("温度"), s("湿度")),
        lines(s("reboot"), s("reset")),
        lines(s("get temp"), s("get time")),
    ]
    base = rand_str(1000, ASCII)
    res.append(lines(s(base), s(base)))
    t = list(base)
    t[777] = "~"                                 # '~' 比字母表里所有字符都大
    res.append(lines(s(base), s("".join(t))))
    N = 10**5
    base = rand_str(N, ASCII)
    res.append(lines(s(base), s(base)))
    res.append(lines(s(base), s(base[:-1])))
    res.append(lines(s(base[:-1] + "!"), s(base)))   # '!' 比所有字母表字符都小
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
