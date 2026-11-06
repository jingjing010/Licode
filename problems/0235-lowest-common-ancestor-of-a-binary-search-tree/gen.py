from genlib import *
from genlib import _Node, _to_level

BIG = 10**9


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


def bst_level(shape, lo=-BIG, hi=BIG):
    """保持形状不变，按中序依次填入互不相同的升序值 -> BST 层序列表"""
    root = build(shape)
    nodes = inorder(root)
    for nd, v in zip(nodes, sorted(random.sample(range(lo, hi + 1), len(nodes)))):
        nd.val = v
    return _to_level(root)


def brute(inp):
    """不利用 BST 性质：记录父亲，把 p 的祖先放进集合，再从 q 往上找第一个在集合里的"""
    ls = inp.split("\n")
    root, pv, qv = build(parse(ls[0])), int(ls[1]), int(ls[2])
    parent, st = {root.val: None}, [root]
    while st:
        t = st.pop()
        for c in (t.left, t.right):
            if c:
                parent[c.val] = t.val
                st.append(c)
    anc, x = set(), pv
    while x is not None:
        anc.add(x)
        x = parent[x]
    x = qv
    while x not in anc:
        x = parent[x]
    return str(x)


def case(level, pv=None, qv=None):
    vals = [v for v in level if v is not None]
    if pv is None:
        pv, qv = random.sample(vals, 2)
    return lines(tree(level), pv, qv)


def samples():
    t = "[6,2,8,0,4,7,9,null,null,3,5]"
    res = [
        (lines(t, 2, 8), "6"),
        (lines(t, 2, 4), "2"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    n = 10**5
    t = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
    res = [
        case([2, 1], 2, 1),
        case([1, None, 2], 1, 2),
        case([0, -BIG, BIG], -BIG, BIG),
        case(t, 3, 5),
        case(t, 5, 0),
        case(t, 9, 7),
        case(bst_level(rand_tree(50))),
        case(bst_level(rand_tree(3000))),
    ]
    vals = sorted(random.sample(range(-10**6, 10**6), n))
    res.append(case(chain(vals, "right"), vals[-1], vals[n // 2]))         # 右链，答案是较浅的那个
    res.append(case(chain(vals[::-1], "left"), vals[0], vals[1]))           # 左链最深的两个
    lv = bst_level(chain([0] * n, "zig"), -10**6, 10**6)
    res.append(case(lv))
    for _ in range(2):
        res.append(case(bst_level(rand_tree(n))))
    lv = bst_level(list(range(n)))                                           # 完全二叉树：两片叶子
    res.append(case(lv, lv[-1], lv[-2]))
    lv = bst_level(list(range(n)))                                           # 最小与最大 -> 根
    vs = sorted(v for v in lv if v is not None)
    res.append(case(lv, vs[0], vs[-1]))
    return res


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
