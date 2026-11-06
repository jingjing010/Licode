from genlib import *
import json


def samples():
    return [
        (lines(mat([[2, 1, 1], [1, 1, 0], [0, 1, 1]])), "4"),
        (lines(mat([[2, 1, 1], [0, 1, 1], [1, 0, 1]])), "-1"),
        (lines(mat([[0, 2]])), "0"),
    ]


def rand_grid(m, n, w=(1, 6, 1)):
    return [random.choices([0, 1, 2], weights=w, k=n) for _ in range(m)]


def cases():
    res = [
        lines(mat([[0]])),
        lines(mat([[1]])),
        lines(mat([[2]])),
        lines(mat([[1, 2]])),
        lines(mat([[1, 1, 1, 1, 1, 1, 1, 1, 1, 2]])),
        lines(mat([[1] * 10 for _ in range(10)])),
    ]
    # 蛇形通道：只有一个烂橘子，传染路径最长
    g = [[1] * 10 for _ in range(10)]
    for r in range(1, 10, 2):
        for c in range(10):
            g[r][c] = 0
        g[r][9 if r % 4 == 1 else 0] = 1
    g[0][0] = 2
    res.append(lines(mat(g)))
    # 全是烂橘子 / 角落一个烂橘子
    res.append(lines(mat([[2] * 10 for _ in range(10)])))
    g = [[1] * 10 for _ in range(10)]
    g[9][9] = 2
    res.append(lines(mat(g)))
    for m, n in ((3, 4), (5, 5), (10, 10), (10, 10), (7, 9)):
        res.append(lines(mat(rand_grid(m, n))))
    res.append(lines(mat(rand_grid(10, 10, (3, 6, 1)))))
    return res


def brute(text):
    g = json.loads(text.strip().splitlines()[0])
    m, n, t = len(g), len(g[0]), 0
    while True:
        fresh = sum(row.count(1) for row in g)
        if fresh == 0:
            return str(t)
        new = [(i, j) for i in range(m) for j in range(n) if g[i][j] == 1 and any(
            0 <= i + a < m and 0 <= j + b < n and g[i + a][j + b] == 2
            for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        if not new:
            return "-1"
        for i, j in new:
            g[i][j] = 2
        t += 1


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 994，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
