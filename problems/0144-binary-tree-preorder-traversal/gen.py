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
    root = build(parse(inp.split("\n")[0]))
    out = []

    def go(t):
        if t:
            out.append(t.val)
            go(t.left)
            go(t.right)
    go(root)
    return arr(out)


def samples():
    res = [
        (lines("[1,null,2,3]"), "[1,2,3]"),
        (lines("[1,2,3,4,5,null,8,null,null,6,7,9]"), "[1,2,4,5,6,7,3,8,9]"),
        (lines("[]"), "[]"),
        (lines("[1]"), "[1]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines(tree([-100])),
        lines(tree([1, 2])),
        lines(tree([1, None, 2])),
        lines(tree(list(range(1, 101)))),
        lines(tree(chain(rand_arr(100, -100, 100), "left"))),
        lines(tree(chain(rand_arr(100, -100, 100), "right"))),
        lines(tree(chain(rand_arr(100, -100, 100), "zig"))),
        lines(tree([0] * 31)),
    ]
    for n in (3, 7, 15, 40, 80, 100, 100):
        res.append(lines(tree(rand_tree(n, -100, 100))))
    return res
