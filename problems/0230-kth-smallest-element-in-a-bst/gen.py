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


def inorder(root):
    out, st, cur = [], [], root
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        out.append(cur)
        cur = cur.right
    return out


def bst_of_shape(level, vals):
    """保持形状不变，按中序依次填入升序的 vals -> 二叉搜索树"""
    root = build(level)
    for nd, v in zip(inorder(root), sorted(vals)):
        nd.val = v
    return root


def brute(inp):
    """所有值排序后取第 k 个"""
    ls = inp.split("\n")
    vals = [v for v in parse(ls[0]) if v is not None]
    return str(sorted(vals)[int(ls[1]) - 1])


def samples():
    return [
        (lines("[3,1,4,null,2]", 1), "1"),
        (lines("[5,3,6,2,4,null,null,1]", 3), "3"),
    ]


def rand_case(n, shape=None, k=None):
    vals = rand_distinct(n, 0, 10**4)
    level = shape if shape is not None else rand_tree(n)
    root = bst_of_shape(level, vals)
    return lines(tree(_to_level(root)), k if k is not None else random.randint(1, n))


def cases():
    n = 10**4
    res = [
        lines(tree([0]), 1),
        lines(tree([1, 0]), 2),
        lines(tree([1, None, 10000]), 1),
        rand_case(7, k=7),
        rand_case(50),
        rand_case(1000),
        rand_case(n, k=1),
        rand_case(n, k=n),
        rand_case(n),
        lines(tree(chain(list(range(n)), "right")), n),
        lines(tree(chain(list(range(n, 0, -1)), "left")), 1),
        lines(tree(chain(list(range(n, 0, -1)), "left")), n),
        rand_case(n, shape=chain([0] * n, "zig"), k=n // 2),
        rand_case(n, shape=list(range(n))),
    ]
    return res
