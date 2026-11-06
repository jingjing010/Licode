import os

from genlib import *

PID = 9047


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
    logs, cap, out = [], 0, []
    for op, a in zip(ops, args):
        if op == "LogBuffer":
            cap = a[0]
            out.append("null")
        elif op == "write":
            logs.append(a[0])
            logs = logs[-cap:]
            out.append("null")
        elif op == "getAll":
            out.append(arr(logs))
        else:
            out.append(str(len(logs)))
    return "[" + ",".join(out) + "]"


def case(ops, args):
    return lines(sarr(ops), mat(args)), ref(ops, args)


SAMPLES = [
    (["LogBuffer", "write", "write", "getAll", "write", "write", "write", "getAll", "count"],
     [[3], [1], [2], [], [3], [4], [5], [], []],
     "[null,null,null,[1,2],null,null,null,[3,4,5],3]"),
    (["LogBuffer", "getAll", "count", "write", "write", "getAll"],
     [[1], [], [], [7], [9], []],
     "[null,[],0,null,null,[9]]"),
]


def samples():
    res = []
    for ops, args, want in SAMPLES:
        text, got = case(ops, args)
        assert got == want
        res.append((text, want))
    return res


def rand_ops(cap, n, max_get, vmax=10**9):
    ops, args, gets = ["LogBuffer"], [[cap]], 0
    for _ in range(n - 1):
        r = random.random()
        if r < 0.85:
            ops.append("write")
            args.append([random.randint(0, vmax)])
        elif r < 0.92 or gets >= max_get:
            ops.append("count")
            args.append([])
        else:
            ops.append("getAll")
            args.append([])
            gets += 1
    return case(ops, args)


def cases():
    res = [
        case(["LogBuffer", "getAll", "count"], [[5], [], []]),
        # 正好写满、再多写一条
        case(["LogBuffer"] + ["write"] * 6 + ["getAll", "write", "getAll", "count"],
             [[6]] + [[i] for i in range(10, 16)] + [[], [99], [], []]),
        # 容量 1，反复覆盖
        case(["LogBuffer"] + ["write", "getAll"] * 10, [[1]] + [x for i in range(10) for x in ([i], [])]),
        # 写入很多圈后读取
        case(["LogBuffer"] + ["write"] * 1000 + ["getAll", "count"],
             [[7]] + [[i] for i in range(1000)] + [[], []]),
        case(["LogBuffer", "write", "write", "count", "getAll"], [[1000], [0], [10**9], [], []]),
    ]
    for cap in (2, 3, 10, 64):
        res.append(rand_ops(cap, 200, 30))
    res.append(rand_ops(1000, 10**4, 40))
    res.append(rand_ops(999, 10**4, 50))
    res.append(rand_ops(7, 10**4, 1000))
    cross_check(samples() + res)
    return [t for t, _ in res]
