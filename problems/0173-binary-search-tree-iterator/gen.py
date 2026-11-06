from genlib import *
from genlib import _Node, _to_level

MAXCALLS = 10**5


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


def bst_level(shape, lo=0, hi=10**6):
    """保持形状不变，按中序依次填入互不相同的升序值 -> BST 层序列表"""
    root = build(shape)
    nodes = inorder(root)
    for nd, v in zip(nodes, sorted(random.sample(range(lo, hi + 1), len(nodes)))):
        nd.val = v
    return _to_level(root)


def brute(inp):
    """直接把所有值排序，用下标模拟指针"""
    ls = inp.split("\n")
    ops = [x.strip().strip('"') for x in ls[0].strip()[1:-1].split(",")]
    rest = ls[1].strip().lstrip("[ ")
    tree_txt = "[" + rest[:rest.index("]") + 1]
    vals = sorted(v for v in parse(tree_txt) if v is not None)
    out, i = [], 0
    for op in ops:
        if op == "BSTIterator":
            out.append("null")
        elif op == "next":
            out.append(str(vals[i]))
            i += 1
        else:
            out.append("true" if i < len(vals) else "false")
    return "[" + ",".join(out) + "]"


def case(level, ops):
    assert len(ops) <= MAXCALLS
    n = sum(1 for v in level if v is not None)
    assert ops.count("next") <= n
    args = "[[" + tree(level) + "]" + ",[]" * len(ops) + "]"
    return lines(sarr(["BSTIterator"] + ops), args)


def rand_ops(n, calls, p_next=0.5):
    """随机交替 next / hasNext，next 次数不超过 n"""
    ops, used = [], 0
    for _ in range(calls):
        if used < n and random.random() < p_next:
            ops.append("next")
            used += 1
        else:
            ops.append("hasNext")
    return ops


def full_walk(n):
    """hasNext, next 交替直到取完，最后再问一次 hasNext"""
    return ["hasNext", "next"] * n + ["hasNext"]


def samples():
    inp = lines(
        sarr(["BSTIterator", "next", "next", "hasNext", "next", "hasNext", "next", "hasNext", "next", "hasNext"]),
        "[[[7,3,15,null,null,9,20]],[],[],[],[],[],[],[],[],[]]")
    want = "[null,3,7,true,9,true,15,true,20,false]"
    assert brute(inp) == want
    return [(inp, want)]


def cases():
    res = [
        case([0], ["hasNext", "next", "hasNext"]),
        case([10**6], ["next"]),
        case([2, 1], full_walk(2)),
        case([1, None, 2], full_walk(2)),
        case(bst_level(list(range(15))), full_walk(15)),
        case(bst_level(rand_tree(30)), rand_ops(30, 50)),
        case(bst_level(rand_tree(1000)), rand_ops(1000, 1500, 0.7)),
        case(bst_level(rand_tree(1000)), ["hasNext"] * 5 + ["next"] * 10),
    ]
    n = 5 * 10**4
    res.append(case(bst_level(rand_tree(n)), full_walk(n - 1)))
    res.append(case(bst_level(rand_tree(10**5)), rand_ops(10**5, MAXCALLS, 0.3)))
    res.append(case(chain(list(range(n)), "right"), full_walk(n - 1)))
    res.append(case(chain(list(range(10**6, 10**6 - n, -1)), "left"), full_walk(n - 1)))
    res.append(case(bst_level(chain([0] * n, "zig")), full_walk(n - 1)))
    res.append(case(bst_level(list(range(10**5))), ["next"] * MAXCALLS))
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
