from genlib import *


def ref(ops, args):
    out, tm = [], {}
    for op, a in zip(ops, args):
        if op == "start":
            tm[a[0]] = [a[1], a[2], a[1]]
        elif op == "stop":
            tm.pop(a[0], None)
        elif op == "tick":
            fired = []
            for i in sorted(tm):
                tm[i][2] -= 1
                if tm[i][2] == 0:
                    fired.append(i)
            for i in fired:
                if tm[i][1]:
                    tm[i][2] = tm[i][0]
                else:
                    del tm[i]
            out.append(arr(fired))
            continue
        out.append("null")
    return "[" + ",".join(out) + "]"


def rand_ops(m, n, max_period=50, p_tick=0.6):
    ops, args = ["TimerManager"], [[m]]
    for _ in range(n - 1):
        r = random.random()
        if r < p_tick:
            ops.append("tick")
            args.append([])
        elif r < p_tick + (1 - p_tick) * 0.8:
            ops.append("start")
            args.append([random.randrange(m), random.randint(1, max_period), random.randint(0, 1)])
        else:
            ops.append("stop")
            args.append([random.randrange(m)])
    out = ref(ops, args)
    assert len(out) < 900000
    return lines(sarr(ops), mat(args))


def samples():
    s = [
        (["TimerManager", "start", "start", "tick", "tick", "tick", "tick", "tick", "tick"],
         [[3], [0, 2, 1], [1, 3, 0], [], [], [], [], [], []],
         "[null,null,null,[],[0],[1],[0],[],[0]]"),
        (["TimerManager", "start", "tick", "start", "tick", "stop", "tick", "start", "start", "tick", "tick", "tick"],
         [[2], [1, 1, 1], [], [0, 1, 0], [], [1], [], [0, 2, 0], [0, 3, 0], [], [], []],
         "[null,null,[1],null,[0,1],null,[],null,null,[],[],[0]]"),
    ]
    for ops, args, want in s:
        assert ref(ops, args) == want
    return [(lines(sarr(ops), mat(args)), want) for ops, args, want in s]


def cases():
    res = [
        lines(sarr(["TimerManager", "tick", "stop", "tick"]), mat([[1], [], [0], []])),
        # 周期 1000 的定时器要 1000 次 tick 才触发
        lines(sarr(["TimerManager", "start"] + ["tick"] * 2001),
              mat([[5], [4, 1000, 1]] + [[]] * 2001)),
        # 单次定时器触发后不再触发；在触发当拍之前 stop
        lines(sarr(["TimerManager", "start", "start", "tick", "stop", "tick", "tick", "tick"]),
              mat([[2], [0, 3, 0], [1, 2, 0], [], [1], [], [], []])),
    ]
    for m, n in ((1, 100), (4, 500), (10, 2000)):
        res.append(rand_ops(m, n))
    res.append(rand_ops(100, 10**4, 1000, 0.7))
    res.append(rand_ops(100, 10**4, 30, 0.5))
    res.append(rand_ops(50, 10**4, 5, 0.3))
    return res
