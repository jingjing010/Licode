import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403


def ref(inp):
    """Python 对照解：str.find 返回第一次出现的下标，空 needle 返回 0"""
    ls = inp.split("\n")
    return str(json.loads(ls[0]).find(json.loads(ls[1])))


def samples():
    res = [
        (lines(s("AT+CSQ\n+CSQ: 23,0\nOK"), s("OK")), "18"),
        (lines(s("aaab"), s("ab")), "2"),
        (lines(s("+CME ERROR: 10"), s("OK")), "-1"),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def cases():
    res = [
        lines(s(""), s("")),                       # 空 needle 返回 haystack
        lines(s("abc"), s("")),
        lines(s(""), s("a")),
        lines(s("ab"), s("abc")),                  # needle 比 haystack 长
        lines(s("abc"), s("abc")),
        lines(s("abcabd"), s("abd")),              # 部分匹配后失败
        lines(s("xxOKxxOK"), s("OK")),             # 返回第一次出现
        lines(s("\n+IPD,5:hello\n"), s("+IPD,")),
        lines(s("abc"), s("c")),                   # 匹配在最后一个字符
    ]
    h = rand_str(5000, "ab")
    res.append(lines(s(h), s(h[3000:3020])))
    res.append(lines(s(rand_str(10**4, "abc")), s(rand_str(8, "abc"))))
    # 朴素算法的最坏情况之一
    res.append(lines(s("a" * 9999 + "b"), s("a" * 99 + "b")))
    res.append(lines(s("a" * 10**4), s("a" * 5000 + "b")))
    res.append(lines(s("a" * 10**4), s("a" * 10**4)))
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
