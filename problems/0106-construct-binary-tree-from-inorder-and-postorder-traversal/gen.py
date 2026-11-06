import sys

from genlib import *
from genlib import _Node, _to_level

sys.setrecursionlimit(20000)


def parse_arr(line):
    line = line.strip()[1:-1].strip()
    return [int(t) for t in line.split(",")] if line else []


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


def relabel(level, lo=-3000, hi=3000):
    cnt = sum(1 for v in level if v is not None)
    it = iter(random.sample(range(lo, hi + 1), cnt))
    return [None if v is None else next(it) for v in level]


def orders(level):
    """返回 (中序, 后序)"""
    root = build(level)
    ino, st, cur = [], [], root
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        ino.append(cur.val)
        cur = cur.right
    post, st = [], [root] if root else []
    while st:                      # 根 -> 右 -> 左 的逆序即 左 -> 右 -> 根
        nd = st.pop()
        post.append(nd.val)
        if nd.left:
            st.append(nd.left)
        if nd.right:
            st.append(nd.right)
    post.reverse()
    return ino, post


def case(level):
    ino, post = orders(level)
    return lines(arr(ino), arr(post))


def brute(inp):
    """朴素分治：每次在中序数组里线性查找根的位置，O(n^2)"""
    ls = inp.split("\n")
    ino, post = parse_arr(ls[0]), parse_arr(ls[1])

    def rec(il, ir, pl, pr):
        if il > ir:
            return None
        nd = _Node(post[pr])
        k = ino.index(post[pr], il, ir + 1)
        left = k - il
        nd.left = rec(il, k - 1, pl, pl + left - 1)
        nd.right = rec(k + 1, ir, pl + left, pr - 1)
        return nd

    return tree(_to_level(rec(0, len(ino) - 1, 0, len(post) - 1)))


def samples():
    res = [
        (lines("[9,3,15,20,7]", "[9,15,7,20,3]"), "[3,9,20,null,null,15,7]"),
        (lines("[-1]", "[-1]"), "[-1]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    n = 3000
    return [
        case([3000]),
        case([1, 2]),
        case([1, None, 2]),
        case(relabel(list(range(15)))),
        case(relabel(rand_tree(10))),
        case(relabel(rand_tree(200))),
        case(relabel(rand_tree(n))),
        case(relabel(rand_tree(n))),
        case(relabel(chain([0] * n, "left"))),
        case(relabel(chain([0] * n, "right"))),
        case(relabel(chain([0] * n, "zig"))),
        case(relabel(list(range(n)))),
        case(chain(list(range(-1500, 1500)), "right")),
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
