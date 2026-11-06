from collections import OrderedDict

from genlib import *

KEY = 10**4
VAL = 10**5
OPS = 2 * 10**5
BIG = 15 * 10**4
LINE_MAX = (1 << 21) - 64
OUT_MAX = (1 << 20) - 64


def brute(cap, ops):
    cache, out = OrderedDict(), ["null"]
    for op in ops:
        if op[0] == "get":
            k = op[1]
            if k in cache:
                cache.move_to_end(k)
                out.append(str(cache[k]))
            else:
                out.append("-1")
        else:
            _, k, v = op
            if k in cache:
                cache.move_to_end(k)
            elif len(cache) == cap:
                cache.popitem(last=False)
            cache[k] = v
            out.append("null")
    return "[" + ",".join(out) + "]"


def fmt(cap, ops):
    names = ["LRUCache"] + [op[0] for op in ops]
    params = ["[%d]" % cap] + ["[" + ",".join(str(x) for x in op[1:]) + "]" for op in ops]
    l1, l2 = sarr(names), "[" + ",".join(params) + "]"
    assert len(l1) < LINE_MAX and len(l2) < LINE_MAX, "单行超过 oj_lib 缓冲区"
    assert len(brute(cap, ops)) < OUT_MAX, "输出超过判题 1MB 上限"
    return lines(l1, l2)


def rand_ops(n, key_hi, p_get=0.5, val_hi=VAL):
    ops = []
    for _ in range(n):
        k = random.randint(0, key_hi)
        if random.random() < p_get:
            ops.append(("get", k))
        else:
            ops.append(("put", k, random.randint(0, val_hi)))
    return ops


def samples():
    ops = [("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3), ("get", 2),
           ("put", 4, 4), ("get", 1), ("get", 3), ("get", 4)]
    want = "[null,null,null,1,null,-1,null,-1,3,4]"
    assert brute(2, ops) == want
    return [(fmt(2, ops), want)]


def cases():
    res = [
        fmt(1, [("get", 0), ("put", 0, 0), ("get", 0), ("put", 1, 5), ("get", 0), ("get", 1)]),
        fmt(2, [("put", 2, 1), ("put", 2, 2), ("get", 2), ("put", 1, 1), ("put", 4, 1), ("get", 2)]),
        fmt(2, [("put", 1, 1), ("put", 2, 2), ("put", 1, 10), ("put", 3, 3), ("get", 1), ("get", 2), ("get", 3)]),
        fmt(3, rand_ops(30, 5)),
        fmt(10, rand_ops(300, 20)),
        fmt(1, rand_ops(1000, 3)),
        fmt(50, rand_ops(5000, 100, 0.7)),
        fmt(3000, [("get", k) for k in range(100)]),
        fmt(1, rand_ops(OPS, KEY)),
        fmt(2, rand_ops(OPS, 4, 0.5, 9)),
        fmt(3000, rand_ops(OPS, KEY, 0.6, 99)),
        fmt(3000, rand_ops(BIG, KEY, 0.6)),
        fmt(3000, rand_ops(BIG, 3500, 0.6)),
        fmt(3000, rand_ops(BIG, 2999, 0.5)),
        fmt(1500, [("put", i % (KEY + 1), i % 7) for i in range(OPS // 2)] +
            [("get", i % (KEY + 1)) for i in range(OPS // 2)]),
        fmt(3000, [("put", KEY - i % 3001, VAL) for i in range(BIG // 2)] +
            [("get", KEY - i % 3001) for i in range(BIG // 2)]),
    ]
    return res
