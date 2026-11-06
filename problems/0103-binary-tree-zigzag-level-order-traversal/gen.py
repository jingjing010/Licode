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
    """先序 DFS（先左后右）按深度收集，同一深度内即从左到右；奇数层再整体反转"""
    root = build(parse(inp.split("\n")[0]))
    levels = []
    st = [(root, 0)] if root else []
    while st:
        nd, d = st.pop()
        if d == len(levels):
            levels.append([])
        levels[d].append(nd.val)
        if nd.right:
            st.append((nd.right, d + 1))
        if nd.left:
            st.append((nd.left, d + 1))
    for d in range(1, len(levels), 2):
        levels[d].reverse()
    return mat(levels)


def samples():
    res = [
        (lines("[3,9,20,null,null,15,7]"), "[[3],[20,9],[15,7]]"),
        (lines("[1]"), "[[1]]"),
        (lines("[]"), "[]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    n = 2000
    return [
        lines(tree([-100, 100])),
        lines(tree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])),
        lines(tree([1, 2, 3, 4, None, None, 5])),
        lines(tree(rand_tree(10))),
        lines(tree(rand_tree(100))),
        lines(tree(rand_tree(n))),
        lines(tree(rand_tree(n))),
        lines(tree(rand_tree(n, -100, -100))),
        lines(tree(chain(rand_arr(n, -100, 100), "left"))),
        lines(tree(chain(rand_arr(n, -100, 100), "right"))),
        lines(tree(chain(rand_arr(n, -100, 100), "zig"))),
        lines(tree(rand_arr(n, -100, 100))),
    ]


if __name__ == "__main__":
    import glob
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    for f in sorted(glob.glob(os.path.join(here, "tests", "*.in"))):
        with open(f, encoding="utf-8") as fi:
            inp = fi.read()
        with open(f[:-3] + ".out", encoding="utf-8") as fo:
            want = fo.read().strip()
        assert brute(inp) == want, os.path.basename(f)
    print("brute check ok")
