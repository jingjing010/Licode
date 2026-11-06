import sys

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


def traversals(level):
    root = build(level)
    pre, st = [], [root] if root else []
    while st:
        t = st.pop()
        pre.append(t.val)
        st += [c for c in (t.right, t.left) if c]
    ino, st, cur = [], [], root
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        ino.append(cur.val)
        cur = cur.right
    return pre, ino


sys.setrecursionlimit(20000)


def make(level):
    """由已知的树生成前序/中序；并用朴素重建确认能还原出原树"""
    pre, ino = traversals(level)
    inp = lines(arr(pre), arr(ino))
    assert brute(inp) == tree(level)
    return inp


def brute(inp):
    """朴素 O(n^2) 重建：每次在中序里线性查找根"""
    ls = inp.split("\n")
    pre, ino = parse(ls[0]), parse(ls[1])
    it = iter(pre)

    def rec(lo, hi):
        if lo > hi:
            return None
        nd = _Node(next(it))
        k = ino.index(nd.val, lo, hi + 1)
        nd.left = rec(lo, k - 1)
        nd.right = rec(k + 1, hi)
        return nd
    return tree(_to_level(rec(0, len(ino) - 1)))


def uniq(n):
    return rand_distinct(n, -3000, 3000)


def samples():
    return [
        (lines("[3,9,20,15,7]", "[9,3,15,20,7]"), "[3,9,20,null,null,15,7]"),
        (lines("[-1]", "[-1]"), "[-1]"),
    ]


def shaped(level):
    """给层序形状重新填入互不相同的值"""
    root = build(level)
    nodes, st = [], [root]
    while st:
        t = st.pop()
        nodes.append(t)
        st += [c for c in (t.left, t.right) if c]
    for nd, v in zip(nodes, uniq(len(nodes))):
        nd.val = v
    return _to_level(root)


def cases():
    res = [
        make([1, 2]),
        make([1, None, 2]),
        make([-3000, 3000, 0]),
        make(shaped(list(range(3000)))),
        make(chain(uniq(3000), "left")),
        make(chain(uniq(3000), "right")),
        make(chain(uniq(3000), "zig")),
    ]
    for n in (4, 10, 50, 300, 1000, 3000, 3000):
        res.append(make(shaped(rand_tree(n))))
    return res
