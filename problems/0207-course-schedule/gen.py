from genlib import *
import sys


def samples():
    return [
        (lines(2, mat([[1, 0]])), "true"),
        (lines(2, mat([[1, 0], [0, 1]])), "false"),
    ]


def rand_dag(n, e):
    """随机 DAG：按随机拓扑序 order，只连「order 小 -> order 大」的边。返回 ([a,b] 列表, order)"""
    order = perm(n, 0)
    rank = {v: i for i, v in enumerate(order)}
    edges = set()
    e = min(e, n * (n - 1) // 2)
    while len(edges) < e:
        x, y = random.sample(range(n), 2)
        if rank[x] > rank[y]:
            x, y = y, x
        edges.add((y, x))          # 学 y 之前先学 x
    edges = [list(p) for p in edges]
    random.shuffle(edges)
    return edges, order


def with_cycle(n, e, cyc_len):
    edges, order = rand_dag(n, e - 1)
    have = {tuple(p) for p in edges}
    # 在拓扑序上取一段，补一条让它首尾相接的边，形成环
    i = random.randrange(n - cyc_len + 1)
    chain = order[i:i + cyc_len]
    for a, c in zip(chain, chain[1:]):
        if (c, a) not in have:
            edges.append([c, a])
            have.add((c, a))
    if (chain[0], chain[-1]) not in have:
        edges.append([chain[0], chain[-1]])
    random.shuffle(edges)
    assert len(edges) <= 5000
    return edges


def cases():
    res = [
        lines(1, mat([])),
        lines(5, mat([])),
        lines(3, mat([[0, 1], [0, 2], [1, 2]])),
        lines(3, mat([[0, 1], [1, 2], [2, 0]])),
        lines(4, mat([[1, 0], [2, 1], [3, 2], [1, 3]])),
        lines(6, mat([[1, 0], [2, 1], [4, 3], [5, 4], [3, 5]])),
        lines(2000, mat([[i + 1, i] for i in range(1999)])),
        lines(2000, mat([[i + 1, i] for i in range(1999)] + [[0, 1999]])),
    ]
    for (n, e) in [(10, 15), (100, 300), (2000, 5000), (500, 5000)]:
        res.append(lines(n, mat(rand_dag(n, e)[0])))
    for (n, e, cl) in [(10, 12, 3), (100, 300, 2), (2000, 4990, 2), (2000, 3400, 1500), (500, 4990, 7)]:
        ed = with_cycle(n, e, cl)
        res.append(lines(n, mat(ed)))
    return res


def brute(text):
    ls = text.strip().splitlines()
    n = int(ls[0])
    import json
    pre = json.loads(ls[1])
    g = [[] for _ in range(n)]
    for a, c in pre:
        g[c].append(a)
    color = [0] * n
    sys.setrecursionlimit(10000)

    def has_cycle(u):
        color[u] = 1
        for v in g[u]:
            if color[v] == 1 or (color[v] == 0 and has_cycle(v)):
                return True
        color[u] = 2
        return False

    return b(not any(color[u] == 0 and has_cycle(u) for u in range(n)))


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 207，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
