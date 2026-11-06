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
    """小树：把树当无向图，从每个结点出发 DFS 枚举所有路径（O(n^2)）。
       大树：自底向上 DP（迭代实现）。"""
    root = build(parse(inp.split("\n")[0]))
    nodes, st = [], [root]
    while st:
        t = st.pop()
        nodes.append(t)
        st += [c for c in (t.left, t.right) if c]
    if len(nodes) <= 400:
        adj = {id(t): [] for t in nodes}
        for t in nodes:
            for c in (t.left, t.right):
                if c:
                    adj[id(t)].append(c)
                    adj[id(c)].append(t)
        best = None
        for s in nodes:
            stack = [(s, None, s.val)]
            while stack:
                u, par, total = stack.pop()
                best = total if best is None or total > best else best
                for v in adj[id(u)]:
                    if v is not par:
                        stack.append((v, u, total + v.val))
        return str(best)
    gain, best = {}, None
    for t in reversed(nodes):          # nodes 是先序，反过来孩子先于父亲
        l = max(gain.get(id(t.left), 0), 0) if t.left else 0
        r = max(gain.get(id(t.right), 0), 0) if t.right else 0
        cand = t.val + l + r
        best = cand if best is None or cand > best else best
        gain[id(t)] = t.val + max(l, r)
    return str(best)


def samples():
    return [
        (lines("[1,2,3]"), "6"),
        (lines("[-10,9,20,null,null,15,7]"), "42"),
    ]


def cases():
    n = 3 * 10**4
    res = [
        lines(tree([-3])),
        lines(tree([1000])),
        lines(tree([-1, -2, -3])),
        lines(tree([2, -1])),
        lines(tree([-2, 1])),
        lines(tree([1, -2, 3])),
        lines(tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])),
        lines(tree(rand_tree(300, -1000, -1))),          # 全负数
        lines(tree(rand_tree(300, -10, 10))),
        lines(tree(rand_tree(400, -1000, 1000))),
        lines(tree(rand_tree(n, -1000, 1000))),
        lines(tree(rand_tree(n, -1000, -1))),
        lines(tree(rand_tree(n, 1000, 1000))),           # 全是 1000，答案较大
        lines(tree(chain([1000] * n, "left"))),          # 答案 3*10^7
        lines(tree(chain(rand_arr(n, -1000, 1000), "zig"))),
    ]
    # 最优路径在很深的子树里，不经过根
    r = _Node(-1000)
    r.left = build(rand_tree(10000, -1000, 1000))
    r.right = build(rand_tree(10000, -1000, 1000))
    res.append(lines(tree(_to_level(r))))
    return res
