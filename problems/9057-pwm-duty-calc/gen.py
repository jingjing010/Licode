import math
import os
from fractions import Fraction

from genlib import *

PID = 9057


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


def rnd(x):
    """四舍五入（x >= 0），用精确分数避免浮点误差"""
    return math.floor(x + Fraction(1, 2))


def ref(clk, psc, freq, duty):
    n = rnd(Fraction(clk, (psc + 1) * freq))
    return n - 1, rnd(Fraction(n * duty, 100))


def valid(clk, psc, freq, duty):
    if not (1 <= clk <= 5 * 10**8 and 0 <= psc <= 65535 and 1 <= freq <= clk and 0 <= duty <= 100):
        return False
    return 1 <= rnd(Fraction(clk, (psc + 1) * freq)) <= 65536


def case(clk, psc, freq, duty):
    assert valid(clk, psc, freq, duty)
    return lines(clk, psc, freq, duty), arr(ref(clk, psc, freq, duty))


def rand_case():
    while True:
        clk = random.choice([8000000, 16000000, 48000000, 72000000, 84000000, 168000000,
                             random.randint(1, 500000000)])
        psc = random.choice([0, random.randint(0, 100), random.randint(0, 65535)])
        n = random.randint(1, 65536)
        freq = max(1, round(clk / ((psc + 1) * n)))
        duty = random.randint(0, 100)
        if valid(clk, psc, freq, duty):
            return case(clk, psc, freq, duty)


def samples():
    s = [((72000000, 71, 1000, 25), "[999,250]"),
         ((84000000, 0, 30000, 33), "[2799,924]"),
         ((16000000, 15, 3000, 50), "[332,167]")]
    res = []
    for p, want in s:
        text, got = case(*p)
        assert got == want
        res.append((text, want))
    return res


def cases():
    res = [
        case(72000000, 71, 1000, 0),          # 占空比 0
        case(72000000, 71, 1000, 100),        # 占空比 100
        case(72000000, 71, 400, 50),          # N 正好在 2500
        case(1, 0, 1, 50),                    # 最小时钟：N = 1，CCR = round(0.5) = 1
        case(65536, 0, 1, 100),               # N = 65536 上限
        case(500000000, 65535, 1, 77),        # 大预分频
        case(500000000, 0, 7630, 99),         # 中间结果较大
        case(168000000, 167, 70, 1),
        case(3, 0, 2, 50),                    # 1.5 → 2
        case(5, 1, 1, 30),                    # 2.5 → 3，CCR = round(0.9) = 1
    ]
    for _ in range(8):
        res.append(rand_case())
    cross_check(samples() + res)
    return [t for t, _ in res]
