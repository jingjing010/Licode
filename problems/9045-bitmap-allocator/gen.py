import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from genlib import *  # noqa: E402,F403


def simulate(ops, args):
    """Python 参考实现：用 bool 列表模拟位图，返回力扣风格的输出字符串"""
    out = []
    bits = []
    for op, a in zip(ops, args):
        if op == "BitmapAllocator":
            bits = [False] * a[0]
            out.append("null")
        elif op == "alloc":
            c, n, run, res = a[0], len(bits), 0, -1
            for i in range(n):
                run = 0 if bits[i] else run + 1
                if run == c:
                    res = i - c + 1
                    break
            if res >= 0:
                for j in range(res, res + c):
                    bits[j] = True
            out.append(str(res))
        elif op == "release":
            st, c = a
            if st >= 0 and c >= 1 and st + c <= len(bits) and all(bits[st:st + c]):
                for j in range(st, st + c):
                    bits[j] = False
                out.append("true")
            else:
                out.append("false")
        else:
            out.append(str(sum(bits)))
    return "[" + ",".join(out) + "]"


def ref(inp):
    ls = inp.split("\n")
    return simulate(json.loads(ls[0]), json.loads(ls[1]))


def fmt(ops, args):
    return lines(sarr(ops), json.dumps(args, separators=(",", ":")))


def samples():
    res = [
        (fmt(["BitmapAllocator", "alloc", "alloc", "usedCount", "alloc"],
             [[10], [3], [4], [], [4]]),
         "[null,0,3,7,-1]"),
        (fmt(["BitmapAllocator", "alloc", "alloc", "alloc", "release", "alloc", "alloc", "usedCount"],
             [[8], [2], [2], [2], [2, 2], [1], [3], []]),
         "[null,0,2,4,true,2,-1,5]"),
        (fmt(["BitmapAllocator", "alloc", "release", "release", "release", "usedCount"],
             [[40], [33], [0, 33], [0, 1], [30, 20], []]),
         "[null,0,true,false,false,0]"),
    ]
    for i, o in res:
        assert ref(i) == o
    return res


def tracked_case(n, m, max_cnt):
    """边生成边记录已分配的区间，让 release 大多是合法的"""
    ops, args = ["BitmapAllocator"], [[n]]
    bits = [False] * n
    ranges = []
    for _ in range(m - 1):
        r = random.random()
        if r < 0.45:
            c = random.randint(1, max_cnt)
            ops.append("alloc")
            args.append([c])
            run = 0
            for i in range(n):
                run = 0 if bits[i] else run + 1
                if run == c:
                    st = i - c + 1
                    for j in range(st, st + c):
                        bits[j] = True
                    ranges.append((st, c))
                    break
        elif r < 0.85:
            ops.append("release")
            k = random.random()
            if ranges and k < 0.6:
                st, c = ranges.pop(random.randrange(len(ranges)))
                for j in range(st, st + c):
                    bits[j] = False
                args.append([st, c])
            elif ranges and k < 0.75:
                # 只释放某个区间的一部分（合法：这些块都是已分配的）
                idx = random.randrange(len(ranges))
                st, c = ranges[idx]
                if c >= 2:
                    ranges[idx] = (st, c - 1)
                    bits[st + c - 1] = False
                    args.append([st + c - 1, 1])
                else:
                    args.append([st, c + 1])            # 多释放一块，通常非法
                    if st + c + 1 <= n and all(bits[st:st + c + 1]):
                        for j in range(st, st + c + 1):
                            bits[j] = False
                        ranges = [(a, b2) for (a, b2) in ranges if not (st <= a < st + c + 1)]
            else:
                st = random.choice([random.randint(0, n - 1), -1, n, -5000, 5000])
                c = random.choice([1, random.randint(1, max_cnt), 5000])
                args.append([st, c])
                if st >= 0 and st + c <= n and all(bits[st:st + c]):
                    for j in range(st, st + c):
                        bits[j] = False
                    ranges = [(a, b2) for (a, b2) in ranges if not (st <= a < st + c)]
        else:
            ops.append("usedCount")
            args.append([])
    return ops, args


def fill_then_fragment(n):
    """先全部按 1 块分配，再释放所有偶数块，制造碎片"""
    ops, args = ["BitmapAllocator"], [[n]]
    ops += ["alloc"] * (n + 1)
    args += [[1]] * (n + 1)
    for i in range(0, n, 2):
        ops.append("release")
        args.append([i, 1])
    ops += ["usedCount", "alloc", "alloc", "release", "alloc", "usedCount"]
    args += [[], [2], [1], [1, 1], [3], []]
    return ops, args


def cases():
    specs = [
        (["BitmapAllocator", "alloc", "alloc", "usedCount", "release", "usedCount", "alloc"],
         [[1], [1], [1], [], [0, 1], [], [1]]),
        (["BitmapAllocator", "alloc", "alloc", "alloc", "usedCount"],
         [[32], [32], [1], [33], []]),
        (["BitmapAllocator", "alloc", "alloc", "release", "alloc", "alloc", "usedCount"],
         [[64], [31], [2], [0, 31], [32], [31], []]),
        (["BitmapAllocator", "release", "release", "release", "alloc", "release", "release"],
         [[16], [0, 1], [-1, 2], [15, 2], [16], [0, 16], [0, 16]]),
        (["BitmapAllocator", "alloc", "alloc", "alloc", "release", "release", "alloc", "usedCount"],
         [[100], [30], [40], [30], [0, 30], [70, 30], [60], []]),
        fill_then_fragment(64),
        fill_then_fragment(1000),
    ]
    specs.append(tracked_case(10, 60, 4))
    specs.append(tracked_case(100, 300, 20))
    specs.append(tracked_case(1000, 2000, 64))
    specs.append(tracked_case(4096, 5000, 200))
    specs.append(tracked_case(4096, 5000, 5000))
    specs.append(tracked_case(33, 5000, 8))
    return [fmt(o, a) for o, a in specs]


if __name__ == "__main__":
    tdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    k = 0
    while os.path.exists(os.path.join(tdir, "%d.in" % (k + 1))):
        k += 1
        with open(os.path.join(tdir, "%d.in" % k), encoding="utf-8") as f:
            inp = f.read()
        with open(os.path.join(tdir, "%d.out" % k), encoding="utf-8") as f:
            out = f.read()
        assert ref(inp).strip() == out.strip(), "测试点 %d 与 Python 对照解不一致" % k
    print("对照解校验通过：%d 个测试点" % k)
