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
    """先序 DFS（先左后右），每层不断覆盖，最后留下的就是最右边的"""
    root = build(parse(inp.split("\n")[0]))
    last = {}

    def go(t, d):
        if t:
            last[d] = t.val
            go(t.left, d + 1)
            go(t.right, d + 1)
    go(root, 0)
    return arr([last[d] for d in range(len(last))])


def samples():
    return [
        (lines("[1,2,3,null,5,null,4]"), "[1,3,4]"),
        (lines("[1,2,3,4,null,null,null,5]"), "[1,3,4,5]"),
        (lines("[1,null,3]"), "[1,3]"),
        (lines("[]"), "[]"),
    ]


def cases():
    res = [
        lines(tree([7])),
        lines(tree([1, 2])),
        lines(tree([1, 2, 3, 4, 5, 6, 7, 8])),
        lines(tree(list(range(1, 101)))),
        lines(tree(chain(rand_arr(100, -100, 100), "left"))),
        lines(tree(chain(rand_arr(100, -100, 100), "zig"))),
    ]
    # 右边很短、左边很深：下面几层只能看到左子树里的结点
    r = _Node(1)
    r.right = _Node(2)
    r.left = build(rand_tree(97, -100, 100))
    res.append(lines(tree(_to_level(r))))
    for n in (5, 12, 30, 60, 100, 100):
        res.append(lines(tree(rand_tree(n, -100, 100))))
    return res
