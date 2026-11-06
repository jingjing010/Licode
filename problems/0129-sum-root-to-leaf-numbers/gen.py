from genlib import *
from genlib import _Node, _to_level

INT_MAX = 2**31 - 1


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


def paths_sum(root):
    """显式栈枚举每条根到叶路径，把路径上的数字串当成十进制数相加"""
    total, st = 0, [(root, str(root.val))]
    while st:
        nd, sdig = st.pop()
        if not nd.left and not nd.right:
            total += int(sdig)
        for c in (nd.left, nd.right):
            if c:
                st.append((c, sdig + str(c.val)))
    return total


def brute(inp):
    return str(paths_sum(build(parse(inp.split("\n")[0]))))


def rand_shape(n, max_depth=10):
    """随机形状、深度不超过 max_depth 的二叉树，返回 (根, 按深度分组的结点)"""
    root = _Node(0)
    by_depth = [[root]]
    free = [(root, 1)]                     # 还有空孩子位置、且深度 < max_depth 的结点
    for _ in range(n - 1):
        while True:
            k = random.randrange(len(free))
            p, d = free[k]
            slots = [s for s in ("left", "right") if getattr(p, s) is None]
            if not slots:
                free[k] = free[-1]
                free.pop()
                continue
            break
        nd = _Node(0)
        setattr(p, random.choice(slots), nd)
        if d + 1 < max_depth:
            free.append((nd, d + 1))
        if len(by_depth) == d:
            by_depth.append([])
        by_depth[d].append(nd)
    return root, by_depth


def fit_int(root, by_depth):
    """若和超过 32 位，就从浅到深把整层改成 0 直到不溢出"""
    for layer in by_depth:
        if paths_sum(root) <= INT_MAX:
            break
        for nd in layer:
            nd.val = 0
    assert paths_sum(root) <= INT_MAX
    return lines(tree(_to_level(root)))


def digits_case(n, max_depth=10, lo=0, hi=9):
    root, by_depth = rand_shape(n, max_depth)
    for layer in by_depth:
        for nd in layer:
            nd.val = random.randint(lo, hi)
    return fit_int(root, by_depth)


def full_case(n):
    """完全二叉树，随机数字（n = 1000 时深度为 10）"""
    root = build([random.randint(0, 9) for _ in range(n)])
    by_depth, layer = [], [root]
    while layer:
        by_depth.append(layer)
        layer = [c for nd in layer for c in (nd.left, nd.right) if c]
    return fit_int(root, by_depth)


def samples():
    res = [
        (lines("[1,2,3]"), "25"),
        (lines("[4,9,0,5,1]"), "1026"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    return [
        lines("[0]"),
        lines("[9]"),
        lines("[1,0]"),
        lines("[1,null,0,0,null,null,9]"),
        lines(tree([2, 1, 4, 7, 4, 8, 3, 6, 4, 7])),
        # 深度 10 的单链：2147483647 恰好等于 INT_MAX
        lines("[2,1,null,4,null,7,null,4,null,8,null,3,null,6,null,4,null,7]"),
        lines("[2,null,1,null,4,null,7,null,4,null,8,null,3,null,6,null,4,null,7]"),
        digits_case(20),
        digits_case(100),
        digits_case(1000),
        digits_case(1000),
        digits_case(1000, lo=0, hi=1),
        digits_case(1000, lo=9, hi=9),
        full_case(1000),
    ]


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
