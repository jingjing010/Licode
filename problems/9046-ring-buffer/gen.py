from genlib import *


def samples():
    return [
        (lines(sarr(["RingBuffer", "push", "push", "push", "push", "isFull", "pop", "push", "count",
                     "pop", "pop", "pop", "pop"]),
               mat([[3], [17], [34], [51], [68], [], [], [85], [], [], [], [], []])),
         "[null,true,true,true,false,true,17,true,3,34,51,85,-1]"),
        (lines(sarr(["RingBuffer", "pop", "push", "isFull", "count", "pop", "isFull"]),
               mat([[1], [], [255], [], [], [], []])),
         "[null,-1,true,true,1,255,false]"),
    ]


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
    return lines(sarr(ops), mat(args))


def cases():
    res = [
        # 只建不用
        lines(sarr(["RingBuffer", "count", "isFull", "pop"]), mat([[5], [], [], []])),
        # 容量 1 来回读写
        rand_ops(1, 50),
        # 反复绕圈：写满再读空多次
        lines(sarr(["RingBuffer"] + (["push"] * 4 + ["pop"] * 4) * 5),
              mat([[4]] + ([[i] for i in range(4)] + [[]] * 4) * 5)),
    ]
    for cap in (2, 7, 16, 100):
        res.append(rand_ops(cap, 300))
    res.append(rand_ops(10, 2000, 0.7))   # 偏写，经常满
    res.append(rand_ops(10, 2000, 0.3))   # 偏读，经常空
    res.append(rand_ops(1000, 20000, 0.55))
    res.append(rand_ops(37, 20000, 0.5))
    return res
