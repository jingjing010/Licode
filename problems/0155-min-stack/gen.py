import json

from genlib import *

LO, HI = -2**31, 2**31 - 1
MAXOPS = 3 * 10**4


def simulate(ops, args):
    st, out = [], []
    for op, a in zip(ops, args):
        if op == "MinStack":
            out.append("null")
        elif op == "push":
            st.append(a[0])
            out.append("null")
        elif op == "pop":
            st.pop()
            out.append("null")
        elif op == "top":
            out.append(str(st[-1]))
        else:
            out.append(str(min(st)))
    return "[" + ",".join(out) + "]"


def case(ops, args):
    assert ops[0] == "MinStack" and len(ops) - 1 <= MAXOPS
    return lines(sarr(ops), json.dumps(args, separators=(",", ":")))


def samples():
    ops = ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"]
    args = [[], [-2], [0], [-3], [], [], [], []]
    want = "[null,null,null,null,-3,null,0,-2]"
    assert simulate(ops, args) == want
    return [(case(ops, args), want)]


def rand_ops(n, lo, hi, p_push=0.45):
    ops, args, size = ["MinStack"], [[]], 0
    for _ in range(n):
        r = random.random()
        if size == 0 or r < p_push:
            ops.append("push")
            args.append([random.randint(lo, hi)])
            size += 1
        elif r < p_push + 0.2:
            ops.append("pop")
            args.append([])
            size -= 1
        elif r < p_push + 0.4:
            ops.append("top")
            args.append([])
        else:
            ops.append("getMin")
            args.append([])
    return ops, args


def pushes_then(vals, tail):
    ops = ["MinStack"] + ["push"] * len(vals)
    args = [[]] + [[v] for v in vals]
    for op in tail:
        ops.append(op)
        args.append([])
    return ops, args


def cases():
    res = [
        case(*pushes_then([LO], ["top", "getMin"])),
        case(*pushes_then([HI], ["getMin", "top", "pop"])),
        case(*pushes_then([0, 1, 0], ["getMin", "pop", "getMin", "pop", "getMin"])),
        case(*pushes_then([5, 5, 5], ["pop", "getMin", "pop", "getMin"])),
        case(*pushes_then([HI, LO, HI], ["getMin", "pop", "pop", "getMin", "top"])),
        case(*pushes_then([3, 2, 1], ["getMin", "pop", "getMin", "pop", "getMin"])),
    ]
    for n, (lo, hi) in ((20, (-10, 10)), (200, (-100, 100)), (2000, (LO, HI))):
        res.append(case(*rand_ops(n, lo, hi)))
    half = MAXOPS // 2
    vals = list(range(half, 0, -1))
    res.append(case(*pushes_then(vals, ["getMin", "pop"] * (half // 2))))
    vals = list(range(1, half + 1))
    res.append(case(*pushes_then(vals, ["getMin", "pop"] * (half // 2))))
    res.append(case(*rand_ops(MAXOPS, LO, HI)))
    res.append(case(*rand_ops(MAXOPS, -5, 5, p_push=0.6)))
    res.append(case(*pushes_then([7] * (MAXOPS - 1), ["getMin"])))
    return res
