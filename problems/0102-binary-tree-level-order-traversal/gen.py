from genlib import *
from genlib import _Node, _to_level


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
    """DFS 记录每个结点的深度，按深度分组（先序遍历保证同层从左到右）"""
    root = build(parse(inp.split("\n")[0]))
    levels = []

    def go(t, d):
        if t is None:
            return
        if d == len(levels):
            levels.append([])
        levels[d].append(t.val)
        go(t.left, d + 1)
        go(t.right, d + 1)
    go(root, 0)
    return mat(levels)


def samples():
    return [
        (lines("[3,9,20,null,null,15,7]"), "[[3],[9,20],[15,7]]"),
        (lines("[1]"), "[[1]]"),
        (lines("[]"), "[]"),
    ]


def cases():
    res = [
        lines(tree([1, 2])),
        lines(tree([1, None, 2])),
        lines(tree([-1000, 1000, -1000, None, 7, 8])),
        lines(tree(list(range(1, 2001)))),
        lines(tree(chain(rand_arr(2000, -1000, 1000), "left"))),
        lines(tree(chain(rand_arr(2000, -1000, 1000), "zig"))),
        lines(tree(rand_arr(2000, -1000, 1000))),
    ]
    for n in (4, 10, 50, 300, 1000, 2000, 2000):
        res.append(lines(tree(rand_tree(n, -1000, 1000))))
    return res
