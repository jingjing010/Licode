from genlib import *
import json


def samples():
    return [
        (lines(cmat(["11110", "11010", "11000", "00000"])), "1"),
        (lines(cmat(["11000", "11000", "00100", "00011"])), "3"),
    ]


def rand_grid(m, n, p):
    return ["".join("1" if random.random() < p else "0" for _ in range(n)) for _ in range(m)]


def spiral(m, n):
    """一条蛇形的超长岛屿（DFS 递归很深）"""
    g = [["0"] * n for _ in range(m)]
    for i in range(0, m, 2):
        for j in range(n):
            g[i][j] = "1"
        if i + 1 < m:
            g[i + 1][n - 1 if (i // 2) % 2 == 0 else 0] = "1"
    return ["".join(r) for r in g]


def cases():
    res = [
        lines(cmat(["0"])),
        lines(cmat(["1"])),
        lines(cmat(["10101010101"])),
        lines(cmat(list("1101011"))),
        lines(cmat(["111", "101", "111"])),
    ]
    for (m, n, p) in [(5, 7, 0.5), (20, 30, 0.4), (50, 50, 0.6), (300, 300, 0.3), (300, 300, 0.55), (300, 300, 0.7)]:
        res.append(lines(cmat(rand_grid(m, n, p))))
    res.append(lines(cmat(["1" * 300] * 300)))
    res.append(lines(cmat(["0" * 300] * 300)))
    res.append(lines(cmat(["".join("1" if (i + j) % 2 == 0 else "0" for j in range(300)) for i in range(300)])))
    res.append(lines(cmat(spiral(300, 300))))
    res.append(lines(cmat(rand_grid(1, 300, 0.5))))
    return res


def brute(text):
    g = json.loads(text.strip().splitlines()[0])
    m, n = len(g), len(g[0])
    parent = list(range(m * n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(m):
        for j in range(n):
            if g[i][j] != "1":
                continue
            for di, dj in ((1, 0), (0, 1)):
                a, b2 = i + di, j + dj
                if a < m and b2 < n and g[a][b2] == "1":
                    parent[find(i * n + j)] = find(a * n + b2)
    return str(len({find(i * n + j) for i in range(m) for j in range(n) if g[i][j] == "1"}))


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 200，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
