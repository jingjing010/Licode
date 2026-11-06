from genlib import *
from genlib import _Node, _to_level

N = 10**4


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
    """按层 BFS 数层数"""
    root = build(parse(inp.split("\n")[0]))
    depth, level = 0, [root] if root else []
    while level:
        depth += 1
        level = [c for x in level for c in (x.left, x.right) if c]
    return str(depth)


def rv(n):
    return rand_arr(n, -100, 100)


def samples():
    res = [
        (lines("[3,9,20,null,null,15,7]"), "3"),
        (lines("[1,null,2]"), "2"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    return [
        lines("[]"),
        lines(tree([0])),
        lines(tree([1, 2])),
        lines(tree([-100, None, 100, 5])),
        lines(tree(list(range(1, 16)))),
        lines(tree(rand_tree(10))),
        lines(tree(rand_tree(100))),
        lines(tree(rand_tree(1000))),
        lines(tree(rand_tree(N))),
        lines(tree(rand_tree(N, 0, 0))),
        lines(tree([random.randint(-100, 100) for _ in range(N)])),
        lines(tree(chain(rv(N), "left"))),
        lines(tree(chain(rv(N), "right"))),
        lines(tree(chain(rv(N), "zig"))),
        lines(tree(broom())),
    ]


def broom():
    """左子树是随机树，右子树是一条很长的链：最深的路径在右边"""
    root = _Node(1)
    root.left = build(rand_tree(N // 2))
    root.right = build(chain(rv(N // 2 - 1), "zig"))
    return _to_level(root)
