from genlib import *
from genlib import _Node, _to_level

INT_MIN, INT_MAX = -2**31, 2**31 - 1


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


def bst_of_shape(level, vals):
    """保持形状不变，按中序依次填入升序的 vals -> 二叉搜索树"""
    root = build(level)
    for nd, v in zip(inorder(root), sorted(vals)):
        nd.val = v
    return root


def brute(inp):
    """有效 BST <=> 中序遍历严格递增"""
    vals = [t.val for t in inorder(build(parse(inp.split("\n")[0])))]
    return b(all(vals[i] < vals[i + 1] for i in range(len(vals) - 1)))


def samples():
    return [
        (lines("[2,1,3]"), "true"),
        (lines("[5,1,4,null,null,3,6]"), "false"),
    ]


def big_vals(n):
    v = random.sample(range(INT_MIN + 1, INT_MAX), n - 2) + [INT_MIN, INT_MAX]
    return v


def cases():
    res = [
        lines(tree([INT_MAX])),
        lines(tree([INT_MIN, None, INT_MAX])),
        lines(tree([INT_MAX, INT_MAX])),
        lines(tree([INT_MIN, INT_MIN])),
        lines(tree([1, 1])),
        lines(tree([5, 4, 6, None, None, 3, 7])),      # 孙子结点违反
        lines(tree([3, 1, 5, 0, 4])),                    # 左子树里出现比根大的数
        lines(tree([32, 26, 47, 19, None, None, 56, None, 27])),
    ]
    # 合法的大 BST（随机形状 / 链状）
    n = 10**4
    res.append(lines(tree(_to_level(bst_of_shape(rand_tree(n), big_vals(n))))))
    res.append(lines(tree(chain(sorted(big_vals(n)), "right"))))
    res.append(lines(tree(chain(sorted(big_vals(n), reverse=True), "left"))))
    # 合法 BST 上做一点破坏
    r = bst_of_shape(rand_tree(n), big_vals(n))
    nodes = inorder(r)
    i, j = sorted(random.sample(range(n), 2))
    nodes[i].val, nodes[j].val = nodes[j].val, nodes[i].val          # 交换两个值
    res.append(lines(tree(_to_level(r))))
    r = bst_of_shape(rand_tree(n), big_vals(n))
    nodes = inorder(r)
    k = random.randrange(n - 1)
    nodes[k + 1].val = nodes[k].val                                    # 制造一个重复值
    res.append(lines(tree(_to_level(r))))
    r = bst_of_shape(rand_tree(2000), rand_distinct(2000, -10**6, 10**6))
    nodes = inorder(r)
    k = random.randrange(1, 1999)
    nodes[k].val = nodes[k - 1].val - 1                                # 只比前一个小一点
    res.append(lines(tree(_to_level(r))))
    for m in (3, 20, 500):
        res.append(lines(tree(_to_level(bst_of_shape(rand_tree(m), rand_distinct(m, -1000, 1000))))))
    return res
