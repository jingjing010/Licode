import bisect
import json

from genlib import *

V = 10**5
MAXOPS = 5 * 10**4


def simulate(ops, args):
    a, out = [], []
    for op, x in zip(ops, args):
        if op == "MedianFinder":
            out.append("null")
        elif op == "addNum":
            bisect.insort(a, x[0])
            out.append("null")
        else:
            k = len(a)
            m = a[k // 2] if k % 2 else (a[k // 2 - 1] + a[k // 2]) / 2
            out.append("%.5f" % m)
    return "[" + ",".join(out) + "]"


def case(ops, args):
    assert ops[0] == "MedianFinder" and len(ops) - 1 <= MAXOPS
    return lines(sarr(ops), json.dumps(args, separators=(",", ":")))


def samples():
    ops = ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
    args = [[], [1], [2], [], [3], []]
    want = "[null,null,null,1.50000,null,2.00000]"
    assert simulate(ops, args) == want
    return [(case(ops, args), want)]


def stream(vals, query_every=1):
    """依次 addNum(vals[i])，每加 query_every 个数查询一次"""
    ops, args = ["MedianFinder"], [[]]
    for i, v in enumerate(vals, 1):
        ops.append("addNum")
        args.append([v])
        if i % query_every == 0:
            ops.append("findMedian")
            args.append([])
    if ops[-1] != "findMedian":
        ops.append("findMedian")
        args.append([])
    return ops, args


def cases():
    half = MAXOPS // 2
    res = [
        case(*stream([5])),
        case(*stream([-V, V])),
        case(*stream([-1, 1])),
        case(*stream([-3, -2])),
        case(*stream([2, 2, 2, 2, 2])),
        case(*stream([6, 10, 2, 6, 5, 0, 6, 3, 1, 0, 0])),
        case(*stream([V, V, -V, -V, V])),
    ]
    for n, lo, hi in ((20, -10, 10), (200, -100, 100), (2000, -V, V)):
        res.append(case(*stream(rand_arr(n, lo, hi))))
    res.append(case(*stream(rand_arr(half, -V, V))))
    res.append(case(*stream(list(range(-half // 2, half // 2)))))
    res.append(case(*stream(list(range(V, V - half, -1)))))
    res.append(case(*stream(rand_arr(MAXOPS - 1, -V, V), query_every=MAXOPS)))
    res.append(case(*stream(rand_arr(half, -3, 3))))
    zig = [(-V + i) if i % 2 else (V - i) for i in range(half)]
    res.append(case(*stream(zig)))
    return res
