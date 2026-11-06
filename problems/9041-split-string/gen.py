import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403


def ref(inp):
    """Python 对照解：split 后去掉空串，取前 maxTokens 个"""
    ls = inp.split("\n")
    text, d, m = json.loads(ls[0]), json.loads(ls[1])[0], int(ls[2])
    return sarr([t for t in text.split(d) if t][:m])


def samples():
    res = [
        (lines(s("SET,LED,1"), s(","), 8), '["SET","LED","1"]'),
        (lines(s("  hello   world "), s(" "), 8), '["hello","world"]'),
        (lines(s("a,b,c,d"), s(","), 2), '["a","b"]'),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def rand_fields(n, delim, alphabet, max_len, max_gap):
    parts = []
    for _ in range(n):
        parts.append(delim * random.randint(0, max_gap))
        parts.append(rand_str(random.randint(1, max_len), alphabet))
    parts.append(delim * random.randint(0, max_gap))
    return "".join(parts)


def cases():
    letters = "abcdefghijklmnopqrstuvwxyz0123456789"
    res = [
        lines(s(""), s(","), 5),                        # 空串
        lines(s(",,,"), s(","), 5),                     # 全是分隔符
        lines(s("abc"), s(","), 5),                     # 没有分隔符
        lines(s(",abc,"), s(","), 5),
        lines(s(",,a,,b,,"), s(","), 1),                # 第 1 个就到上限
        lines(s("a,b"), s(","), 2),                     # 正好等于上限
        lines(s("$GPGGA,123519,4807.038,N,01131.000,E"), s(","), 32),
        lines(s("led on  now"), s(" "), 2),
        lines(s("k1=v1;k2=v2;;k3=v3;"), s(";"), 10),
        lines(s(rand_fields(50, ",", letters, 6, 3)), s(","), 100),
        lines(s(rand_fields(50, ":", letters, 6, 3)), s(":"), 20),
    ]
    big = rand_fields(20000, ",", letters, 3, 2)[:10**5]
    res.append(lines(s(big), s(","), 10**5))
    res.append(lines(s("a," * 50000), s(","), 10**5))        # 5 万个单字符子串
    res.append(lines(s(" " * 10**5), s(" "), 10**5))         # 全是分隔符
    res.append(lines(s(rand_str(10**5, letters)), s(","), 1))  # 一个超长子串
    res.append(lines(s(big), s(","), 777))
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
