import os

from genlib import *

PID = 9053


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


def ref(sig, k):
    n, h = len(sig), k // 2
    out = []
    for i in range(n):
        w = sorted(sig[min(max(j, 0), n - 1)] for j in range(i - h, i + h + 1))
        out.append(w[h])
    return out


def case(sig, k):
    assert k % 2 == 1
    return lines(arr(sig), k), arr(ref(sig, k))


def noisy(n, base=0, noise=20, spike_p=0.05):
    """缓慢变化的信号 + 小噪声 + 偶发尖峰"""
    out, v = [], base
    for _ in range(n):
        v = max(-9000, min(9000, v + random.randint(-5, 5)))
        x = v + random.randint(-noise, noise)
        if random.random() < spike_p:
            x = random.choice([-10000, 10000, random.randint(-10000, 10000)])
        out.append(x)
    return out


def samples():
    res = [case([10, 12, 250, 11, 13], 3), case([1, 100, 2, 3, 200, 4], 5), case([5, -3], 1)]
    assert [w for _, w in res] == ["[10,12,12,13,13]", "[1,2,3,4,4,4]", "[5,-3]"]
    return res


def cases():
    res = [
        case([7], 1),
        case([7], 51),                       # k 远大于 len
        case([3, 1, 2], 51),
        case([0] * 50, 5),
        case(list(range(20)), 9),            # 单调信号
        case([5, 5, 5, -1, 5, 5, 5, 5, 30, 30, 30], 3),
        case([10000, -10000] * 50, 3),
        case([-10000] * 10 + [10000] * 10 + [-10000] * 10, 7),
    ]
    for n, k in ((20, 3), (100, 5), (500, 9)):
        res.append(case(noisy(n), k))
    res.append(case(noisy(10**4, 0, 100, 0.1), 51))
    res.append(case(rand_arr(10**4, -10000, 10000), 49))
    res.append(case(rand_arr(10**4, -3, 3), 51))
    cross_check(samples() + res)
    return [t for t, _ in res]
