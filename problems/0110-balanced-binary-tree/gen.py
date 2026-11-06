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


def brute(inp):
    """对每个结点分别求左右子树高度（O(n^2) 的直接定义）"""
    root = build(parse(inp.split("\n")[0]))

    def h(t):
        return 0 if t is None else max(h(t.left), h(t.right)) + 1

    def ok(t):
        if t is None:
            return True
        return abs(h(t.left) - h(t.right)) <= 1 and ok(t.left) and ok(t.right)
    return b(ok(root))


def rv():
    return random.randint(-10**4, 10**4)


def fib_node(h):
    """最"瘦"的平衡树：左子树高 h-1，右子树高 h-2"""
    if h <= 0:
        return None
    nd = _Node(rv())
    nd.left = fib_node(h - 1)
    nd.right = fib_node(h - 2)
    return nd


def deepest_leftmost(nd):
    while nd.left or nd.right:
        nd = nd.left if nd.left else nd.right
    return nd


def avl(n):
    """随机插入 n 个键得到的 AVL 树（一定平衡）"""
    def ht(t):
        return t[3] if t else 0

    def mk(k, l, r):
        return (k, l, r, max(ht(l), ht(r)) + 1)

    def rot_r(t):
        l = t[1]
        return mk(l[0], l[1], mk(t[0], l[2], t[2]))

    def rot_l(t):
        r = t[2]
        return mk(r[0], mk(t[0], t[1], r[1]), r[2])

    def fix(t):
        if ht(t[1]) - ht(t[2]) > 1:
            if ht(t[1][1]) < ht(t[1][2]):
                t = mk(t[0], rot_l(t[1]), t[2])
            return rot_r(t)
        if ht(t[2]) - ht(t[1]) > 1:
            if ht(t[2][2]) < ht(t[2][1]):
                t = mk(t[0], t[1], rot_r(t[2]))
            return rot_l(t)
        return t

    def ins(t, k):
        if t is None:
            return (k, None, None, 1)
        if k < t[0]:
            return fix(mk(t[0], ins(t[1], k), t[2]))
        return fix(mk(t[0], t[1], ins(t[2], k)))

    t = None
    for k in random.sample(range(-10**4, 10**4 + 1), n):
        t = ins(t, k)

    def conv(t):
        if t is None:
            return None
        nd = _Node(t[0])
        nd.left, nd.right = conv(t[1]), conv(t[2])
        return nd
    return conv(t)


def samples():
    res = [
        (lines("[3,9,20,null,null,15,7]"), "true"),
        (lines("[1,2,2,3,3,null,null,4,4]"), "false"),
        (lines("[]"), "true"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines("[1]"),
        lines("[1,2]"),
        lines("[1,2,null,3]"),
        # 根的左右高度相等，但内部结点不平衡
        lines("[1,2,2,3,null,null,3,4,null,null,4]"),
        lines(tree(list(range(1, N + 1)))),
        lines(tree(chain(rand_arr(N, -10**4, 10**4), "zig"))),
        lines(tree(rand_tree(N, -10**4, 10**4))),
        lines(tree(_to_level(avl(N)))),
        lines(tree(_to_level(avl(1000)))),
        lines(tree(_to_level(fib_node(17)))),
    ]
    root = fib_node(17)
    deepest_leftmost(root).left = _Node(7)          # 根的左子树变高 1 -> 不平衡
    res.append(lines(tree(_to_level(root))))
    root = fib_node(16)
    leaf = deepest_leftmost(root.right)             # 右子树里加一个结点：仍平衡
    leaf.left = _Node(7)
    res.append(lines(tree(_to_level(root))))
    # 左边是平衡树，右边是同样高的链：根平衡，但链上的结点不平衡
    root = _Node(0)
    root.left = fib_node(12)
    root.right = build(chain(rand_arr(12, -10, 10), "right"))
    res.append(lines(tree(_to_level(root))))
    return res
