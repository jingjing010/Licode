import heapq
import os

from genlib import *

PID = 9060


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


def ref(pr, ar, bu):
    """堆写法（solution.c 用就绪位图 + 每优先级队列），交叉验证"""
    n = len(pr)
    order = sorted(range(n), key=lambda i: (ar[i], i))
    rem = list(bu)
    heap, out, t, k, done = [], [], 0, 0, 0
    while done < n:
        while k < n and ar[order[k]] <= t:
            i = order[k]
            heapq.heappush(heap, (-pr[i], ar[i], i))
            k += 1
        if not heap:
            out.append(-1)
        else:
            _, _, i = heap[0]
            out.append(i)
            rem[i] -= 1
            if rem[i] == 0:
                heapq.heappop(heap)
                done += 1
        t += 1
    return out


def case(pr, ar, bu):
    n = len(pr)
    assert n == len(ar) == len(bu) and 1 <= n <= 500
    assert all(0 <= x <= 31 for x in pr) and all(0 <= x <= 5 * 10**4 for x in ar)
    assert all(1 <= x <= 100 for x in bu)
    out = ref(pr, ar, bu)
    assert len(out) <= max(ar) + sum(bu)
    return lines(arr(pr), arr(ar), arr(bu)), arr(out)


def rand_case(n, max_arrive, max_burst, max_prio=31):
    return case(rand_arr(n, 0, max_prio), rand_arr(n, 0, max_arrive), rand_arr(n, 1, max_burst))


def samples():
    res = [case([1, 3, 2], [0, 1, 2], [3, 2, 1]), case([5, 5], [2, 0], [1, 1]), case([2, 2], [0, 0], [2, 1])]
    assert [w for _, w in res] == ["[0,1,1,2,0,0]", "[1,-1,0]", "[0,0,1]"]
    return res


def cases():
    res = [
        case([0], [0], [1]),
        case([31], [50000], [100]),                         # 前面长时间空闲
        case([1, 2, 3, 4], [0, 1, 2, 3], [4, 3, 2, 1]),     # 逐个被抢占
        case([4, 3, 2, 1], [3, 2, 1, 0], [1, 1, 1, 1]),
        case([1, 1, 1, 1], [3, 2, 1, 0], [2, 2, 2, 2]),     # 同优先级按到达顺序
        case([7, 7, 7], [0, 0, 0], [3, 3, 3]),              # 同优先级同时到达按编号
        case([0, 31, 0], [0, 50, 100], [10, 10, 10]),
        case([3, 2, 1, 0, 4], [0, 0, 0, 0, 2], [2, 2, 2, 2, 2]),
    ]
    for n, ma, mb, mp in ((5, 10, 5, 3), (20, 50, 10, 31), (100, 200, 20, 5), (200, 2000, 50, 31)):
        res.append(rand_case(n, ma, mb, mp))
    res.append(rand_case(500, 50000, 100, 31))
    res.append(rand_case(500, 1000, 100, 2))
    res.append(rand_case(500, 0, 100, 31))
    res.append(case([i % 32 for i in range(500)], [50000 - i for i in range(500)], [100] * 500))
    cross_check(samples() + res)
    return [t for t, _ in res]
