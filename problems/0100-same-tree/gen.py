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
    """层序表示（去掉末尾 null）是树的唯一编码：两棵树相同 <=> 编码相同"""
    ls = inp.split("\n")
    a, b_ = build(parse(ls[0])), build(parse(ls[1]))
    return b(_to_level(a) == _to_level(b_))


def mutate(level):
    """随机改掉一个非空结点的值"""
    level = list(level)
    idx = [i for i, v in enumerate(level) if v is not None]
    i = random.choice(idx)
    level[i] = level[i] + random.choice([-1, 1])
    return level


def samples():
    res = [
        (lines("[1,2,3]", "[1,2,3]"), "true"),
        (lines("[1,2]", "[1,null,2]"), "false"),
        (lines("[1,2,1]", "[1,1,2]"), "false"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines("[]", "[]"),
        lines("[]", "[0]"),
        lines("[0]", "[]"),
        lines("[5]", "[5]"),
        lines("[5]", "[-5]"),
        lines(tree([10000, -10000]), tree([10000, -10000])),
    ]
    t = rand_tree(100, -10**4, 10**4)
    res.append(lines(tree(t), tree(t)))
    res.append(lines(tree(t), tree(mutate(t))))
    vals = rand_arr(100, -100, 100)
    res.append(lines(tree(chain(vals, "left")), tree(chain(vals, "left"))))
    res.append(lines(tree(chain(vals, "left")), tree(chain(vals, "right"))))
    res.append(lines(tree(chain(vals, "zig")), tree(chain(vals[:-1], "zig"))))
    # 形状相同、值全相同但结构有细微差别
    t = rand_tree(100, 0, 0)
    res.append(lines(tree(t), tree(rand_tree(100, 0, 0))))
    res.append(lines(tree(t), tree(t)))
    full = list(range(1, 101))
    res.append(lines(tree(full), tree(full)))
    res.append(lines(tree(rand_tree(100, -3, 3)), tree(rand_tree(100, -3, 3))))
    return res
