"""gen.py 用的测试数据格式化 / 随机生成工具（力扣风格）

在 gen.py 里 `from genlib import *` 即可使用。build.py 会在调用前用题号设置随机种子，保证可复现。
"""
import json
import random

__all__ = ["random", "arr", "mat", "s", "sarr", "carr", "cmat", "b", "tree", "lines",
           "rand_arr", "rand_sorted", "rand_distinct", "rand_str", "rand_tree", "rand_bst", "perm"]


def arr(a):
    """[1,2,3]"""
    return "[" + ",".join(str(int(x)) for x in a) + "]"


def mat(m):
    """[[1,2],[3,4]]"""
    return "[" + ",".join(arr(r) for r in m) + "]"


def s(x):
    """带双引号的字符串 "abc" """
    return json.dumps(x, ensure_ascii=False)


def sarr(a):
    """["ab","cd"]"""
    return "[" + ",".join(s(x) for x in a) + "]"


def carr(a):
    """字符数组 ["a","b"]，a 可以是字符串或字符列表"""
    return "[" + ",".join(s(c) for c in a) + "]"


def cmat(m):
    """字符矩阵 [["1","0"],["0","1"]]，每行可以是字符串"""
    return "[" + ",".join(carr(r) for r in m) + "]"


def b(x):
    return "true" if x else "false"


def tree(level):
    """层序列表（None 表示空）-> [3,9,20,null,null,15,7]"""
    level = list(level)
    while level and level[-1] is None:
        level.pop()
    return "[" + ",".join("null" if v is None else str(int(v)) for v in level) + "]"


def lines(*parts):
    """把每个参数拼成一行，生成一份完整的 .in 内容"""
    return "\n".join(str(p) for p in parts) + "\n"


# ---------------------------------------------------------------- 随机
def rand_arr(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def rand_sorted(n, lo, hi):
    return sorted(rand_arr(n, lo, hi))


def rand_distinct(n, lo, hi):
    return random.sample(range(lo, hi + 1), n)


def rand_str(n, alphabet="abcdefghijklmnopqrstuvwxyz"):
    return "".join(random.choice(alphabet) for _ in range(n))


def perm(n, start=1):
    a = list(range(start, start + n))
    random.shuffle(a)
    return a


class _Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, v):
        self.val, self.left, self.right = v, None, None


def _to_level(root):
    if root is None:
        return []
    out, q, i = [], [root], 0
    while i < len(q):
        nd = q[i]
        i += 1
        if nd is None:
            out.append(None)
            continue
        out.append(nd.val)
        q.append(nd.left)
        q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out


def rand_tree(n, lo=-100, hi=100):
    """随机形状的二叉树，返回层序列表（可直接交给 tree()）"""
    if n <= 0:
        return []
    nodes = [_Node(random.randint(lo, hi)) for _ in range(n)]
    for i in range(1, n):
        while True:
            p = nodes[random.randrange(i)]
            if p.left is None and random.random() < 0.5:
                p.left = nodes[i]
                break
            if p.right is None:
                p.right = nodes[i]
                break
    return _to_level(nodes[0])


def rand_bst(vals):
    """按 vals 的顺序依次插入得到的二叉搜索树（vals 应互不相同），返回层序列表"""
    root = None
    for v in vals:
        nd = _Node(v)
        if root is None:
            root = nd
            continue
        cur = root
        while True:
            if v < cur.val:
                if cur.left is None:
                    cur.left = nd
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = nd
                    break
                cur = cur.right
    return _to_level(root)
