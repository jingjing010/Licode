import os

from genlib import *

PID = 9055
TRAFFIC = [[1, 3, -1], [2, 3, -1], [0, 3, -1], [-1, -1, 0]]


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


def ref(table, s, events):
    out = []
    for e in events:
        if table[s][e] != -1:
            s = table[s][e]
        out.append(s)
    return out


def rand_table(ns, ne, p_ignore=0.3):
    return [[-1 if random.random() < p_ignore else random.randrange(ns) for _ in range(ne)] for _ in range(ns)]


def case(table, init, events):
    return lines(mat(table), init, arr(events)), arr(ref(table, init, events))


def samples():
    res = [case(TRAFFIC, 0, [0, 0, 0, 0, 1, 0, 2]), case(TRAFFIC, 2, [2, 1, 2])]
    assert [w for _, w in res] == ["[1,2,0,1,3,3,0]", "[2,3,0]"]
    return res


def cases():
    res = [
        case([[-1]], 0, [0, 0, 0]),
        case([[0]], 0, [0]),
        case([[1, -1], [-1, 0]], 1, [0, 0, 1, 1, 0]),
        case(TRAFFIC, 3, [0, 1, 0, 1, 2, 0, 0, 0]),
        case(TRAFFIC, 0, rand_arr(200, 0, 2)),
    ]
    for ns, ne, n in ((3, 2, 50), (10, 5, 1000), (50, 20, 5000)):
        res.append(case(rand_table(ns, ne), random.randrange(ns), rand_arr(n, 0, ne - 1)))
    res.append(case(rand_table(50, 20, 0.1), 0, rand_arr(10**5, 0, 19)))
    res.append(case(rand_table(50, 20, 0.9), 49, rand_arr(10**5, 0, 19)))
    res.append(case(TRAFFIC, 0, [0] * 10**5))
    cross_check(samples() + res)
    return [t for t, _ in res]
