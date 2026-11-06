from genlib import *
from genlib import _Node, _to_level

N = 10**5


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
    """DFS 走遍所有叶子，取最小深度"""
    root = build(parse(inp.split("\n")[0]))
    if root is None:
        return "0"
    best, st = None, [(root, 1)]
    while st:
        t, d = st.pop()
        if t.left is None and t.right is None:
            best = d if best is None else min(best, d)
        st += [(c, d + 1) for c in (t.left, t.right) if c]
    return str(best)


def small(n):
    return rand_arr(n, 0, 9)


def samples():
    res = [
        (lines("[3,9,20,null,null,15,7]"), "2"),
        (lines("[2,null,3,null,4,null,5,null,6]"), "5"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines("[]"),
        lines("[0]"),
        lines("[1,2]"),
        lines("[1,null,2]"),
        lines("[1,2,3,4,5,null,null,6,7,8,9]"),
        lines(tree(rand_tree(100, -1000, 1000))),
        lines(tree(rand_tree(1000, -1000, 1000))),
        lines(tree(rand_arr(N, -1000, 1000))),
        lines(tree(rand_tree(N, -9, 9))),
        lines(tree(chain(small(N), "left"))),
        lines(tree(chain(small(N), "right"))),
        lines(tree(chain(small(N), "zig"))),
    ]
    # 左边是很长的链、右边是满二叉树：最近的叶子在右边
    root = _Node(1)
    root.left = build(chain(small(N // 2), "left"))
    root.right = build(rand_arr(N // 2 - 1, 0, 9))
    res.append(lines(tree(_to_level(root))))
    # "毛毛虫"：一条长链，每个结点另一侧挂一个只有单孩子的结点，最近叶子在很深处
    root = _Node(0)
    cur, k = root, 1
    while k + 3 <= 30000:
        side = _Node(1)
        side.left = _Node(2)
        nxt = _Node(3)
        cur.left, cur.right = side, nxt
        side.left.right = _Node(4) if k + 3 < 29000 else None
        cur = nxt
        k += 4
    res.append(lines(tree(_to_level(root))))
    return res
