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
    """还原后的树应与原树完全相同：把输入建树后再按 oj_print_tree 的规则输出"""
    return tree(_to_level(build(parse(inp.split("\n")[0]))))


def samples():
    res = [
        (lines("[1,2,3,null,null,4,5]"), "[1,2,3,null,null,4,5]"),
        (lines("[]"), "[]"),
        (lines("[1]"), "[1]"),
        (lines("[1,2]"), "[1,2]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    n = 10**4
    return [
        lines("[1,null,2]"),
        lines("[-1000,1000]"),
        lines("[0,0,0,0,null,null,0]"),
        lines("[5,4,7,3,null,2,null,-1,null,9]"),
        lines(tree(rand_tree(20, -1000, 1000))),
        lines(tree(rand_tree(500, -1000, 1000))),
        lines(tree(rand_tree(n, -1000, 1000))),
        lines(tree(rand_tree(n, -1000, -1000))),
        lines(tree(chain(rand_arr(n, -1000, 1000), "left"))),
        lines(tree(chain(rand_arr(n, -1000, 1000), "right"))),
        lines(tree(chain(rand_arr(n, -1000, 1000), "zig"))),
        lines(tree(rand_arr(n, -1000, 1000))),
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
