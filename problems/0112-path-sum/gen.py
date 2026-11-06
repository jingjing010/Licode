from genlib import *
from genlib import _Node, _to_level

N = 5000


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


def leaf_sums(level):
    """所有根到叶子路径的和（列表）"""
    root = build(level)
    res, st = [], ([(root, 0)] if root else [])
    while st:
        t, s0 = st.pop()
        s0 += t.val
        if t.left is None and t.right is None:
            res.append(s0)
        st += [(c, s0) for c in (t.left, t.right) if c]
    return res


def node_sums(level):
    """根到每个结点（含非叶子）的路径和"""
    root = build(level)
    res, st = [], ([(root, 0)] if root else [])
    while st:
        t, s0 = st.pop()
        s0 += t.val
        res.append(s0)
        st += [(c, s0) for c in (t.left, t.right) if c]
    return res


def brute(inp):
    ls = inp.split("\n")
    return b(int(ls[1]) in leaf_sums(parse(ls[0])))


def hit(level):
    """随机挑一条根到叶子路径的和作为 target（落在 [-1000,1000] 内）"""
    c = [x for x in leaf_sums(level) if -1000 <= x <= 1000]
    return random.choice(c) if c else 0


def miss(level):
    """一个不等于任何根到叶子路径和、但等于某个中间结点前缀和的 target（尽量制造陷阱）"""
    ls = set(leaf_sums(level))
    c = [x for x in node_sums(level) if -1000 <= x <= 1000 and x not in ls]
    if c:
        return random.choice(c)
    c = [x for x in range(-1000, 1001) if x not in ls]
    return random.choice(c)


def samples():
    res = [
        (lines("[5,4,8,11,null,13,4,7,2,null,null,null,1]", 22), "true"),
        (lines("[1,2,3]", 5), "false"),
        (lines("[]", 0), "false"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines("[]", 5),
        lines("[1]", 1),
        lines("[1]", 0),
        lines("[1,2]", 1),
        lines("[-2,null,-3]", -5),
        lines("[1,-2,-3,1,3,-2,null,-1]", -1),
        lines("[1000,-1000,null,1000,-1000]", 1000),
    ]
    vals = rand_arr(N, -1, 1)
    lv = chain(vals, "zig")
    res.append(lines(tree(lv), hit(lv)))
    res.append(lines(tree(lv), miss(lv)))
    lv = chain(rand_arr(N, -1, 1), "left")
    res.append(lines(tree(lv), hit(lv)))
    for n in (100, N, N):
        lv = rand_tree(n, -100, 100)
        res.append(lines(tree(lv), hit(lv)))
        res.append(lines(tree(lv), miss(lv)))
    lv = rand_arr(N, -1000, 1000)
    res.append(lines(tree(lv), miss(lv)))
    return res
