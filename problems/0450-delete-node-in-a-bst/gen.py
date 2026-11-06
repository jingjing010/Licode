from genlib import *
from genlib import _Node, _to_level

LIM = 10**5


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


def bst_level(shape, lo=-LIM, hi=LIM):
    """保持形状不变，按中序依次填入互不相同的升序值 -> BST 层序列表"""
    root = build(shape)
    nodes = inorder(root)
    for nd, v in zip(nodes, sorted(random.sample(range(lo, hi + 1), len(nodes)))):
        nd.val = v
    return _to_level(root)


def brute(inp):
    """合法答案的中序遍历一定是：原树所有值去掉 key 后从小到大排列"""
    ls = inp.split("\n")
    key = int(ls[1])
    return arr(sorted(v for v in parse(ls[0]) if v is not None and v != key))


def vals_of(level):
    return [v for v in level if v is not None]


def case(level, key=None):
    if key is None:
        key = random.choice(vals_of(level))
    return lines(tree(level), key)


def two_child_key(level):
    """挑一个有两个孩子的结点作为 key"""
    root = build(level)
    cand = [nd.val for nd in inorder(root) if nd.left and nd.right]
    return random.choice(cand)


def samples():
    t = "[5,3,6,2,4,null,7]"
    res = [
        (lines(t, 3), "[2,4,5,6,7]"),
        (lines(t, 0), "[2,3,4,5,6,7]"),
        (lines("[]", 0), "[]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    n = 10**4
    t = [5, 3, 6, 2, 4, None, 7]
    res = [
        case([1], 1),
        case([1], 2),
        case([2, 1, 3], 2),
        case(t, 5),
        case(t, 7),
        case([5, 3, 8, None, None, 6, 9, None, 7], 5),       # 后继 6 带右孩子 7
        case([LIM, -LIM], LIM),
        case(bst_level(rand_tree(100))),
        case(bst_level(rand_tree(100)), LIM),
    ]
    lv = bst_level(rand_tree(n))
    res.append(case(lv, two_child_key(lv)))
    lv = bst_level(rand_tree(n))
    res.append(case(lv, lv[0]))                               # 删根
    vals = sorted(random.sample(range(-LIM, LIM + 1), n))
    res.append(case(chain(vals, "right"), vals[n // 2]))
    res.append(case(chain(vals[::-1], "left"), vals[0]))      # 删最深的叶子
    lv = bst_level(chain([0] * n, "zig"))
    res.append(case(lv, lv[0]))
    lv = bst_level(list(range(n)))
    res.append(case(lv, lv[0]))
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
