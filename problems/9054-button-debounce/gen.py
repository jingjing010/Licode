import os

from genlib import *

PID = 9054


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


def ref(s, N):
    """按"游程长度"判断：当前值与稳定状态不同、且它已连续出现 N 次时翻转"""
    ev, stable, run = [], 0, 0
    for i, x in enumerate(s):
        run = run + 1 if i > 0 and s[i - 1] == x else 1
        if x != stable and run == N:
            stable = x
            ev.append([i, x])
    return ev


def bouncy(presses, N, bounce):
    """模拟真实按键：每次按下/松开前有一段抖动，然后稳定保持一段时间"""
    s, level = [], 0
    for _ in range(presses):
        level ^= 1
        for _ in range(random.randint(0, bounce)):
            s.append(random.randint(0, 1))
        s += [level] * random.randint(1, 3 * N)
    return s


def case(s, N):
    return lines(arr(s), N), mat(ref(s, N))


def samples():
    res = [
        case([0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0], 3),
        case([1, 0, 0, 1], 1),
        case([1, 1, 1, 0, 1, 1], 4),
    ]
    assert [w for _, w in res] == ["[[5,1],[11,0]]", "[[0,1],[1,0],[3,1]]", "[]"]
    return res


def cases():
    res = [
        case([0], 1),
        case([1], 1),
        case([0] * 100, 1),
        case([1] * 100, 100),                 # 正好在最后一个采样确认
        case([1] * 99, 100),                  # 差一个
        case([1, 0] * 50, 2),                 # 一直抖动
        case([1] * 5 + [0] * 5 + [1] * 5, 5),
    ]
    for N, bounce in ((5, 3), (20, 5), (100, 10)):
        res.append(case(bouncy(60, N, bounce)[:5 * 10**4], N))
    res.append(case(bouncy(4000, 8, 8)[:5 * 10**4], 8))
    res.append(case([i & 1 for i in range(5 * 10**4)], 1))      # 事件最多
    res.append(case(rand_arr(5 * 10**4, 0, 1), 3))
    res.append(case(bouncy(30, 1000, 30)[:5 * 10**4], 1000))
    cross_check(samples() + res)
    return [t for t, _ in res]
