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
    """记录每个结点的父亲，把 p 的所有祖先放进集合，再从 q 往上找第一个在集合里的"""
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


def values_of(level):
    return [v for v in level if v is not None]


def relabel(level, lo, hi):
    """保持形状，把值换成 [lo, hi] 内互不相同的随机数"""
    cnt = len(values_of(level))
    it = iter(random.sample(range(lo, hi + 1), cnt))
    return [None if v is None else next(it) for v in level]


def case(level, pv=None, qv=None):
    vals = values_of(level)
    if pv is None:
        pv, qv = random.sample(vals, 2)
    return lines(tree(level), pv, qv)


def samples():
    return [
        (lines("[3,5,1,6,2,0,8,null,null,7,4]", 5, 1), "3"),
        (lines("[3,5,1,6,2,0,8,null,null,7,4]", 5, 4), "5"),
        (lines("[1,2]", 1, 2), "1"),
    ]


def cases():
    BIG = 10**9
    res = [
        case([1, 2], 2, 1),
        case([1, None, 2], 2, 1),
        case([-BIG, BIG, 0], BIG, 0),
        case([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 7, 8),
        case([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 6, 4),
    ]
    lv = relabel(rand_tree(50), -BIG, BIG)
    res.append(case(lv))
    lv = relabel(rand_tree(2000), -BIG, BIG)
    res.append(case(lv))
    n = 10**5
    # 链状：p 是链底，q 在链中间 -> 答案是 q
    vals = random.sample(range(-10**6, 10**6), n)
    res.append(case(chain(vals, "left"), vals[-1], vals[n // 2]))
    res.append(case(chain(vals, "zig"), vals[n // 3], vals[-1]))
    # 根下两条长链，p、q 分别在两条链底 -> 答案是根
    r = _Node(0)
    r.left = build(chain(list(range(1, 50001)), "left"))
    r.right = build(chain(list(range(50001, 99999)), "right"))
    res.append(case(_to_level(r), 50000, 99998))
    for _ in range(3):
        res.append(case(relabel(rand_tree(n), -10**6, 10**6)))
    lv = relabel(list(range(n)), -10**6, 10**6)            # 完全二叉树，取最后两个叶子
    res.append(case(lv, lv[-1], lv[-2]))
    return res
