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


def mirror_copy(t):
    if t is None:
        return None
    nd = _Node(t.val)
    nd.left = mirror_copy(t.right)
    nd.right = mirror_copy(t.left)
    return nd


def nodes_of(t):
    out, st = [], [t] if t else []
    while st:
        x = st.pop()
        out.append(x)
        st += [c for c in (x.left, x.right) if c]
    return out


def sym_tree(half, lo=-100, hi=100):
    """左子树随机（half 个结点），右子树是它的镜像 -> 对称树"""
    root = _Node(random.randint(lo, hi))
    root.left = build(rand_tree(half, lo, hi))
    root.right = mirror_copy(root.left)
    return root


def brute(inp):
    """对称 <=> 树和它的镜像完全相同（比较层序表示）"""
    root = build(parse(inp.split("\n")[0]))
    return b(_to_level(root) == _to_level(mirror_copy(root)))


def samples():
    return [
        (lines("[1,2,2,3,4,4,3]"), "true"),
        (lines("[1,2,2,null,3,null,3]"), "false"),
    ]


def cases():
    res = [
        lines(tree([1])),
        lines(tree([1, 2])),
        lines(tree([1, 2, 2])),
        lines(tree([1, 2, 3])),
        lines(tree([1, 2, 2, 2, None, 2])),
        lines(tree([5] * 1000)),
    ]
    for half in (3, 50, 499):
        res.append(lines(tree(_to_level(sym_tree(half)))))
    # 对称树改一个值 -> 不对称
    r = sym_tree(499)
    x = random.choice(nodes_of(r.right))
    x.val = x.val + 1 if x.val < 100 else x.val - 1
    res.append(lines(tree(_to_level(r))))
    # 对称树删掉一个叶子 -> 结构不对称
    r = sym_tree(300, 0, 0)
    leaf = [x for x in nodes_of(r.left) if x.left is None and x.right is None][0]
    for x in nodes_of(r.left):
        if x.left is leaf:
            x.left = None
        if x.right is leaf:
            x.right = None
    res.append(lines(tree(_to_level(r))))
    # 左右子树完全相同（不是镜像）
    r = _Node(1)
    r.left = build(rand_tree(200, 0, 3))
    r.right = build(_to_level(r.left))
    res.append(lines(tree(_to_level(r))))
    # 两条对称的长链
    r = _Node(0)
    r.left = build(chain(rand_arr(499, -100, 100), "left"))
    r.right = mirror_copy(r.left)
    res.append(lines(tree(_to_level(r))))
    res.append(lines(tree(rand_tree(1000, -1, 1))))
    return res
