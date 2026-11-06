from genlib import *
import json


def samples():
    return [
        (lines(sarr(["MemoryPool", "alloc", "alloc", "alloc", "freeCount"]),
               "[[16,2],[],[],[],[]]"),
         "[null,0,1,-1,0]"),
        (lines(sarr(["MemoryPool", "alloc", "alloc", "release", "alloc", "freeCount"]),
               "[[8,3],[],[],[0],[],[]]"),
         "[null,0,1,true,0,1]"),
        (lines(sarr(["MemoryPool", "alloc", "release", "release", "release", "freeCount"]),
               "[[4,2],[],[0],[0],[5],[]]"),
         "[null,0,true,false,false,2]"),
    ]


def simulate(ops, args):
    """Python 参考实现：返回力扣风格的输出字符串"""
    out = []
    for op, a in zip(ops, args):
        if op == "MemoryPool":
            n = a[1]
            stack = list(range(n - 1, -1, -1))   # 栈顶 = 列表末尾 = 链表头
            used = [False] * n
            out.append("null")
        elif op == "alloc":
            if stack:
                i = stack.pop()
                used[i] = True
                out.append(str(i))
            else:
                out.append("-1")
        elif op == "release":
            i = a[0]
            if 0 <= i < n and used[i]:
                used[i] = False
                stack.append(i)
                out.append("true")
            else:
                out.append("false")
        else:
            out.append(str(len(stack)))
    return "[" + ",".join(out) + "]"


def fmt(ops, args):
    return lines(sarr(ops), json.dumps(args, separators=(",", ":")))


def tracked_case(block_size, n, m):
    """边生成边模拟，让 release 大多是合法的"""
    ops, args = ["MemoryPool"], [[block_size, n]]
    stack = list(range(n - 1, -1, -1))
    used = []
    for _ in range(m - 1):
        r = random.random()
        if r < 0.45:
            ops.append("alloc")
            args.append([])
            if stack:
                used.append(stack.pop())
        elif r < 0.85:
            ops.append("release")
            if used and random.random() < 0.8:
                i = used.pop(random.randrange(len(used)))
                stack.append(i)
                args.append([i])
            else:
                args.append([random.choice([random.randint(0, n - 1), -1, n, 2000, -1000])])
                i = args[-1][0]
                if i in used:
                    used.remove(i)
                    stack.append(i)
        else:
            ops.append("freeCount")
            args.append([])
    return ops, args


def drain_refill(n):
    ops, args = ["MemoryPool"], [[4, n]]
    ops += ["alloc"] * (n + 1)
    args += [[]] * (n + 1)
    order = list(range(n))
    random.shuffle(order)
    for i in order:
        ops.append("release")
        args.append([i])
    ops.append("freeCount")
    args.append([])
    ops += ["alloc"] * (n + 1)
    args += [[]] * (n + 1)
    ops.append("freeCount")
    args.append([])
    return ops, args


def cases():
    specs = [
        (["MemoryPool", "alloc", "alloc", "release", "release", "alloc", "freeCount"],
         [[4, 1], [], [], [0], [0], [], []]),
        (["MemoryPool", "freeCount", "release", "release"], [[64, 1000], [], [0], [999]]),
        (["MemoryPool", "alloc", "alloc", "alloc", "release", "release", "release", "alloc", "alloc", "alloc"],
         [[8, 3], [], [], [], [1], [2], [0], [], [], []]),
        drain_refill(5),
        drain_refill(1000),
    ]
    specs.append(tracked_case(4, 1, 50))
    specs.append(tracked_case(16, 5, 200))
    specs.append(tracked_case(32, 50, 2000))
    specs.append(tracked_case(64, 1000, 10**4))
    specs.append(tracked_case(4, 10, 10**4))
    specs.append(tracked_case(8, 300, 10**4))
    return [fmt(o, a) for o, a in specs]
