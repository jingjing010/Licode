import os
from collections import deque

from genlib import *

PID = 9046


def cross_check(pairs):
    """用 solution.c 实际跑一遍全部输入，和 Python 对照解逐个比对"""
    import judge
    prob = judge.get_problem(PID)
    wd = judge._workdir()
    try:
        with open(os.path.join(prob["dir"], "solution.c"), encoding="utf-8") as f:
            ok, err, _, _ = judge.compile_code(prob, f.read(), wd)
        assert ok, err
        exe = os.path.join(wd, "main.exe" if os.name == "nt" else "main")
        for k, (text, want) in enumerate(pairs, 1):
            r = judge.run_one(exe, text, 5000)
            assert r["status"] == "OK", (k, r["status"])
            assert judge.normalize(r["stdout"]) == want, "第 %d 个测试与对照解不一致" % k
    finally:
        judge._cleanup(wd)


def ref(ops, args):
    q, cap, out = deque(), 0, []
    for op, a in zip(ops, args):
        if op == "RingBuffer":
            cap = a[0]
            out.append("null")
        elif op == "push":
            if len(q) < cap:
                q.append(a[0])
                out.append("true")
            else:
                out.append("false")
        elif op == "pop":
            out.append(str(q.popleft()) if q else "-1")
        elif op == "count":
            out.append(str(len(q)))
        else:
            out.append(b(len(q) == cap))
    return "[" + ",".join(out) + "]"


def case(ops, args):
    return lines(sarr(ops), mat(args)), ref(ops, args)


SAMPLES = [
    (["RingBuffer", "push", "push", "push", "push", "isFull", "pop", "push", "count", "pop", "pop", "pop", "pop"],
     [[3], [17], [34], [51], [68], [], [], [85], [], [], [], [], []],
     "[null,true,true,true,false,true,17,true,3,34,51,85,-1]"),
    (["RingBuffer", "pop", "push", "isFull", "count", "pop", "isFull"],
     [[1], [], [255], [], [], [], []],
     "[null,-1,true,true,1,255,false]"),
]


def samples():
    res = []
    for ops, args, want in SAMPLES:
        text, got = case(ops, args)
        assert got == want
        res.append((text, want))
    return res


def rand_ops(cap, n, push_ratio=0.5):
    ops, args = ["RingBuffer"], [[cap]]
    for _ in range(n - 1):
        r = random.random()
        if r < push_ratio:
            ops.append("push")
            args.append([random.randint(0, 255)])
        elif r < push_ratio + 0.3:
            ops.append("pop")
            args.append([])
        elif r < push_ratio + 0.4:
            ops.append("count")
            args.append([])
        else:
            ops.append("isFull")
            args.append([])
    return case(ops, args)


def cases():
    res = [
        # 只建不用
        case(["RingBuffer", "count", "isFull", "pop"], [[5], [], [], []]),
        # 容量 1 来回读写
        rand_ops(1, 50),
        # 反复绕圈：写满再读空多次
        case(["RingBuffer"] + (["push"] * 4 + ["pop"] * 4) * 5,
             [[4]] + ([[i] for i in range(4)] + [[]] * 4) * 5),
        # 容量 1000 写满后继续写，再全部读出
        case(["RingBuffer"] + ["push"] * 1005 + ["isFull", "count"] + ["pop"] * 1001,
             [[1000]] + [[i % 256] for i in range(1005)] + [[], []] + [[]] * 1001),
    ]
    for cap in (2, 7, 16, 100):
        res.append(rand_ops(cap, 300))
    res.append(rand_ops(10, 2000, 0.7))   # 偏写，经常满
    res.append(rand_ops(10, 2000, 0.3))   # 偏读，经常空
    res.append(rand_ops(1000, 20000, 0.55))
    res.append(rand_ops(37, 20000, 0.5))
    cross_check(samples() + res)
    return [t for t, _ in res]
