from genlib import *
from genlib import _Node, _to_level

BIG = 10**9


def parse(line):
    line = line.strip()[1:-1].strip()
    if not line:
        return []
    return [None if t.strip() == "null" else int(t) for t in line.split(",")]


def build(level):
    """层序列表 -> 根结点（与 oj_read_tree 的规则相同）"""
    if not level or level[0] is None:
        return None
    nodes = [None if v is None else _Node(v) for v in level]
    q, h, i = [nodes[0]], 0, 1
    while h < len(q) and i < len(nodes):
        nd = q[h]
        h += 1
        for side in ("left", "right"):
            if i < len(nodes):
                setattr(nd, side, nodes[i])
                if nodes[i] is not None:
                    q.append(nodes[i])
                i += 1
    return nodes[0]


def chain(vals, side):
    """单链形状的树：side 为 left / right / zig（左右交替）"""
    if not vals:
        return []
    root = _Node(vals[0])
    cur = root
    for k, v in enumerate(vals[1:]):
        nd = _Node(v)
        sd = side if side != "zig" else ("left" if k % 2 == 0 else "right")
        setattr(cur, sd, nd)
        cur = nd
    return _to_level(root)


def brute(inp):
    """对每个结点，沿着它到根的祖先链往上累加，数和为 target 的段（O(n·h)，与前缀和哈希无关）"""
    ls = inp.split("\n")
    root, target = build(parse(ls[0])), int(ls[1])
    total, st = 0, ([(root, ())] if root else [])
    while st:
        t, path = st.pop()
        path = path + (t.val,)
        s = 0
        for v in reversed(path):
            s += v
            if s == target:
                total += 1
        st += [(c, path) for c in (t.left, t.right) if c]
    return str(total)


def samples():
    return [
        (lines("[10,5,-3,3,2,null,11,3,-2,null,1]", 8), "3"),
        (lines("[5,4,8,11,null,13,4,7,2,null,null,5,1]", 22), "3"),
    ]


def cases():
    res = [
        lines("[]", 0),
        lines(tree([1]), 1),
        lines(tree([1]), 0),
        lines(tree([1, 2]), 2),
        # int 溢出陷阱：用 int 累加会得到错误答案
        lines(tree([BIG, BIG, None, 294967296, None, BIG, None, BIG, None, BIG]), 0),
        lines(tree([BIG, -BIG, BIG, -BIG]), 0),
        lines(tree(chain([0] * 1000, "left")), 0),             # 答案 1000*1001/2
        lines(tree(chain(rand_arr(1000, -2, 2), "zig")), 1),
        lines(tree([0] * 1000), 0),
        lines(tree(rand_tree(1000, -3, 3)), 2),
        lines(tree(rand_tree(1000, -3, 3)), -1000),
        lines(tree(rand_tree(1000, -BIG, BIG)), 0),
        lines(tree(rand_tree(1000, -1000, 1000)), 1000),
    ]
    vals = [random.choice([BIG, -BIG, 500, -500, 0]) for _ in range(1000)]
    res.append(lines(tree(chain(vals, "right")), 1000))
    vals = [random.choice([BIG, -BIG, 1, -1]) for _ in range(1000)]
    lvl = rand_tree(1000)
    root = build(lvl)
    st, k = [root], 0
    while st:
        t = st.pop()
        t.val = vals[k]
        k += 1
        st += [c for c in (t.left, t.right) if c]
    res.append(lines(tree(_to_level(root)), -1))
    return res
