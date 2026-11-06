import math
import os
from fractions import Fraction

from genlib import *

PID = 9058


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


def rnd_away(fr):
    """四舍五入、.5 远离零"""
    if fr >= 0:
        return math.floor(fr + Fraction(1, 2))
    return -math.floor(-fr + Fraction(1, 2))


def ref(at, tt, x):
    """线性扫描写法（solution.c 用二分），交叉验证"""
    if x <= at[0]:
        return tt[0]
    if x >= at[-1]:
        return tt[-1]
    for i in range(len(at) - 1):
        if at[i] <= x < at[i + 1]:
            return tt[i] + rnd_away(Fraction((tt[i + 1] - tt[i]) * (x - at[i]), at[i + 1] - at[i]))
    raise AssertionError


def case(at, tt, qs):
    assert len(at) == len(tt) >= 1 and all(at[i] < at[i + 1] for i in range(len(at) - 1))
    assert all(0 <= v <= 4095 for v in at + qs) and all(-400 <= v <= 1500 for v in tt)
    return lines(arr(at), arr(tt), arr(qs)), arr([ref(at, tt, x) for x in qs])


def ntc_table(n):
    """模拟 NTC（B=3950，10k 上拉）：ADC 递增、温度递减，步长不均匀"""
    xs = sorted(random.sample(range(1, 4095), n))
    ts, last = [], 10**9
    for x in xs:
        r = 10000.0 * x / (4096 - x)
        t = 1 / (1 / 298.15 + math.log(r / 10000.0) / 3950) - 273.15
        v = max(-400, min(1500, round(t * 10)))
        v = min(v, last)
        ts.append(v)
        last = v
    return xs, ts


def samples():
    res = [
        case([100, 400, 700, 1000], [850, 400, 150, -200], [50, 100, 250, 550, 999, 4000]),
        case([0, 4, 8], [0, 10, 0], [1, 3, 5, 7]),
        case([2000], [253], [0, 2000, 4095]),
    ]
    assert [w for _, w in res] == ["[850,850,625,275,-199,-200]", "[3,8,7,2]", "[253,253,253]"]
    return res


def cases():
    res = [
        case([0, 4095], [-400, 1500], list(range(0, 4096, 37)) + [4095]),
        case([0, 4095], [1500, -400], [0, 1, 2047, 2048, 4094, 4095]),
        case([0, 2, 4, 6], [0, 1, -1, 2], list(range(7))),      # 每段都有 .5
        case([10, 20], [0, 0], [10, 11, 15, 19, 20]),
        case(list(range(0, 4096, 16)), [(i * 7) % 1901 - 400 for i in range(256)], rand_arr(1000, 0, 4095)),
    ]
    for n, q in ((5, 50), (33, 500), (200, 2000)):
        at, tt = ntc_table(n)
        res.append(case(at, tt, rand_arr(q, 0, 4095)))
    at, tt = ntc_table(256)
    res.append(case(at, tt, rand_arr(10**4, 0, 4095)))
    at = sorted(random.sample(range(4096), 256))
    res.append(case(at, rand_arr(256, -400, 1500), rand_arr(10**4, 0, 4095)))
    at = sorted(random.sample(range(4096), 64))
    res.append(case(at, rand_arr(64, -400, 1500), at + [a + 1 for a in at if a < 4095]))
    cross_check(samples() + res)
    return [t for t, _ in res]
