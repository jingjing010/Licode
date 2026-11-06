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
    """先序遍历得到值序列，再拼成一条只有右孩子的链"""
    root = build(parse(inp.split("\n")[0]))
    pre, st = [], [root] if root else []
    while st:
        t = st.pop()
        pre.append(t.val)
        st += [c for c in (t.right, t.left) if c]
    return tree(chain(pre, "right"))


def samples():
    return [
        (lines("[1,2,5,3,4,null,6]"), "[1,null,2,null,3,null,4,null,5,null,6]"),
        (lines("[]"), "[]"),
        (lines("[0]"), "[0]"),
    ]


def cases():
    res = [
        lines(tree([1, 2])),
        lines(tree([1, None, 2])),
        lines(tree([1, 2, 3])),
        lines(tree(list(range(1, 32)))),
        lines(tree(rand_arr(2000, -100, 100))),
        lines(tree(chain(rand_arr(2000, -100, 100), "left"))),
        lines(tree(chain(rand_arr(2000, -100, 100), "right"))),
        lines(tree(chain(rand_arr(2000, -100, 100), "zig"))),
    ]
    for n in (5, 20, 100, 500, 2000, 2000):
        res.append(lines(tree(rand_tree(n, -100, 100))))
    return res
