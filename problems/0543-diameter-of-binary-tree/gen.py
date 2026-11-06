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
    """把树看成无向图，两次 BFS 求最远点对的距离"""
    root = build(parse(inp.split("\n")[0]))
    adj, st = {}, [root]
    while st:
        t = st.pop()
        adj.setdefault(id(t), [])
        for c in (t.left, t.right):
            if c:
                adj[id(t)].append(id(c))
                adj.setdefault(id(c), []).append(id(t))
                st.append(c)

    def bfs(s):
        dist, q = {s: 0}, [s]
        for u in q:
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
        far = max(dist, key=dist.get)
        return far, dist[far]

    a, _ = bfs(id(root))
    _, d = bfs(a)
    return str(d)


def samples():
    return [
        (lines("[1,2,3,4,5]"), "3"),
        (lines("[1,2]"), "1"),
    ]


def cases():
    res = [
        lines(tree([1])),
        lines(tree([1, None, 2])),
        lines(tree(list(range(1, 32)))),
        # 最长路径不经过根：根只有一个孩子，下面是一棵"宽"的子树
        lines(tree([1, 2, None, 3, 4, 5, None, None, 6, 7, None, None, 8, 9, None, None, 10])),
        lines(tree(chain(rand_arr(10**4, -100, 100), "left"))),
        lines(tree(chain(rand_arr(10**4, -100, 100), "zig"))),
        lines(tree(rand_arr(10**4, -100, 100))),
    ]
    # 两条长链挂在根上
    r = _Node(0)
    r.left = build(chain(rand_arr(4000, -100, 100), "left"))
    r.right = build(chain(rand_arr(5999, -100, 100), "right"))
    res.append(lines(tree(_to_level(r))))
    # 根下挂一条短链，链底挂两条长链（直径不经过根）
    r = build(chain([0] * 100, "left"))
    cur = r
    while cur.left:
        cur = cur.left
    cur.left = build(chain([1] * 3000, "left"))
    cur.right = build(chain([2] * 3000, "right"))
    res.append(lines(tree(_to_level(r))))
    for n in (5, 30, 300, 3000, 10**4, 10**4):
        res.append(lines(tree(rand_tree(n, -100, 100))))
    return res
