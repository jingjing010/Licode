from genlib import *
from genlib import _Node, _to_level

N = 1000


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
    """带着「是不是左孩子」的标记遍历所有结点"""
    root = build(parse(inp.split("\n")[0]))
    total, st = 0, [(root, False)]
    while st:
        t, is_left = st.pop()
        if t.left is None and t.right is None and is_left:
            total += t.val
        if t.left:
            st.append((t.left, True))
        if t.right:
            st.append((t.right, False))
    return str(total)


def samples():
    res = [
        (lines("[3,9,20,null,null,15,7]"), "24"),
        (lines("[1]"), "0"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines("[-1000]"),
        lines("[1,2]"),
        lines("[1,null,2]"),
        lines("[1,2,3,4,5]"),
        lines("[0,null,1,2]"),
        lines(tree(chain(rand_arr(N, -1000, 1000), "left"))),
        lines(tree(chain(rand_arr(N, -1000, 1000), "right"))),
        lines(tree(chain(rand_arr(N, -1000, 1000), "zig"))),
        lines(tree(rand_arr(N, -1000, 1000))),
        lines(tree([1000] * N)),
        lines(tree([-1000] * N)),
    ]
    for n in (10, 100, N, N, N):
        res.append(lines(tree(rand_tree(n, -1000, 1000))))
    return res
