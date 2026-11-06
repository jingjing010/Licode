from genlib import *
from genlib import _Node, _to_level

N = 10**4
LO, HI = -2**31, 2**31 - 1


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
    """逐层收集，取最后一层的第一个"""
    root = build(parse(inp.split("\n")[0]))
    level = [root]
    while True:
        nxt = [c for x in level for c in (x.left, x.right) if c]
        if not nxt:
            return str(level[0].val)
        level = nxt


def rv(n):
    return rand_arr(n, LO, HI)


def samples():
    res = [
        (lines("[2,1,3]"), "1"),
        (lines("[1,2,3,4,null,5,6,null,null,7]"), "7"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines(tree([LO])),
        lines(tree([HI])),
        lines("[1,2]"),
        lines("[1,null,2]"),
        lines("[1,2,3,null,null,null,4]"),
        lines("[0,-1,1,null,-2,2,null,null,-3,3]"),
        lines(tree(rv(N))),
        lines(tree(chain(rv(N), "left"))),
        lines(tree(chain(rv(N), "right"))),
        lines(tree(chain(rv(N), "zig"))),
        lines(tree(rand_tree(100, LO, HI))),
        lines(tree(rand_tree(N, LO, HI))),
        lines(tree(rand_tree(N, -5, 5))),
    ]
    # 左边是浅的满二叉树，右边一条长链：答案在右子树最深处
    root = _Node(0)
    root.left = build(rv(1023))
    root.right = build(chain(rv(N - 1024), "zig"))
    res.append(lines(tree(_to_level(root))))
    return res
