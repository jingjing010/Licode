import os
from fractions import Fraction

from genlib import *

PID = 9052


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


def round_half_up(fr):
    return int(fr + Fraction(1, 2)) if fr >= 0 else None


def ref(ops, args):
    out, hist, w = [], [], 0
    for op, a in zip(ops, args):
        if op == "MovingAvg":
            w = a[0]
            hist = []
            out.append("null")
        elif op == "reset":
            hist = []
            out.append("null")
        else:
            hist.append(a[0])
            win = hist[-w:]
            out.append(str(round_half_up(Fraction(sum(win), len(win)))))
    return "[" + ",".join(out) + "]"


def case(ops, args):
    return lines(sarr(ops), mat(args)), ref(ops, args)


def rand_ops(w, n, lo=0, hi=65535, reset_p=0.0):
    ops, args = ["MovingAvg"], [[w]]
    base = random.randint(lo, hi)
    for _ in range(n - 1):
        if random.random() < reset_p:
            ops.append("reset")
            args.append([])
        else:
            base = min(hi, max(lo, base + random.randint(-50, 50)))
            v = min(hi, max(lo, base + random.randint(-300, 300)))
            ops.append("update")
            args.append([v])
    return case(ops, args)


SAMPLES = [
    (["MovingAvg", "update", "update", "update", "update", "update"],
     [[3], [10], [11], [30], [40], [45]], "[null,10,11,17,27,38]"),
    (["MovingAvg", "update", "update", "reset", "update", "update"],
     [[2], [100], [1], [], [7], [8]], "[null,100,51,null,7,8]"),
]


def samples():
    res = []
    for ops, args, want in SAMPLES:
        text, got = case(ops, args)
        assert got == want
        res.append((text, want))
    return res


def cases():
    res = [
        case(["MovingAvg", "update", "update", "update"], [[1], [5], [65535], [0]]),
        case(["MovingAvg", "reset", "update"], [[4], [], [3]]),
        case(["MovingAvg"] + ["update"] * 8, [[2]] + [[1], [2]] * 4),       # 每次都是 x.5
        case(["MovingAvg"] + ["update"] * 2000, [[1000]] + [[65535]] * 2000),  # 最大和
        case(["MovingAvg"] + ["update"] * 30, [[8]] + [[random.choice([0, 65535])] for _ in range(30)]),
    ]
    for w, n, rp in ((2, 50, 0.1), (5, 200, 0.02), (16, 500, 0.0), (64, 2000, 0.005)):
        res.append(rand_ops(w, n, reset_p=rp))
    res.append(rand_ops(1000, 20000, 0, 65535, 0.001))
    res.append(rand_ops(999, 20000))
    res.append(rand_ops(7, 20000, 0, 1000, 0.01))
    cross_check(samples() + res)
    return [t for t, _ in res]
